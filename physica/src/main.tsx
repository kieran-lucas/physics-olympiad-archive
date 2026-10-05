import { createRoot } from 'react-dom/client';
import '@fontsource/lexend/400.css';
import '@fontsource/lexend/500.css';
import '@fontsource/lexend/600.css';
import { App } from './App';
import './style.css';
import './production.css';
createRoot(document.getElementById('root')!).render(<App />);
