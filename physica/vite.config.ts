import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
export default defineConfig({ plugins: [react()], server: { port: 1420, strictPort: true, watch: { ignored: ['**/src-tauri/**', '**/tests/artifacts/**'] } }, clearScreen: false });
