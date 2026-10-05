import { useEffect, useRef, useState } from 'react';
import { convertFileSrc } from '@tauri-apps/api/core';
import { getDocument, GlobalWorkerOptions, TextLayer, type PDFDocumentProxy } from 'pdfjs-dist';
import type { TextItem } from 'pdfjs-dist/types/src/display/api';
import worker from 'pdfjs-dist/build/pdf.worker.min.mjs?url';
import 'pdfjs-dist/web/pdf_viewer.css';
import { api } from './api';
import { findHeading } from './heading';
import type { DocumentInfo, Problem } from './types';
GlobalWorkerOptions.workerSrc = worker;

function PdfPage({ doc, number, width, ratio, root, visible }: { doc: PDFDocumentProxy; number: number; width: number; ratio: number; root: HTMLDivElement | null; visible: (n: number) => void }) {
  const ref = useRef<HTMLDivElement>(null), canvas = useRef<HTMLCanvasElement>(null), text = useRef<HTMLDivElement>(null);
  const [near, setNear] = useState(false), [aspect, setAspect] = useState(ratio), [error, setError] = useState(''), [rendered, setRendered] = useState(false);
  useEffect(() => {
    const node = ref.current!;
    const observer = new IntersectionObserver(es => setNear(es[0].isIntersecting), { root, rootMargin: '650px 0px' }); observer.observe(node);
    const indicator = new IntersectionObserver(es => { if (es[0].isIntersecting) visible(number); }, { root, rootMargin: '-10% 0px -70% 0px' }); indicator.observe(node);
    return () => { observer.disconnect(); indicator.disconnect(); };
  }, [root, number, visible]);
  useEffect(() => {
    setRendered(false); setError('');
    if (!near) { if (canvas.current) { canvas.current.width = 0; canvas.current.height = 0; } text.current?.replaceChildren(); return; }
    let cancelled = false; let render: ReturnType<Awaited<ReturnType<PDFDocumentProxy['getPage']>>['render']> | undefined; let layer: TextLayer | undefined;
    void (async () => {
      try {
        const page = await doc.getPage(number); if (cancelled) return;
        const base = page.getViewport({ scale: 1 }), viewport = page.getViewport({ scale: width / base.width });
        setAspect(base.height / base.width); const node = canvas.current!, context = node.getContext('2d')!;
        const dpr = Math.min(window.devicePixelRatio || 1, 2); node.width = Math.floor(viewport.width * dpr); node.height = Math.floor(viewport.height * dpr);
        render = page.render({ canvas: node, canvasContext: context, viewport, transform: [dpr, 0, 0, dpr, 0, 0] }); await render.promise;
        if (cancelled) return; setRendered(true);
        const content = await page.getTextContent(); if (cancelled) return;
        text.current!.replaceChildren(); text.current!.style.setProperty('--scale-factor', String(viewport.scale));
        layer = new TextLayer({ textContentSource: content, container: text.current!, viewport }); await layer.render();
      } catch (e) { if (!cancelled) setError(String(e)); }
    })();
    return () => { cancelled = true; render?.cancel(); layer?.cancel(); };
  }, [doc, number, width, near]);
  return <div ref={ref} className="pdf-page" data-page={number} data-rendered={rendered} style={{ width, height: width * aspect }}>
    <canvas ref={canvas} style={{ width: '100%', height: '100%' }} aria-label={`PDF page ${number}`} /><div ref={text} className="textLayer" />
    {!rendered && !error && <span className="page-placeholder">{near ? 'Rendering' : 'Page'} {number}{near ? '…' : ''}</span>}{error && <div className="pdf-error">Page {number}: {error}</div>}
  </div>;
}
const cmaps = '/pdf-assets/cmaps/', standardFonts = '/pdf-assets/standard_fonts/', wasm = '/pdf-assets/wasm/';
export function PdfViewer({ problem, solution, onStatement, onError }: { problem: Problem; solution: boolean; onStatement: () => void; onError: (s: string) => void }) {
  const scroll = useRef<HTMLDivElement>(null);
  const [doc, setDoc] = useState<PDFDocumentProxy | null>(null), [info, setInfo] = useState<DocumentInfo | null>(null);
  const [width, setWidth] = useState(800), [zoom, setZoom] = useState(1), [ratio, setRatio] = useState(1.414);
  const [page, setPage] = useState(problem.page_start), [status, setStatus] = useState('Loading original PDF…'), [loadError, setLoadError] = useState('');
  const indicator = useRef((n: number) => setPage(n)).current;
  useEffect(() => {
    const observer = new ResizeObserver(es => setWidth(Math.max(300, Math.min(930, es[0].contentRect.width)))); observer.observe(scroll.current!); return () => observer.disconnect();
  }, []);
  useEffect(() => {
    let cancelled = false; let task: ReturnType<typeof getDocument> | undefined; setDoc(null); setInfo(null); setLoadError(''); setStatus('Loading original PDF…');setZoom(1);
    void (async () => {
      try {
        const d = await api<DocumentInfo>('document', { problem_id: problem.problem_id, solution }); if (cancelled) return;
        task = getDocument({ url: convertFileSrc(d.path), cMapUrl: cmaps, cMapPacked: true, standardFontDataUrl: standardFonts, wasmUrl: wasm, disableAutoFetch: true, disableStream: true });
        const pdf = await task.promise; if (cancelled) return;
        const first = await pdf.getPage(Math.min(d.page_start, pdf.numPages)); const v = first.getViewport({ scale: 1 });
        setRatio(v.height / v.width); setInfo(d); setDoc(pdf);
      } catch (e) { if (!cancelled) { setLoadError(String(e)); onError(String(e)); } }
    })();
    return () => { cancelled = true; void task?.destroy(); };
  }, [problem.problem_id, solution, onError]);
  useEffect(() => {
    if (!doc || !info) return;
    let cancelled = false;
    const jump = (number: number, y: number) => {
      const element = scroll.current?.querySelector<HTMLElement>(`[data-page="${number}"]`);
      if (element && scroll.current) scroll.current.scrollTop = element.offsetTop + y * element.clientHeight - 105;
      setPage(number);
    };
    void (async () => {
      const explicitPage = !solution && typeof problem.location.heading_page === 'number' && problem.location.heading_page >= info.page_start && problem.location.heading_page <= (info.page_end || doc.numPages) ? problem.location.heading_page : info.page_start;
      const start = Math.min(info.anchor?.page || explicitPage, doc.numPages); jump(start, info.anchor?.y_ratio ?? 0.04);
      if (info.anchor && !solution) { setStatus('Cached heading'); return; }
      if (solution) { setStatus('Official solution'); return; }
      try {
        const page = await doc.getPage(start), v = page.getViewport({ scale: 1 });
        let y: number | null = null;
        const bbox = problem.location.heading_bbox_pdf_points;
        if (Array.isArray(bbox) && problem.location.heading_page === start && typeof bbox[1] === 'number') y = bbox[1] / v.height;
        if (y === null) { const content = await page.getTextContent(); y = findHeading(content.items.filter((i): i is TextItem => 'str' in i), problem, v.height); }
        if (cancelled) return;
        if (y !== null) { jump(start, y); setStatus('Problem heading'); await api('anchor', { problem_id: problem.problem_id, fingerprint: info.fingerprint, page: start, y_ratio: y }); }
        else { setStatus('Page fallback'); jump(start, 0.04); }
      } catch { if (!cancelled) setStatus('Page fallback'); }
    })();
    return () => { cancelled = true; };
  }, [doc, info, problem, solution]);
  return <div className="pdf-workspace">
    <div className="pdf-scroll" ref={scroll} aria-label="Original PDF" tabIndex={0}>
      {!doc && <div className="pdf-loading">{loadError || status}{loadError && <p>The source has been left intact. Try another problem or check the PDF in Library.</p>}</div>}
      {doc && Array.from({ length: doc.numPages }, (_, i) => <PdfPage key={i} doc={doc} number={i + 1} width={width * zoom} ratio={ratio} root={scroll.current} visible={indicator} />)}
    </div>
    <div className="pdf-tools" aria-label="PDF controls">
      <button aria-label="Zoom out" onClick={() => setZoom(z => Math.max(.5, z - .15))}>−</button><button onClick={() => setZoom(1)}>Fit width</button><button aria-label="Zoom in" onClick={() => setZoom(z => Math.min(2.5, z + .15))}>+</button>
      <label>Page <input aria-label="Go to page" type="number" min="1" max={doc?.numPages || 1} value={page} onChange={e => { const n = Math.max(1, Math.min(doc?.numPages || 1, Number(e.target.value))); setPage(n); scroll.current?.querySelector<HTMLElement>(`[data-page="${n}"]`)?.scrollIntoView({ block: 'start' }); }} /> / {doc?.numPages || '…'}</label>
      <span className="viewer-status" data-anchor-status={status}>{status}{!solution && info && ` · problem pp. ${info.page_start}${info.page_end && info.page_end !== info.page_start ? '–' + info.page_end : ''}`}</span>
      {solution && <button onClick={onStatement}>Return to problem</button>}
      {solution && info?.note && <span title={info.note} className="solution-note">ⓘ {info.note}</span>}
    </div>
  </div>;
}
