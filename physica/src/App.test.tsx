import { beforeEach, afterEach, describe, expect, it, vi } from 'vitest';
import { cleanup, render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import type { Bootstrap, Attempt } from './types';
const native = vi.hoisted(() => ({ api: vi.fn(), close: vi.fn(), minimize: vi.fn(), toggleMaximize: vi.fn() }));
vi.mock('./api', () => ({ api: native.api }));
vi.mock('./PdfViewer', () => ({ PdfViewer: () => <div>Original local PDF</div> }));
vi.mock('@tauri-apps/api/window', () => ({ getCurrentWindow: () => ({ close: native.close, minimize: native.minimize, toggleMaximize: native.toggleMaximize }) }));
import { App } from './App';
let data: Bootstrap;
let current: Attempt | null;
beforeEach(() => {
  current = null;
  for (const action of [native.close, native.minimize, native.toggleMaximize]) action.mockReset().mockResolvedValue(undefined);
  window.matchMedia = vi.fn().mockReturnValue({ matches: true });
  data = { problems: [{ problem_id: 'real::1', title: 'A falling magnet', label: '1', competition: 'IPhO', year: '2025', section: 'Theory', format: 'Theory', topic: 3, secondary_topics: [], pdf_path: 'real.pdf', page_start: 1, page_end: 3, file_id: 1, document_id: 1, source_problem_id: 1, available: true, decision: 'KEEP', location: {}, solution: null, canonical_id: null, source_quality_notes: null }], states: {}, history: [], active: null, settings: { mode: 'Balanced', weights: [2, 1, 1], topics: [], exclude_solved: false, corpus_root: 'corpus' }, corpus_root: 'corpus', diagnostics: { source_db: 'source.sqlite', state_db: 'state.sqlite', total: 1, keep: 1, formats: { Theory: 1, MCQ: 0, Experimental: 0 }, topics: [0, 0, 0, 1, 0, 0], missing_pdf: 0, keep_missing_pdf: 0, unresolved_format: 0, unresolved_topic: 0, solution_linked: 0, aliases: 0, skipped: 0, fingerprint: 'fp', last_indexed: '1' } };
  native.api.mockReset(); native.api.mockImplementation(async (command: string, payload: Record<string, unknown>) => {
    if (command === 'bootstrap' || command === 'snapshot') return structuredClone(data);
    if (command === 'settings') { data.settings = { ...data.settings, ...payload }; return structuredClone(data); }
    if (command === 'draw') return data.problems[0];
    if (command === 'open') {
      current = { id: 1, problem_id: 'real::1', elapsed: 0, result: null, finished_at: null, started_at: 1, answer_viewed: false }; data.active = current;
      data.states['real::1'] = { problem_id: 'real::1', opened: 1, solved: 0, failed: 0, skipped: false, last_opened: 1, last_result: null }; return current;
    }
    if (command === 'outcome') {
      if (payload.action === 'Answer') { current!.answer_viewed = true; return current; }
      current = { ...current!, result: String(payload.action), finished_at: 2 }; data.history = [current]; data.active = null;
      const s = data.states['real::1']; s.last_result = String(payload.action); s.skipped = payload.action === 'SKIP'; s.solved = +(payload.action === 'Solved'); s.failed = +(payload.action === 'Failed'); return current;
    }
    if (command === 'restore') { data.states['real::1'].skipped = false; return structuredClone(data); }
    return true;
  });
});
afterEach(cleanup);
async function open() { const user = userEvent.setup(); render(<App />); await user.click(await screen.findByRole('button', { name: 'Draw a problem' })); const button = await screen.findByRole('button', { name: 'Open problem →' }); await waitFor(() => expect((button as HTMLButtonElement).disabled).toBe(false)); await user.click(button); await screen.findByText('Original local PDF'); return user; }
describe('window controls and practice modes', () => {
  it('skips the draw animation without rerolling and opens the preselected problem', async () => {
    window.matchMedia = vi.fn().mockReturnValue({ matches: false });
    const user = userEvent.setup(); render(<App />); await user.click(await screen.findByRole('button', { name: 'Draw a problem' }));
    await user.click(await screen.findByRole('button', { name: /Skip animation/ }));
    await user.click(screen.getByRole('button', { name: 'Open problem →' })); await screen.findByText('Original local PDF');
    expect(native.api.mock.calls.filter(call => call[0] === 'draw')).toHaveLength(1); expect(native.api).toHaveBeenCalledWith('open', { problem_id: 'real::1' });
  });
  it('orders teal/minimize, blue/maximize/restore, red/close and invokes native actions', async () => {
    const user = userEvent.setup(); const view = render(<App />);
    await screen.findByRole('button', { name: 'Draw a problem' });
    const dots = [...view.container.querySelectorAll<HTMLButtonElement>('.window-dots button')];
    expect(dots.map(dot => dot.getAttribute('aria-label'))).toEqual(['Minimize window', 'Maximize or restore window', 'Close window']);
    await user.click(dots[0]); expect(native.minimize).toHaveBeenCalledTimes(1); expect(native.toggleMaximize).not.toHaveBeenCalled(); expect(native.close).not.toHaveBeenCalled();
    await user.click(dots[1]); await user.click(dots[1]); expect(native.toggleMaximize).toHaveBeenCalledTimes(2); expect(native.close).not.toHaveBeenCalled();
    await user.click(dots[2]); await waitFor(() => expect(native.close).toHaveBeenCalledTimes(1)); expect(native.minimize).toHaveBeenCalledTimes(1);
  });
  it('exposes all six modes, saves selection, and restores its active chip', async () => {
    const user = userEvent.setup(); const view = render(<App />);
    await user.click(await screen.findByRole('button', { name: 'Practice controls' }));
    for (const mode of ['Balanced', 'Theory', 'MCQ', 'Experimental', 'Topic Focus', 'Unseen']) {
      const chip = screen.getByRole('button', { name: mode });
      await user.click(chip);
      await waitFor(() => expect(chip.getAttribute('aria-pressed')).toBe('true'));
      expect(native.api).toHaveBeenCalledWith('settings', expect.objectContaining({ mode }));
    }
    view.unmount(); render(<App />);
    await user.click(await screen.findByRole('button', { name: 'Practice controls' }));
    expect(screen.getByRole('button', { name: 'Unseen' }).getAttribute('aria-pressed')).toBe('true');
  });
  it('shows a format-specific empty-pool message without opening a different format', async () => {
    native.api.mockImplementationOnce(async () => { data.settings.mode = 'Experimental'; return structuredClone(data); });
    const user = userEvent.setup(); render(<App />);
    await screen.findByRole('button', { name: 'Draw a problem' });
    native.api.mockRejectedValueOnce('No eligible Experimental problems. Choose another mode to draw a different format.');
    await user.click(screen.getByRole('button', { name: 'Draw a problem' }));
    await screen.findByText('No eligible Experimental problems. Choose another mode to draw a different format.');
    expect(native.api.mock.calls.filter(call => call[0] === 'open')).toHaveLength(0);
    expect(screen.queryByRole('button', { name: 'Open problem →' })).toBeNull();
  });
});
describe('confirmed practice flows', () => {
  it('keeps corpus recovery available after startup failure', async () => { native.api.mockRejectedValueOnce('Invalid source database'); render(<App />); const button = await screen.findByRole('button', { name: 'Select corpus folder' }); expect((button as HTMLButtonElement).disabled).toBe(false); });
  for (const action of ['Answer', 'Solved', 'Failed', 'SKIP']) it(`${action} requires confirmation; Escape and Cancel preserve state`, async () => {
    const user = await open(); await user.click(screen.getByRole('button', { name: action })); expect(screen.getByRole('dialog')).toBeTruthy(); expect(native.api.mock.calls.filter(c => c[0] === 'outcome')).toHaveLength(0);
    await user.keyboard('{Escape}'); expect(screen.queryByRole('dialog')).toBeNull(); await user.click(screen.getByRole('button', { name: action })); await user.click(screen.getByRole('button', { name: 'Cancel' })); expect(native.api.mock.calls.filter(c => c[0] === 'outcome')).toHaveLength(0);
  });
  it('Solved saves first, then Back to home returns without drawing', async () => { const user = await open(); await user.click(screen.getByRole('button', { name: 'Solved' })); await user.click(screen.getByRole('button', { name: 'Confirm' })); await screen.findByText('What do you want to do next?'); await user.click(screen.getByRole('button', { name: 'Back to home' })); await screen.findByRole('button', { name: 'Draw a problem' }); expect(native.api.mock.calls.filter(c => c[0] === 'draw')).toHaveLength(1); expect(data.history[0].result).toBe('Solved'); });
  it('Solve another selects a new draw', async () => { const user = await open(); await user.click(screen.getByRole('button', { name: 'Solved' })); await user.click(screen.getByRole('button', { name: 'Confirm' })); await user.click(await screen.findByRole('button', { name: 'Solve another' })); await waitFor(() => expect(native.api.mock.calls.filter(c => c[0] === 'draw')).toHaveLength(2)); });
  it('SKIP is restored without erasing history', async () => { const user = await open(); await user.click(screen.getByRole('button', { name: 'SKIP' })); await user.click(screen.getByRole('button', { name: 'Confirm' })); await screen.findByRole('button', { name: 'Draw a problem' }); await user.click(screen.getByRole('button', { name: 'Skip List' })); await user.click(await screen.findByRole('button', { name: 'Restore' })); await waitFor(() => expect(screen.queryByRole('button', { name: 'Restore' })).toBeNull()); expect(data.history).toHaveLength(1); expect(data.states['real::1'].skipped).toBe(false); });
  it('Answer viewed does not imply Failed', async () => { const user = await open(); await user.click(screen.getByRole('button', { name: 'Answer' })); await user.click(screen.getByRole('button', { name: 'Confirm' })); await screen.findByText('No official solution linked for this problem.'); expect(current?.answer_viewed).toBe(true); expect(data.states['real::1'].failed).toBe(0); });
});
