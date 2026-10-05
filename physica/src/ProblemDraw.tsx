import { useCallback, useEffect, useLayoutEffect, useMemo, useRef, useState, type CSSProperties } from 'react';
import { TOPICS, source, type Problem } from './types';
import { GalaxyReveal } from './GalaxyReveal';
import './ProblemDraw.css';

export const DRAW_TIMING = { charge: 1000, roll: 4000, reveal: 3000, total: 8000 } as const;
const WINNER_INDEX = 24, CARD_PITCH = 226;
type Phase = 'charge' | 'rolling' | 'reveal' | 'ready';
const phaseText: Record<Phase, string> = { charge: 'Building momentum', rolling: 'The next challenge approaches', reveal: 'Your next problem', ready: 'Ready when you are' };

function Atom({ className = '' }: { className?: string }) {
  return <svg className={className} viewBox="0 0 120 120" fill="none" aria-hidden="true"><g stroke="currentColor" strokeWidth="1.25"><ellipse cx="60" cy="60" rx="49" ry="19" /><ellipse cx="60" cy="60" rx="49" ry="19" transform="rotate(60 60 60)" /><ellipse cx="60" cy="60" rx="49" ry="19" transform="rotate(120 60 60)" /></g><circle cx="60" cy="60" r="5" fill="currentColor" /><circle cx="109" cy="60" r="3" fill="currentColor" /></svg>;
}

