import { lazy, Suspense, useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { getCurrentWindow } from '@tauri-apps/api/window';
import { api } from './api';
import { Modal } from './Modal';
import { ProblemDraw } from './ProblemDraw';
import { FORMATS, TOPICS, source, time, type Attempt, type Bootstrap, type Problem, type Settings, type Snapshot } from './types';
type Tab = 'Practice' | 'Library' | 'History' | 'Skip List';
type Action = 'Answer' | 'Solved' | 'Failed' | 'SKIP';
// Keep PDF.js out of startup; warm its code while the draw animation runs.
const loadPdfViewer = () => import('./PdfViewer').then(module => ({ default: module.PdfViewer }));
const PdfViewer = lazy(loadPdfViewer);

export function App() {
  const [data, setData] = useState<Bootstrap | null>(null), [tab, setTab] = useState<Tab>('Practice');
  const [problem, setProblem] = useState<Problem | null>(null), [attempt, setAttempt] = useState<Attempt | null>(null);
  const [solution, setSolution] = useState(false), [drawer, setDrawer] = useState(false), [pending, setPending] = useState<Problem | null>(null);
  const [action, setAction] = useState<Action | null>(null), [next, setNext] = useState(false), [busy, setBusy] = useState(false), [error, setError] = useState('');
  const [initError, setInitError] = useState(false);
  const [elapsed, setElapsed] = useState(0), [running, setRunning] = useState(false);
  const clock = useRef({ base: 0, since: 0, running: false, attempt: null as Attempt | null });
  const notify = useCallback((s: string) => setError(s), []);
  const getElapsed = useCallback(() => Math.floor(clock.current.base + (clock.current.running ? (performance.now() - clock.current.since) / 1000 : 0)), []);
  const checkpoint = useCallback(async () => { const a = clock.current.attempt; if (a && !a.finished_at) await api('checkpoint', { attempt_id: a.id, elapsed: getElapsed() }); }, [getElapsed]);
  const pause = useCallback(() => { clock.current.base = getElapsed(); clock.current.running = false; setElapsed(clock.current.base); setRunning(false); }, [getElapsed]);
  const refresh = useCallback(async () => { const snapshot = await api<Snapshot>('snapshot'); setData(d => d ? { ...d, ...snapshot } : d); }, []);
  useEffect(() => { void api<Bootstrap>('bootstrap').then(setData).catch(e => { setInitError(true); notify(String(e)); }); }, [notify]);
  useEffect(() => {
    const tick = setInterval(() => { if (clock.current.running) setElapsed(getElapsed()); }, 250);
    const save = setInterval(() => { void checkpoint().catch(e => notify(String(e))); }, 5000);
    const blur = () => { void checkpoint().catch(e => notify(String(e))); }; window.addEventListener('pagehide', blur);
    return () => { clearInterval(tick); clearInterval(save); window.removeEventListener('pagehide', blur); };
  }, [checkpoint, getElapsed, notify]);
  useEffect(() => { if (!error) return; const t = setTimeout(() => setError(''), 7000); return () => clearTimeout(t); }, [error]);
  const home = useCallback(() => { pause(); void checkpoint().catch(e => notify(String(e))); setProblem(null); setSolution(false); setTab('Practice'); setNext(false); }, [pause, checkpoint, notify]);
  const open = useCallback(async (p: Problem) => {
    setBusy(true);
    void loadPdfViewer().catch(() => {});
    try {
      await checkpoint(); pause(); const a = await api<Attempt>('open', { problem_id: p.problem_id });
      clock.current = { base: a.elapsed, since: 0, running: false, attempt: a }; setElapsed(a.elapsed); setAttempt(a); setProblem(p); setSolution(false); setTab('Practice'); setPending(null); setDrawer(false); await refresh();
    } catch (e) { notify(String(e)); } finally { setBusy(false); }
  }, [checkpoint, pause, refresh, notify]);
  const draw = useCallback(async () => {
    if (busy || pending) return; setBusy(true);
    try { await checkpoint(); pause(); const selected = await api<Problem>('draw'); void loadPdfViewer().catch(() => {}); setPending(selected); setDrawer(false); setTab('Practice'); }
    catch (e) { notify(String(e)); } finally { setBusy(false); }
  }, [busy, pending, checkpoint, pause, notify]);
  const confirm = async () => {
    if (!action || !attempt) return; setBusy(true);
    try {
      const result = await api<Attempt>('outcome', { attempt_id: attempt.id, action, elapsed: getElapsed() });
      clock.current.attempt = result; setAttempt(result);
      if (action === 'Answer') { if (problem?.solution) setSolution(true); else notify('No official solution linked for this problem.'); }
      else { pause(); if (action === 'Solved') setNext(true); else home(); }
      setAction(null); await refresh();
    } catch (e) { notify(String(e)); } finally { setBusy(false); }
  };
  const restore = useCallback(async (p: Problem) => { try { const s = await api<Snapshot>('restore', { problem_id: p.problem_id }); setData(d => d ? { ...d, ...s } : d); } catch (e) { notify(String(e)); } }, [notify]);
  const settings = async (s: Settings) => { try { const v = await api<Snapshot>('settings', s); setData(d => d ? { ...d, ...v } : d); } catch (e) { notify(String(e)); } };
  const chooseCorpus = async () => { setBusy(true); try { const d = await api<Bootstrap | null>('pick_corpus'); if (d) { pause(); clock.current.attempt = null; setAttempt(null); setProblem(null); setData(d); setInitError(false); } } catch (e) { notify(String(e)); } finally { setBusy(false); } };
  const close = async () => { try { await checkpoint(); await getCurrentWindow().close(); } catch (e) { notify(String(e)); } };
  const active = data?.active && data.problems.find(p => p.problem_id === data.active?.problem_id);
  return <>
    <main className="app" aria-label="Physica olympiad trainer">
      <header className="titlebar" data-tauri-drag-region>
        <nav className="tabs" aria-label="Main navigation" data-tauri-drag-region>{(['Practice', 'Library', 'History', 'Skip List'] as Tab[]).map(t => <button key={t} className={`tab ${tab === t ? 'active' : ''}`} onClick={() => { setTab(t); if (t === 'Practice' && !next) home(); }} aria-current={tab === t ? 'page' : undefined}>{t}</button>)}</nav>
        <div className="title-actions"><button className="ticon" title="Practice controls" aria-label="Practice controls" onClick={() => setDrawer(x => !x)}>☷</button><button className="draw-top" disabled={busy || !!pending || !!next || !data?.diagnostics.keep} onClick={() => void draw()}>Draw ✦</button></div>
        <div className="window-dots"><button className="dot" aria-label="Minimize window" onClick={() => void getCurrentWindow().minimize().catch(e => notify(String(e)))} /><button className="dot" aria-label="Maximize or restore window" onClick={() => void getCurrentWindow().toggleMaximize().catch(e => notify(String(e)))} /><button className="dot" aria-label="Close window" onClick={() => void close()} /></div>
      </header>
      <div className="viewport">
        {tab === 'Practice' && !problem && <section className="page home active"><div className="micro left">A WIDER<br />PROBLEM<br />SPACE</div><div className="micro right">SAME<br />CURIOSITY<br />FURTHER</div><div className="page-inner home-inner"><div className="home-copy">
          <div className="kicker">Physics olympiad training · SPhO-oriented</div><h1>Pick a problem.<br /><span>Make it count.</span></h1>
          <p>One weighted draw at a time. Theory carries more weight, while topics are softly balanced so the long-run practice mix stays broad without feeling scripted.</p>
          <div className="home-actions">{data?.diagnostics.keep ? <button className="draw-main" disabled={busy || !!pending} onClick={() => void draw()}><span className="spark" aria-hidden="true">✦</span> Draw a problem</button> : data ? <button className="draw-main" disabled={busy} onClick={() => void chooseCorpus()}>Select corpus folder</button> : <button className="draw-main" disabled={!initError || busy} onClick={() => void chooseCorpus()}>{initError ? 'Select corpus folder' : 'Opening corpus…'}</button>}
            {active && <button className="resume" disabled={busy} onClick={() => void open(active)}>Resume last</button>}</div>
          <div className="mode-line"><span className="mode-chip">{data?.settings.mode || 'Balanced'}</span><span>SKIP removes a problem from rotation until restored.</span></div>
        </div></div></section>}
        {tab === 'Practice' && problem && <section className="page problem-page active" aria-label="Problem workspace">
          <Suspense fallback={<div className="pdf-loading" role="status">Loading original PDF…</div>}><PdfViewer key={`${problem.problem_id}:${solution}`} problem={problem} solution={solution} onStatement={() => setSolution(false)} onError={notify} /></Suspense>
          <aside className="problem-name" aria-label="Current problem" title={problem.title}><span>Current problem</span><strong>{problem.title}</strong></aside>
          <div className="timer-card"><div className="timer-label">Stopwatch</div><div className="timer-row"><div className="clock" aria-label="Elapsed time">{time(elapsed)}</div><div className="timer-controls"><button className="timer-icon" aria-label={running ? 'Pause stopwatch' : 'Start stopwatch'} disabled={!!attempt?.finished_at} onClick={() => { if (running) { pause(); void checkpoint(); } else { clock.current.since = performance.now(); clock.current.running = true; setRunning(true); } }}>{running ? '❚❚' : '▶'}</button><button className="timer-icon" aria-label="Reset stopwatch" disabled={!!attempt?.finished_at} onClick={() => { pause(); clock.current.base = 0; setElapsed(0); void checkpoint(); }}>↺</button></div></div></div>
          <div className="action-rail">{(['Answer', 'Solved', 'Failed', 'SKIP'] as Action[]).map((a, i) => <button key={a} className={`action ${a.toLowerCase()}`} disabled={busy || !!attempt?.finished_at} onClick={() => setAction(a)}><span className="action-symbol" aria-hidden="true">{a === 'SKIP' ? <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round"><path d="m3 5 8 7-8 7V5Zm8 0 8 7-8 7V5Z" /><path d="M21 5v14" /></svg> : ['▤', '✓', '×'][i]}</span><span>{a}</span></button>)}</div>
        </section>}
        {data && tab !== 'Practice' && <Collection tab={tab} data={data} onOpen={p => void open(p)} onRestore={p => void restore(p)} />}
        {drawer && <aside className="drawer open" aria-label="Practice controls"><div className="drawer-head"><b>Practice controls</b><button className="drawer-close" aria-label="Close practice controls" onClick={() => setDrawer(false)}>×</button></div>
          {data && <><div className="group open"><div className="group-head">Mode</div><div className="group-body"><div className="mode-grid">{['Balanced', 'Theory', 'MCQ', 'Experimental', 'Topic Focus', 'Unseen'].map(m => <button key={m} className={`mode-btn ${data.settings.mode === m ? 'active' : ''}`} aria-pressed={data.settings.mode === m} onClick={() => void settings({ ...data.settings, mode: m })}>{m}</button>)}</div>{data.settings.mode === 'Topic Focus' && <div className="topic-options">{TOPICS.map((t, i) => <label key={t}><input type="checkbox" checked={data.settings.topics.includes(i)} onChange={e => void settings({ ...data.settings, topics: e.target.checked ? [...data.settings.topics, i] : data.settings.topics.filter(x => x !== i) })} />{t}</label>)}{!data.settings.topics.length && <p>Choose at least one topic.</p>}</div>}</div></div>
            <div className="group open"><div className="group-head">Format selection weights</div><div className="group-body"><div className="weight-grid">{FORMATS.map((f, i) => <label key={f} className="weight"><input type="number" aria-label={`${f} weight`} min="0" max="100" step="0.25" value={data.settings.weights[i]} onChange={e => { const w = [...data.settings.weights] as Settings['weights']; w[i] = Number(e.target.value); void settings({ ...data.settings, weights: w }); }} /><span>{f}</span></label>)}</div></div></div>
            <div className="group open"><div className="group-head">Rotation</div><div className="group-body"><label className="toggle-row">Exclude solved problems<input type="checkbox" role="switch" checked={data.settings.exclude_solved} onChange={e => void settings({ ...data.settings, exclude_solved: e.target.checked })} /></label><p className="control-note">SKIP always excludes a problem until restored. Experimental topic balancing follows supply.</p></div></div></>}
          <div className="group open"><div className="group-head">Local corpus</div><div className="group-body"><p className="path">{data?.corpus_root || 'No corpus selected'}</p><button className="soft" disabled={busy} onClick={() => void chooseCorpus()}>Select corpus folder</button> <button className="soft" disabled={busy || !data?.corpus_root} onClick={async () => { setBusy(true); try { setData(await api<Bootstrap>('refresh')); notify('Corpus index refreshed.'); } catch (e) { notify(String(e)); } finally { setBusy(false); } }}>Refresh index</button></div></div>
          {data && <details className="group diagnostics"><summary>Diagnostics</summary><div className="group-body"><dl>{[['Normalized total', data.diagnostics.total], ['KEEP', data.diagnostics.keep], ...FORMATS.map(f => [f, data.diagnostics.formats[f]]), ...TOPICS.map((t, i) => [t, data.diagnostics.topics[i]]), ['Missing PDFs (all / KEEP)', `${data.diagnostics.missing_pdf} / ${data.diagnostics.keep_missing_pdf}`], ['Unresolved KEEP formats', data.diagnostics.unresolved_format], ['Unresolved KEEP topics', data.diagnostics.unresolved_topic], ['KEEP with official solution', data.diagnostics.solution_linked], ['KEEP aliases', data.diagnostics.aliases], ['Skipped', data.diagnostics.skipped]].map(([k, v]) => <div key={k}><dt>{k}</dt><dd>{v}</dd></div>)}</dl><p className="path">Source DB: {data.diagnostics.source_db}</p><p className="path">State DB: {data.diagnostics.state_db}</p><p className="path">Fingerprint: {data.diagnostics.fingerprint}</p><p className="control-note">Last indexed: {data.diagnostics.last_indexed ? new Date(Number(data.diagnostics.last_indexed) * 1000).toLocaleString() : '—'}</p><p className="control-note">Unknown topics retain their supply share. Unresolved formats stay browsable in Library and are excluded from weighted draws. Aliases share exclusion and draw once per canonical problem.</p></div></details>}
        </aside>}
      </div>
    </main>
    {pending && <ProblemDraw problem={pending} pool={data!.problems} mode={data!.settings.mode} busy={busy} onOpen={() => void open(pending)} />}
    {action && <Modal title={action === 'Answer' ? 'Open the official answer / solution?' : action === 'SKIP' ? 'Move this problem to Skip List?' : `Mark this problem ${action.toLowerCase()}?`} onCancel={() => { if (!busy) setAction(null); }}><p>{action === 'Answer' ? 'Only a linked official document will open. Viewing it does not mark this attempt Failed.' : action === 'SKIP' ? 'This problem will leave random rotation until you restore it. Your attempt and elapsed time will be saved.' : `Save ${action} and the current elapsed time (${time(getElapsed())})?`}</p><div className="confirm-actions"><button className="confirm-btn" disabled={busy} onClick={() => setAction(null)}>Cancel</button><button className={`confirm-btn ${action === 'Solved' ? 'success' : action === 'Failed' ? 'danger' : 'primary'}`} disabled={busy} onClick={() => void confirm()}>Confirm</button></div></Modal>}
    {next && <Modal title="What do you want to do next?" kicker="Solved" choice onCancel={home}><p>The result has been saved. Continue into another draw, or return to the home screen.</p><div className="confirm-actions"><button className="confirm-btn success" onClick={() => { setNext(false); home(); void draw(); }}>Solve another</button><button className="confirm-btn" onClick={home}>Back to home</button></div></Modal>}
    {error && <div className="toast show" role="status">{error}<button aria-label="Dismiss message" onClick={() => setError('')}>×</button></div>}
  </>;
}

function Collection({ tab, data, onOpen, onRestore }: { tab: Tab; data: Bootstrap; onOpen: (p: Problem) => void; onRestore: (p: Problem) => void }) {
  const [search, setSearch] = useState(''), [format, setFormat] = useState(''), [topic, setTopic] = useState(''), [status, setStatus] = useState(''), [competition, setCompetition] = useState('');
  const [startYear, setStartYear] = useState(''), [endYear, setEndYear] = useState(''), [decision, setDecision] = useState('KEEP'), [section, setSection] = useState(''), [sort, setSort] = useState('Source'), [page, setPage] = useState(0);
  const byId = useMemo(() => new Map(data.problems.map(p => [p.problem_id, p])), [data.problems]);
  const competitions = useMemo(() => [...new Set(data.problems.map(p => p.competition))].sort(), [data.problems]);
  const matches = useMemo(() => {
    const q = search.toLowerCase().trim();
    return data.problems.filter(p => {
      const s = data.states[p.problem_id];
      if (tab === 'Skip List' && !s?.skipped) return false;
      if (tab === 'Library' && decision && p.decision !== decision) return false;
      if (q && ![p.title, p.label, source(p)].join(' ').toLowerCase().includes(q)) return false;
      if (format && (format === 'Unresolved' ? p.format !== null : p.format !== format)) return false;
      if (topic && (topic === 'Unresolved' ? p.topic !== null : p.topic !== Number(topic))) return false;
      if (competition && p.competition !== competition) return false;
      if (section && !p.section?.toLowerCase().includes(section.toLowerCase())) return false;
      if ((startYear || endYear) && (!/^\d{4}$/.test(p.year || '') || (startYear && Number(p.year) < Number(startYear)) || (endYear && Number(p.year) > Number(endYear)))) return false;
      if (status === 'Unseen' && s?.opened) return false; if (status === 'Seen' && !s?.opened) return false;
      if (status === 'Solved' && !s?.solved) return false; if (status === 'Failed' && !s?.failed) return false; if (status === 'Skipped' && !s?.skipped) return false;
      return true;
    }).sort((a, b) => sort === 'Title' ? a.title.localeCompare(b.title) : sort === 'Year (newest)' ? Number(b.year || 0) - Number(a.year || 0) || a.title.localeCompare(b.title) : sort === 'Last opened' ? (data.states[b.problem_id]?.last_opened || 0) - (data.states[a.problem_id]?.last_opened || 0) : source(a).localeCompare(source(b), undefined, { numeric: true }) || (a.label || '').localeCompare(b.label || '', undefined, { numeric: true }));
  }, [data, search, format, topic, status, competition, section, decision, startYear, endYear, sort, tab]);
  useEffect(() => setPage(0), [search, format, topic, status, competition, section, decision, startYear, endYear, sort, tab]);
  const history = tab === 'History' ? data.history.filter(a => byId.has(a.problem_id) && (!search || [byId.get(a.problem_id)!.title, source(byId.get(a.problem_id)!)].join(' ').toLowerCase().includes(search.toLowerCase()))) : [];
  const count = tab === 'History' ? history.length : matches.length;
  const names = tab === 'Library' ? ['Browse the corpus', 'Find a specific problem by its existing metadata.'] : tab === 'History' ? ['Recent work', 'The problems you actually touched, including unfinished attempts.'] : ['Out of rotation', 'Skipped problems stay here until you deliberately restore them.'];
  const openButton = (p: Problem) => <button className="problem-link" onClick={() => onOpen(p)} disabled={!p.available} title={`${p.problem_id} · ${p.label || ''} · pp. ${p.page_start}–${p.page_end || '?'}${p.canonical_id ? ' · alias of ' + p.canonical_id : ''}${p.source_quality_notes ? ' · ' + p.source_quality_notes : ''}`}>{p.title}<small>{p.label ? `#${p.label} · ` : ''}{p.decision || 'Unreviewed'}{!p.available ? ' · PDF unavailable' : ''}</small></button>;
  return <section className="page active"><div className="page-inner section-wrap"><div className="section-head"><div><div className="kicker">{tab}</div><h2>{names[0]}</h2><p>{names[1]}</p></div><span className="badge">{count.toLocaleString()} {tab === 'History' ? 'attempts' : 'problems'}</span></div>
    <div className="filter-row"><input className="search" aria-label="Search problems" placeholder="Search title, label, competition, source…" value={search} onChange={e => setSearch(e.target.value)} />
      {tab === 'Library' && <><select aria-label="Format filter" value={format} onChange={e => setFormat(e.target.value)}><option value="">All formats</option>{[...FORMATS, 'Unresolved'].map(f => <option key={f}>{f}</option>)}</select><select aria-label="Topic filter" value={topic} onChange={e => setTopic(e.target.value)}><option value="">All topics</option>{TOPICS.map((t, i) => <option key={t} value={i}>{t}</option>)}<option value="Unresolved">Unclassified topic</option></select></>}
    </div>
    {tab === 'Library' && <><div className="filter-row secondary-filters"><select aria-label="Status filter" value={status} onChange={e => setStatus(e.target.value)}><option value="">All statuses</option>{['Unseen', 'Seen', 'Solved', 'Failed', 'Skipped'].map(s => <option key={s}>{s}</option>)}</select><select aria-label="Competition filter" value={competition} onChange={e => setCompetition(e.target.value)}><option value="">All sources</option>{competitions.map(c => <option key={c}>{c}</option>)}</select><input type="number" className="year-filter" aria-label="From year" placeholder="From year" value={startYear} onChange={e => setStartYear(e.target.value)} /><input type="number" className="year-filter" aria-label="To year" placeholder="To year" value={endYear} onChange={e => setEndYear(e.target.value)} /><select aria-label="Sort problems" value={sort} onChange={e => setSort(e.target.value)}>{['Source', 'Title', 'Year (newest)', 'Last opened'].map(s => <option key={s}>{s}</option>)}</select></div><details className="advanced"><summary>Advanced filters</summary><div className="filter-row"><select aria-label="Screening decision" value={decision} onChange={e => setDecision(e.target.value)}><option value="">All registered units</option>{['KEEP', 'BORDERLINE', 'REJECT'].map(d => <option key={d}>{d}</option>)}</select><input className="search" aria-label="Section filter" placeholder="Round / section" value={section} onChange={e => setSection(e.target.value)} /></div></details></>}
    <table className="data-table"><thead><tr>{(tab === 'History' ? ['Problem', 'Result', 'Time', 'When', 'Source'] : tab === 'Skip List' ? ['Problem', 'Source', 'Topic', ''] : ['Problem', 'Format', 'Topic', 'Source', 'Status']).map((h, i) => <th key={i}>{h}</th>)}</tr></thead><tbody>
      {tab === 'History' ? history.slice(page * 80, (page + 1) * 80).map(a => { const p = byId.get(a.problem_id)!; return <tr key={a.id}><td>{openButton(p)}</td><td><span className="badge">{a.result || (a.finished_at ? 'Opened' : 'In progress')}</span>{a.answer_viewed && <small className="answer-indicator">Answer viewed</small>}</td><td>{time(a.elapsed)}</td><td>{new Date((a.finished_at || a.started_at) * 1000).toLocaleString()}</td><td>{source(p)}</td></tr>; }) : matches.slice(page * 80, (page + 1) * 80).map(p => <tr key={p.problem_id}><td>{openButton(p)}</td>{tab === 'Skip List' ? <><td>{source(p)}</td><td>{p.topic !== null ? TOPICS[p.topic] : 'Unclassified'}</td><td><button className="restore" onClick={() => onRestore(p)}>Restore</button></td></> : <><td><span className="badge">{p.format || 'Unresolved'}</span></td><td title={p.secondary_topics.map(t => TOPICS[t]).join('; ')}>{p.topic !== null ? TOPICS[p.topic] : 'Unclassified'}{p.secondary_topics.length > 0 && <small>+{p.secondary_topics.length} secondary</small>}</td><td>{source(p)}</td><td><span className="badge">{data.states[p.problem_id]?.skipped ? 'Skipped' : data.states[p.problem_id]?.last_result || (data.states[p.problem_id]?.opened ? 'Seen' : 'Unseen')}</span></td></>}</tr>)}
      {count === 0 && <tr><td colSpan={5}><div className="empty">{tab === 'Skip List' ? 'Nothing skipped. Every problem stays in rotation until you choose SKIP.' : 'No matching records.'}</div></td></tr>}
    </tbody></table><div className="pagination"><button className="soft" disabled={page === 0} onClick={() => setPage(p => p - 1)}>Previous</button><span>{Math.min(page * 80 + 1, count)}–{Math.min((page + 1) * 80, count)} of {count.toLocaleString()}</span><button className="soft" disabled={(page + 1) * 80 >= count} onClick={() => setPage(p => p + 1)}>Next</button></div>
  </div></section>;
}
