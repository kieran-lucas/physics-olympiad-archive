import type { TextItem } from 'pdfjs-dist/types/src/display/api';
import type { Problem } from './types';
const normalize = (s: string) => s.toLowerCase().normalize('NFKC').replace(/[\u2010-\u2015]/g, '-').replace(/\s+/g, ' ').trim();
export function findHeading(items: TextItem[], problem: Pick<Problem, 'title' | 'label'>, height: number): number | null {
  // Reassemble PDF.js fragments into lines; standalone numbers are too ambiguous to be reliable anchors.
  const lines: { y: number; font: number; items: TextItem[] }[] = [];
  for (const item of items) {
    const y = item.transform[5]; let line = lines.find(l => Math.abs(l.y - y) < 3);
    if (!line) { line = { y, font: Math.abs(item.transform[3]), items: [] }; lines.push(line); }
    line.items.push(item);
  }
  const title = normalize(problem.title), label = normalize(problem.label || '');
  const escaped = label.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const numbered = label ? new RegExp(`^(?:(?:problem|question|task|theory|experiment(?:al)?|q)\\s*[-:.]?\\s*)?${escaped}(?:[.):]|\\s+[-–—:]|\\s+(?=[a-z]))`, 'i') : null;
  for (const line of lines.sort((a, b) => b.y - a.y)) {
    const text = normalize(line.items.sort((a, b) => a.transform[4] - b.transform[4]).map(i => i.str).join(' '));
    const titleMatch = title.length >= 7 && !/^problem\s*[\d-]*$/.test(title) && (text.includes(title) || (title.length > 24 && text.includes(title.slice(0, 24))));
    const numberMatch = numbered?.test(text) && !/^\d+\.\d/.test(text);
    if (titleMatch || numberMatch) return Math.max(0, Math.min(1, (height - line.y - line.font) / height));
  }
  return null;
}
