import { mkdirSync, cpSync } from 'node:fs';
for (const folder of ['cmaps', 'standard_fonts', 'wasm', 'iccs']) {
  mkdirSync(`public/pdf-assets/${folder}`, { recursive: true });
  cpSync(`node_modules/pdfjs-dist/${folder}`, `public/pdf-assets/${folder}`, { recursive: true });
}
