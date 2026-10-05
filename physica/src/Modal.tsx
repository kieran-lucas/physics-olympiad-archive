import { useEffect, useRef, type ReactNode } from 'react';
export function Modal({ title, children, onCancel, kicker = 'Confirm action', choice = false }: { title: string; children: ReactNode; onCancel: () => void; kicker?: string; choice?: boolean }) {
  const ref = useRef<HTMLDivElement>(null);
  const cancel = useRef(onCancel); cancel.current = onCancel;
  useEffect(() => {
    const previous = document.activeElement as HTMLElement | null;
    const box = ref.current!;
    const buttons = () => [...box.querySelectorAll<HTMLElement>('button:not(:disabled),input,select,[tabindex="0"]')];
    buttons()[0]?.focus();
    const key = (e: KeyboardEvent) => {
      if (e.key === 'Escape') { e.preventDefault(); cancel.current(); }
      if (e.key === 'Tab') {
        const list = buttons(), first = list[0], last = list.at(-1);
        if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last?.focus(); }
        if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first?.focus(); }
      }
    };
    document.addEventListener('keydown', key);
    return () => { document.removeEventListener('keydown', key); previous?.focus(); };
  }, []);
  return <div className={`confirm-modal show ${choice ? 'solve-choice' : ''}`} onMouseDown={e => { if (e.target === e.currentTarget) onCancel(); }}>
    <div className="confirm-box" ref={ref} role="dialog" aria-modal="true" aria-labelledby="modal-title"><div className="confirm-kicker">{kicker}</div><h3 id="modal-title">{title}</h3>{children}</div>
  </div>;
}