/** Presentation only: the native scheduler has already selected `problem` before this mounts. */
export function ProblemDraw({ problem, pool, mode, busy, onOpen }: { problem: Problem; pool: Problem[]; mode: string; busy: boolean; onOpen: () => void }) {
  const [phase, setPhase] = useState<Phase>('charge');
  const [instant, setInstant] = useState(false);
  const timers = useRef<ReturnType<typeof setTimeout>[]>([]);
  const complete = useCallback(() => { timers.current.forEach(timer => clearTimeout(timer)); timers.current = []; setPhase('ready'); }, []);
  const finish = useCallback(() => { setInstant(true); complete(); }, [complete]);
  const dialog = useRef<HTMLDivElement>(null), open = useRef<HTMLButtonElement>(null), skip = useRef<HTMLButtonElement>(null);
  const phaseRef = useRef(phase); phaseRef.current = phase;
  const revealed = phase === 'reveal' || phase === 'ready', ready = phase === 'ready';
  const cards = useMemo(() => {
    const previews = pool.filter(p => p.available && p.decision === 'KEEP' && p.format === problem.format && p.problem_id !== problem.problem_id);
    return Array.from({ length: WINNER_INDEX + 4 }, (_, i) => i === WINNER_INDEX ? problem : previews[(i * 137 + 19) % previews.length] || problem);
  }, [pool, problem]);
  useLayoutEffect(() => {
    const target = dialog.current?.querySelector<HTMLElement>('.draw-target');
    const result = dialog.current?.querySelector<HTMLElement>('.draw-result');
    const root = dialog.current?.parentElement;
    if (!target || !result || !root || !result.offsetWidth || !result.offsetHeight) return;
    // Both cards share an aspect ratio: one scale preserves shape and center.
    const targetWidth = Number.parseFloat(getComputedStyle(target).width);
    const resultWidth = Number.parseFloat(getComputedStyle(result).width);
    root.style.setProperty('--draw-card-scale', String(targetWidth / resultWidth));
  }, [problem.problem_id]);
  useEffect(() => {
    const media = window.matchMedia('(prefers-reduced-motion: reduce)');
    if (media.matches) { finish(); return; }
    timers.current = [
      setTimeout(() => setPhase('rolling'), DRAW_TIMING.charge),
      setTimeout(() => setPhase('reveal'), DRAW_TIMING.charge + DRAW_TIMING.roll),
      setTimeout(complete, DRAW_TIMING.total),
    ];
    const reduced = () => { if (media.matches) finish(); };
    media.addEventListener?.('change', reduced);
    return () => { timers.current.forEach(timer => clearTimeout(timer)); timers.current = []; media.removeEventListener?.('change', reduced); };
  }, [problem.problem_id, complete, finish]);
  useEffect(() => {
    const previous = document.activeElement as HTMLElement | null;
    const key = (event: KeyboardEvent) => {
      if (event.key === 'Escape' && phaseRef.current !== 'ready') { event.preventDefault(); finish(); }
      if (event.key === 'Tab') {
        const buttons = [...dialog.current!.querySelectorAll<HTMLButtonElement>('button:not(:disabled)')];
        const first = buttons[0], last = buttons.at(-1);
        if (!first) { event.preventDefault(); return; }
        if (!dialog.current!.contains(document.activeElement) || (event.shiftKey && document.activeElement === first)) { event.preventDefault(); (event.shiftKey ? last : first)?.focus(); }
        else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
      }
    };
    document.addEventListener('keydown', key);
    return () => { document.removeEventListener('keydown', key); if (previous?.isConnected) previous.focus(); };
  }, [finish]);
  useEffect(() => { if (ready) open.current?.focus(); else if (phase === 'charge') skip.current?.focus(); }, [phase, ready]);
  const styles = { '--draw-charge-ms': `${DRAW_TIMING.charge}ms`, '--draw-roll-ms': `${DRAW_TIMING.roll}ms`, '--draw-reveal-ms': `${DRAW_TIMING.reveal}ms`, '--draw-total-ms': `${DRAW_TIMING.total}ms`, '--reel-end': `${-WINNER_INDEX * CARD_PITCH}px` } as CSSProperties;
  return <div className={`problem-draw draw-phase-${phase} draw-format-${problem.format?.toLowerCase() || 'theory'}${revealed ? ' draw-revealed' : ''}${instant ? ' draw-instant' : ''}`} style={styles}>
    <div className="draw-dialog" ref={dialog} role="dialog" aria-modal="true" aria-label="Problem draw">
      <header className="draw-header"><div><span className="draw-eyebrow">Physica / Problem draw</span><h2>{phaseText[phase]}</h2></div><span className="draw-mode"><i />{mode}</span></header>
      <div className="draw-scene">
        <GalaxyReveal active={revealed && !instant} />
        <div className="draw-sky" aria-hidden="true" /><div className="draw-horizon" aria-hidden="true" />
        <div className="draw-orbits" aria-hidden="true"><i /><i /><i /></div>
        <div className="draw-charge" aria-hidden="true"><Atom /><span>One problem. New possibilities.</span></div>
        <div className="draw-selection" aria-hidden="true"><i /><i /></div>
        <div className="draw-reel-mask" aria-hidden="true"><div className="draw-reel">{cards.map((p, i) => <div key={i} className={`draw-preview ${i === WINNER_INDEX ? 'draw-target' : ''}`} data-problem-id={p.problem_id}>
          <div className="draw-preview-type"><Atom />{p.format || 'Problem'}</div><h3>{p.title}</h3><p>{p.topic !== null ? TOPICS[p.topic] : 'Physics olympiad'}</p><div className="draw-preview-source">{source(p)}</div>
        </div>)}</div></div>
        <div className="draw-reveal-stage">
        <div className="draw-bloom" aria-hidden="true" />
        <article className="draw-result" aria-hidden={!revealed} data-problem-id={problem.problem_id}>
          <div className="draw-result-top"><span>{problem.format || 'Physics'}</span><Atom /></div>
          <h3>{problem.title}</h3><p>{problem.topic !== null ? TOPICS[problem.topic] : 'Physics olympiad'}</p><div className="draw-result-source">{source(problem)}</div>
        </article>
        </div>
        <div className="draw-scene-caption" aria-hidden="true">{revealed ? 'A fresh page. A new perspective.' : phase === 'rolling' ? 'Follow your curiosity' : 'Make room for the next idea'}</div>
      </div>
      <footer className="draw-footer"><div className="draw-footer-copy" role="status" aria-live="polite"><span className="draw-eyebrow">{revealed ? 'Selected problem' : 'Next up'}</span><div>{revealed ? problem.title : 'Something worth figuring out.'}</div></div><div className="draw-footer-actions">{!ready && <button ref={skip} className="draw-skip" onClick={finish}>Skip animation <span aria-hidden="true">↠</span></button>}<button ref={open} className="draw-open" disabled={!ready || busy} onClick={onOpen}>Open problem →</button></div></footer>
      <div className="draw-progress" aria-hidden="true"><i /></div>
    </div>
  </div>;
}
