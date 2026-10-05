import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { act, cleanup, fireEvent, render, screen } from '@testing-library/react';
import { DRAW_TIMING, ProblemDraw } from './ProblemDraw';
import type { Problem } from './types';
const problem: Problem = { problem_id: 'selected::1', title: 'A falling magnet', label: '1', competition: 'IPhO', year: '2025', section: 'Theory', format: 'Theory', topic: 3, secondary_topics: [], pdf_path: 'real.pdf', page_start: 1, page_end: 3, file_id: 1, document_id: 1, source_problem_id: 1, available: true, decision: 'KEEP', location: {}, solution: null, canonical_id: null, source_quality_notes: null };
let onOpen: ReturnType<typeof vi.fn>;
beforeEach(() => { vi.useFakeTimers(); onOpen = vi.fn(); window.matchMedia = vi.fn().mockReturnValue({ matches: false }); });
afterEach(() => { cleanup(); vi.restoreAllMocks(); vi.useRealTimers(); });
function show() { return render(<ProblemDraw problem={problem} pool={[problem, { ...problem, problem_id: 'preview::2', title: 'A charged pendulum' }]} mode="Theory" busy={false} onOpen={onOpen} />); }
const advance = (ms: number) => act(() => vi.advanceTimersByTime(ms));
describe('problem draw presentation', () => {
  it('stages charge, spin, reveal and ready over the full timeline without changing the selected problem', () => {
    expect(DRAW_TIMING).toEqual({ charge: 1000, roll: 4000, reveal: 3000, total: 8000 });
    const view = show(); const open = screen.getByRole('button', { name: 'Open problem →' }) as HTMLButtonElement;
    expect(view.container.firstElementChild!.classList.contains('draw-phase-charge')).toBe(true); expect(open.disabled).toBe(true); fireEvent.click(open); expect(onOpen).not.toHaveBeenCalled();
    advance(DRAW_TIMING.charge); expect(view.container.firstElementChild!.classList.contains('draw-phase-rolling')).toBe(true);
    advance(DRAW_TIMING.roll); expect(view.container.firstElementChild!.classList.contains('draw-phase-reveal')).toBe(true); expect(screen.getByRole('heading', { name: problem.title })).toBeTruthy(); expect(open.disabled).toBe(true);
    expect(view.container.firstElementChild!.classList.contains('draw-revealed')).toBe(true);
    advance(DRAW_TIMING.reveal - 1); expect(open.disabled).toBe(true);
    advance(1); expect(open.disabled).toBe(false); expect(view.container.firstElementChild!.classList.contains('draw-revealed')).toBe(true); expect(view.container.firstElementChild!.classList.contains('draw-instant')).toBe(false); expect(view.container.querySelector('.draw-result')!.getAttribute('data-problem-id')).toBe(problem.problem_id); fireEvent.click(open); expect(onOpen).toHaveBeenCalledTimes(1);
  });
  it('skipping animation reveals the same candidate and cancels remaining phase timers', () => {
    const view = show(); advance(200); fireEvent.click(screen.getByRole('button', { name: /Skip animation/ }));
    advance(DRAW_TIMING.total); expect(view.container.firstElementChild!.classList.contains('draw-phase-ready')).toBe(true);
    expect(view.container.firstElementChild!.classList.contains('draw-instant')).toBe(true);
    const open = screen.getByRole('button', { name: 'Open problem →' }) as HTMLButtonElement; expect(open.disabled).toBe(false); expect(document.activeElement).toBe(open); expect(view.container.querySelector('.draw-result')!.getAttribute('data-problem-id')).toBe(problem.problem_id); fireEvent.click(open); expect(onOpen).toHaveBeenCalledTimes(1);
  });
  it('Escape finishes the animation and keyboard focus stays inside the draw dialog', () => {
    show(); advance(DRAW_TIMING.charge); fireEvent.keyDown(document, { key: 'Escape' }); const open = screen.getByRole('button', { name: 'Open problem →' }) as HTMLButtonElement;
    expect(open.disabled).toBe(false); expect(document.activeElement).toBe(open); fireEvent.keyDown(document, { key: 'Tab' }); expect(document.activeElement).toBe(open); advance(DRAW_TIMING.total); expect(open.disabled).toBe(false);
  });
  it('respects reduced motion and cleans up pending timers on unmount', () => {
    const schedule = vi.spyOn(globalThis, 'setTimeout'), cancel = vi.spyOn(globalThis, 'clearTimeout');
    const delays = [DRAW_TIMING.charge, DRAW_TIMING.charge + DRAW_TIMING.roll, DRAW_TIMING.total];
    window.matchMedia = vi.fn().mockReturnValue({ matches: true }); const reduced = show(); expect((screen.getByRole('button', { name: 'Open problem →' }) as HTMLButtonElement).disabled).toBe(false); expect(screen.queryByRole('button', { name: /Skip animation/ })).toBeNull(); expect(schedule.mock.calls.some(call => delays.includes(Number(call[1])))).toBe(false); reduced.unmount();
    schedule.mockClear(); window.matchMedia = vi.fn().mockReturnValue({ matches: false }); const animated = show();
    const ownedTimers = schedule.mock.calls.flatMap((call, i) => delays.includes(Number(call[1])) ? [schedule.mock.results[i].value] : []);
    expect(ownedTimers).toHaveLength(3); animated.unmount(); for (const timer of ownedTimers) expect(cancel).toHaveBeenCalledWith(timer);
  });
});
