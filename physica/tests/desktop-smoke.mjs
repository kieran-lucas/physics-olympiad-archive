// Drives the actual Windows Tauri/WebView2 binary. Uses a fresh, isolated state profile.
import { chromium, expect } from '@playwright/test';
import { spawn } from 'node:child_process';
import { mkdirSync, mkdtempSync, readFileSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { resolve, join } from 'node:path';
const exe = resolve(process.env.PHYSICA_EXE || 'src-tauri/target/debug/physica.exe');
const profile = mkdtempSync(join(tmpdir(), 'physica-smoke-'));
const artifacts = resolve('tests/artifacts'); mkdirSync(artifacts, { recursive: true });
const report = { executable: exe, state_profile: profile, samples: [], checks: [], console_errors: [] };
let child, browser, page;
const delay = ms => new Promise(r => setTimeout(r, ms));
async function launch() {
  child = spawn(exe, [], { cwd: resolve('..'), windowsHide: true, env: { ...process.env, PHYSICA_STATE_DIR: profile, WEBVIEW2_ADDITIONAL_BROWSER_ARGUMENTS: '--remote-debugging-port=9223' }, stdio: 'ignore' });
  child.on('error', e => { report.launch_error = String(e); });
  for (let i = 0; i < 100; i++) { try { const res = await fetch('http://127.0.0.1:9223/json/version'); if (res.ok) break; } catch {} await delay(300); }
  browser = await chromium.connectOverCDP('http://127.0.0.1:9223');
  for (let i = 0; i < 100; i++) { page = browser.contexts().flatMap(c => c.pages()).find(p => /127\.0\.0\.1:1420|tauri\.localhost/.test(p.url())); if (page) break; await delay(200); }
  if (!page) throw Error('Physica WebView did not appear');
  page.on('pageerror', e => report.console_errors.push(String(e)));
  await expect(page.getByRole('button', { name: 'Draw a problem', exact: true })).toBeVisible({ timeout: 30000 });
}
async function native(command, payload = {}) { return page.evaluate(({ command, payload }) => window.__TAURI_INTERNALS__.invoke('api', { command, payload }), { command, payload }); }
async function openProblem(p) {
  await page.getByRole('button', { name: 'Library', exact: true }).click();
  await page.getByRole('textbox', { name: 'Search problems' }).fill(p.title);
    const rows = page.locator('tbody tr').filter({ has: page.locator(`button[title^="${p.problem_id} ·"]`) });
  await rows.locator('.problem-link').click();
  await expect(page.locator('.pdf-page').first()).toBeVisible({ timeout: 20000 });
  await page.waitForFunction(() => { const s = document.querySelector('[data-anchor-status]')?.getAttribute('data-anchor-status'); return s && !s.includes('Loading'); }, { timeout: 20000 });
  const pageNumber = p.page_start;
  await page.waitForFunction(n => document.querySelector(`[data-page="${n}"]`)?.getAttribute('data-rendered') === 'true', pageNumber, { timeout: 20000 });
  await delay(250);
  const rendered = await page.evaluate(n => {
    const canvas = document.querySelector(`[data-page="${n}"] canvas`), ctx = canvas.getContext('2d');
    const pixels = ctx.getImageData(0, 0, canvas.width, canvas.height).data; let ink = 0;
    for (let i = 0; i < pixels.length; i += 16) if (pixels[i] < 220 && pixels[i + 3] > 0) ink++;
    return { ink, text_spans: document.querySelectorAll(`[data-page="${n}"] .textLayer span`).length, status: document.querySelector('[data-anchor-status]')?.getAttribute('data-anchor-status'), scroll: document.querySelector('.pdf-scroll').scrollTop, page: document.querySelector('[aria-label="Go to page"]').value, error: document.querySelector('.pdf-error')?.textContent || null };
  }, pageNumber);
  expect(rendered.ink).toBeGreaterThan(20); expect(rendered.error).toBeNull();
  report.samples.push({ id: p.problem_id, format: p.format, topic: p.topic, page_start: p.page_start, ...rendered });
  return rendered;
}
async function action(name) { await page.getByRole('button', { name, exact: true }).click(); await expect(page.getByRole('dialog')).toBeVisible(); await page.getByRole('button', { name: 'Confirm', exact: true }).click(); }
async function stop() {
  if (page && !page.isClosed()) await page.getByRole('button', { name: 'Close window', exact: true }).click().catch(() => {});
  await delay(500); await browser?.close().catch(() => {}); child?.kill(); await delay(500);
}
try {
  await launch();
  const data = await native('bootstrap'); report.diagnostics = data.diagnostics;
  expect(data.diagnostics.keep).toBeGreaterThan(0);
  await page.context().route(/https?:\/\/(?!127\.0\.0\.1|localhost|tauri\.localhost|asset\.localhost|ipc\.localhost)/, route => route.abort());
  await page.screenshot({ path: join(artifacts, 'home.png') });
  const pool = data.problems.filter(p => p.available && p.decision === 'KEEP');
  const samples = new Map();
  for (const f of ['Theory', 'MCQ', 'Experimental']) for (let t = 0; t < 6; t++) {
    const p = pool.find(p => p.format === f && p.topic === t && p.title.length > 10 && !p.title.startsWith('Problem ')); if (p) samples.set(p.problem_id, p);
  }
  for (const id of ['raw::5', 'raw::962', 'raw::963', 'raw::964', 'raw::131']) { const p = pool.find(p => p.problem_id === id); if (p) samples.set(id, p); }
  for (const p of samples.values()) await openProblem(p);
  report.checks.push('Real PDFs rendered across available format/topic pairs; text-based anchors and scan fallback exercised');
  const multi = pool.find(p => p.problem_id === 'raw::4'); await openProblem(multi);
  await page.getByRole('button', { name: 'Start stopwatch' }).click();
  const timer = await page.locator('.timer-card').boundingBox(); await page.getByRole('spinbutton', { name: 'Go to page' }).fill('8');
  await page.waitForFunction(() => document.querySelector('[data-page="8"]')?.getAttribute('data-rendered') === 'true');
  await delay(2000);
  const after = await page.locator('.timer-card').boundingBox(); expect(Math.abs(timer.y - after.y)).toBeLessThan(1); expect(Math.abs(timer.x - after.x)).toBeLessThan(1);
  await page.screenshot({ path: join(artifacts, 'solving-page-8.png') }); report.checks.push('Timer stays pinned while scrolling to page 8');
  for (const a of ['Answer', 'Solved', 'Failed', 'SKIP']) { const before = await native('snapshot'); await page.getByRole('button', { name: a, exact: true }).click(); await expect(page.getByRole('dialog')).toBeVisible(); await page.keyboard.press('Escape'); const after = await native('snapshot'); expect(after.history).toEqual(before.history); }
  report.checks.push('All four actions require confirmation; Escape preserves state');
  await action('Failed'); await expect(page.getByRole('button', { name: 'Draw a problem', exact: true })).toBeVisible();
  const linked = pool.find(p => p.problem_id === 'raw::5'); await openProblem(linked); await action('Answer');
  await expect(page.getByRole('button', { name: 'Return to problem' })).toBeVisible({ timeout: 20000 });
  await page.waitForFunction(() => document.querySelector('.pdf-page')?.getAttribute('data-rendered') === 'true'); await page.screenshot({ path: join(artifacts, 'official-solution.png') });
  await page.getByRole('button', { name: 'Return to problem' }).click(); await action('Solved');
  await expect(page.getByText('What do you want to do next?')).toBeVisible(); await page.getByRole('button', { name: 'Solve another', exact: true }).click();
  await expect(page.getByRole('dialog', { name: 'Problem draw' })).toBeVisible(); await expect(page.getByRole('button', { name: 'Open problem →' })).toBeEnabled({ timeout: 10000 });await page.getByRole('button', { name: 'Open problem →' }).click();
  await expect(page.locator('.pdf-page').first()).toBeVisible({ timeout: 20000 }); await action('Solved'); await page.getByRole('button', { name: 'Back to home' }).click();
  report.checks.push('Official solution opens in same viewer; Solved supports both next choices');
  const skipped = pool.find(p => p.problem_id === 'raw::962'); await openProblem(skipped); await action('SKIP');
  const beforeRestart = await native('snapshot');expect(beforeRestart.states[skipped.problem_id].skipped).toBe(true);
  for (let i = 0; i < 100; i++) expect((await native('draw')).problem_id).not.toBe(skipped.problem_id);
  await native('settings', { ...beforeRestart.settings, mode: 'Topic Focus', topics: [5], exclude_solved: true });
  for (let i = 0; i < 15; i++) { const p = await native('draw'); expect(p.topic).toBe(5); expect(beforeRestart.states[p.problem_id]?.solved || 0).toBe(0); }
  await native('settings', { ...beforeRestart.settings, mode: 'Unseen' });
  for (let i = 0; i < 15; i++) { const p = await native('draw'); expect(beforeRestart.states[p.problem_id]?.opened || 0).toBe(0); }
  await native('settings', beforeRestart.settings);
  report.checks.push('Topic Focus, Unseen and Exclude solved work with real corpus; external network blocked during rendering');
  await stop(); await launch(); const restored = await native('snapshot');
  expect(restored.states[skipped.problem_id].skipped).toBe(true);expect(restored.history.filter(a => a.result === 'Solved').length).toBeGreaterThanOrEqual(2);expect(restored.history.some(a => a.result === 'Failed' && a.elapsed >= 1)).toBe(true);
  await page.getByRole('button', { name: 'Skip List', exact: true }).click(); await page.getByRole('button', { name: 'Restore', exact: true }).click();
  const state = await native('snapshot'); expect(state.states[skipped.problem_id].skipped).toBe(false);expect(state.history.length).toEqual(restored.history.length);
  await openProblem(linked); await page.getByRole('button', { name: 'Start stopwatch' }).click();await delay(2100);await page.getByRole('button', { name: 'Pause stopwatch' }).click();
  const activeBefore = await native('snapshot'); await stop(); await launch();
  await page.getByRole('button', { name: 'Resume last' }).click();
  await expect(page.getByRole('button', { name: 'Start stopwatch' })).toBeVisible();
  expect((await native('snapshot')).active.elapsed).toBe(activeBefore.active.elapsed);
  report.checks.push('Unfinished stopwatch attempt resumes paused after a second restart');
  report.checks.push('SKIP exclusion and Solved/Failed elapsed history persist across process restart; Restore preserves history');
  report.success = true;
} catch (e) {
  report.success = false; report.failure = String(e); await page?.screenshot({ path: join(artifacts, 'failure.png') }).catch(() => {}); console.error(String(e)); process.exitCode = 1;
} finally {
  writeFileSync(join(artifacts, 'desktop-smoke.json'), JSON.stringify(report, null, 2)); await stop();
  console.log(JSON.stringify({ success: report.success, samples: report.samples.length, diagnostics: report.diagnostics, checks: report.checks, errors: report.console_errors.slice(0, 8) }, null, 2));
}
