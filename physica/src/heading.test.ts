import { describe, it, expect } from 'vitest';
import { findHeading } from './heading';
import type { TextItem } from 'pdfjs-dist/types/src/display/api';
const item = (str: string, x = 0, y = 600): TextItem => ({ str, dir: 'ltr', transform: [12, 0, 0, 12, x, y], width: 100, height: 12, fontName: 'test', hasEOL: false });
describe('PDF heading detection', () => {
  it('finds a title spread over PDF text fragments', () => { expect(findHeading([item('Problem 2.', 0), item('A falling magnet', 100)], { title: 'A falling magnet', label: '2' }, 800)).toBeCloseTo(.235); });
  it('finds numbered MCQ headings and avoids bare page numbers', () => { expect(findHeading([item('4. A particle travels')], { title: 'Problem 4', label: '4' }, 800)).toBeCloseTo(.235); expect(findHeading([item('4')], { title: 'Problem 4', label: '4' }, 800)).toBeNull(); });
  it('falls back for scans and mismatched headings', () => { expect(findHeading([], { title: 'A falling magnet', label: '2' }, 800)).toBeNull(); expect(findHeading([item('Problem 3')], { title: 'A falling magnet', label: '2' }, 800)).toBeNull(); });
});
