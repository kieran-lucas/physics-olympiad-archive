import { useEffect, useRef } from 'react';

const DELAY_MS = 500, LIGHT_MS = 2500;

/** Original procedural art, inspired by accretion disks; no downloaded assets. */
function makeDisk() {
  const texture = document.createElement('canvas'); texture.width = texture.height = 768;
  const ctx = texture.getContext('2d'); if (!ctx) return null;
  const center = 384, radius = 355;
  ctx.translate(center, center);
  const gas = ctx.createRadialGradient(0, 0, radius * .43, 0, 0, radius);
  gas.addColorStop(0, 'rgba(2,9,30,0)'); gas.addColorStop(.2, 'rgba(7,31,91,.85)');
  gas.addColorStop(.45, 'rgba(32,108,245,.85)'); gas.addColorStop(.62, 'rgba(120,236,255,.8)');
  gas.addColorStop(.8, 'rgba(29,91,221,.45)'); gas.addColorStop(1, 'rgba(31,82,191,0)');
  ctx.fillStyle = gas; ctx.fillRect(-center, -center, 768, 768);
  // Build the turbulence once. Only this cached image rotates on each frame.
  let seed = 90210;
  const random = () => { seed = (Math.imul(seed, 1664525) + 1013904223) >>> 0; return seed / 4294967296; };
  for (let arm = 0; arm < 7; arm++) {
    for (let strand = 0; strand < 12; strand++) {
      ctx.beginPath();
      for (let step = 0; step <= 64; step++) {
        const r = radius * (.52 + step / 64 * .46);
        const angle = arm / 7 * Math.PI * 2 + step / 64 * 2.7 + strand * .025;
        const x = Math.cos(angle) * r, y = Math.sin(angle) * r;
        if (!step) ctx.moveTo(x, y); else ctx.lineTo(x, y);
      }
      ctx.strokeStyle = strand % 3 === 0 ? 'rgba(191,249,255,.35)' : 'rgba(58,149,255,.22)';
      ctx.lineWidth = strand % 3 === 0 ? 1.1 : 2; ctx.stroke();
    }
  }
  for (let i = 0; i < 3200; i++) {
    const r = radius * (.53 + random() * .44), arm = i % 7;
    const angle = arm / 7 * Math.PI * 2 + (r / radius - .52) * 5.9 + (random() - .5) * .25;
    ctx.fillStyle = i % 5 === 0 ? 'rgba(226,254,255,.85)' : `rgba(80,176,255,${.2 + random() * .55})`;
    ctx.beginPath(); ctx.arc(Math.cos(angle) * r, Math.sin(angle) * r, .4 + random() * 1.25, 0, Math.PI * 2); ctx.fill();
  }
  for (let band = 0; band < 12; band++) {
    ctx.strokeStyle = `rgba(169,244,255,${.16 + band % 3 * .08})`; ctx.lineWidth = .8;
    ctx.beginPath(); ctx.arc(0, 0, radius * (.57 + band * .029), 0, Math.PI * 2); ctx.stroke();
  }
  return texture;
}

function makeSpace(width: number, height: number, dpr: number) {
  const sky = document.createElement('canvas'); sky.width = Math.round(width * dpr); sky.height = Math.round(height * dpr);
  const ctx = sky.getContext('2d'); if (!ctx) return sky;
  ctx.scale(dpr, dpr);
  const night = ctx.createLinearGradient(0, 0, width, height);
  night.addColorStop(0, '#030916'); night.addColorStop(.5, '#07162d'); night.addColorStop(1, '#020713');
  ctx.fillStyle = night; ctx.fillRect(0, 0, width, height);
  for (const [x, y, color] of [[.14, .35, 'rgba(31,86,206,.38)'], [.78, .64, 'rgba(11,140,207,.3)'], [.6, .1, 'rgba(84,67,181,.23)']] as const) {
    ctx.save(); ctx.translate(width * x, height * y); ctx.rotate(-.3); ctx.scale(1, .58);
    const radius = width * .65, mist = ctx.createRadialGradient(0, 0, 0, 0, 0, radius);
    mist.addColorStop(0, color); mist.addColorStop(1, 'rgba(0,0,0,0)');
    ctx.fillStyle = mist; ctx.fillRect(-radius, -radius, radius * 2, radius * 2); ctx.restore();
  }
  let seed = 731;
  const random = () => { seed = (Math.imul(seed, 1664525) + 1013904223) >>> 0; return seed / 4294967296; };
  for (let i = 0; i < 950; i++) {
    const x = random() * width, y = random() * height, size = .35 + random() * 1.35;
    ctx.fillStyle = `rgba(${i % 5 === 0 ? '107,189,255' : '210,239,255'},${.2 + random() * .65})`;
    ctx.beginPath(); ctx.arc(x, y, size / 2, 0, Math.PI * 2); ctx.fill();
    if (i % 53 === 0) { ctx.fillStyle = 'rgba(161,222,255,.45)'; ctx.fillRect(x - 3, y - .3, 6, .6); ctx.fillRect(x - .3, y - 3, .6, 6); }
  }
  return sky;
}

export function GalaxyReveal({ active }: { active: boolean }) {
  const back = useRef<HTMLCanvasElement>(null), front = useRef<HTMLCanvasElement>(null);
  const disk = useRef<HTMLCanvasElement | null>(null);
  const sky = useRef<HTMLCanvasElement | null>(null);
  const prepared = useRef({ width: 0, height: 0 });
  useEffect(() => {
    if (typeof window.CanvasRenderingContext2D === 'function' && back.current) {
      disk.current = makeDisk();
      const { clientWidth: width, clientHeight: height } = back.current;
      sky.current = makeSpace(width, height, Math.min(window.devicePixelRatio || 1, 1.25)); prepared.current = { width, height };
    }
    return () => { disk.current = null; sky.current = null; };
  }, []);
  useEffect(() => {
    if (!active || !disk.current || !back.current || !front.current) return;
    const canvases = [back.current, front.current], contexts = canvases.map(c => c.getContext('2d'));
    if (!contexts[0] || !contexts[1]) return;
    const dpr = Math.min(window.devicePixelRatio || 1, 1.25);
    let width = 0, height = 0, frame = 0, frames = 0;
    const resize = () => {
      width = canvases[0].clientWidth; height = canvases[0].clientHeight;
      for (const canvas of canvases) { canvas.width = Math.round(width * dpr); canvas.height = Math.round(height * dpr); }
      if (prepared.current.width !== width || prepared.current.height !== height) {
        sky.current = makeSpace(width, height, dpr); prepared.current = { width, height };
      }
    };
    resize(); const observer = new ResizeObserver(resize); observer.observe(canvases[0]);
    const started = performance.now();
    const render = (now: number) => {
      const elapsed = now - started;
      if (elapsed >= DELAY_MS + LIGHT_MS) return;
      if (elapsed < DELAY_MS) { frame = requestAnimationFrame(render); return; }
      const time = (elapsed - DELAY_MS) / 1000, x = width / 2, y = height / 2;
      for (let layer = 0; layer < 2; layer++) {
        const ctx = contexts[layer]!; ctx.setTransform(dpr, 0, 0, dpr, 0, 0); ctx.clearRect(0, 0, width, height);
        if (!layer) {
          ctx.save(); ctx.translate(x, y); ctx.scale(1.01 + time * .008, 1.01 + time * .008);
          if (sky.current) ctx.drawImage(sky.current, -x, -y, width, height); ctx.restore();
          const photonRadius = Math.min(width * .34, height * .45);
          const nebula = ctx.createRadialGradient(x, y, photonRadius * .55, x, y, photonRadius * 1.28);
          nebula.addColorStop(0, 'rgba(3,12,37,.88)'); nebula.addColorStop(.46, 'rgba(10,31,81,.72)');
          nebula.addColorStop(.64, 'rgba(35,112,251,.48)'); nebula.addColorStop(.82, 'rgba(87,189,255,.2)'); nebula.addColorStop(1, 'rgba(52,116,228,0)');
          ctx.fillStyle = nebula; ctx.fillRect(0, 0, width, height);
          // The bent upper/lower image is behind the card; its text stays clear.
          ctx.save(); ctx.translate(x, y); ctx.scale(1.08, 1);
          for (let rim = 0; rim < 4; rim++) {
            ctx.strokeStyle = ['rgba(32,117,255,.13)', 'rgba(46,155,255,.36)', 'rgba(124,233,255,.66)', 'rgba(225,253,255,.95)'][rim];
            ctx.lineWidth = [22, 9, 3, 1.2][rim]; ctx.beginPath(); ctx.arc(0, 0, photonRadius, 0, Math.PI * 2); ctx.stroke();
          }
          ctx.restore();
          for (let star = 0; star < 76; star++) {
            const angle = star * 2.39996 + time * (.04 + star % 3 * .01), r = photonRadius * (1.04 + star % 9 * .026);
            ctx.fillStyle = star % 4 ? 'rgba(75,166,255,.55)' : 'rgba(211,252,255,.9)';
            ctx.fillRect(x + Math.cos(angle) * r * 1.08, y + Math.sin(angle) * r, star % 4 ? 1 : 1.7, star % 4 ? 1 : 1.7);
          }
        }
        ctx.save(); ctx.translate(x, y + height * .045); ctx.rotate(-12 * Math.PI / 180); ctx.scale(1, .34);
        const radius = width * .82;
        ctx.beginPath(); ctx.rect(-radius * 1.2, layer ? 0 : -radius * 1.2, radius * 2.4, radius * 1.2); ctx.clip();
        ctx.rotate(time * .85); ctx.drawImage(disk.current!, -radius, -radius, radius * 2, radius * 2); ctx.restore();
      }
      frames++; if (frames % 10 === 0) for (const canvas of canvases) canvas.dataset.frames = String(frames);
      frame = requestAnimationFrame(render);
    };
    frame = requestAnimationFrame(render);
    return () => { cancelAnimationFrame(frame); observer.disconnect(); };
  }, [active]);
  return <><canvas ref={back} className="draw-galaxy draw-galaxy-back" aria-hidden="true" /><canvas ref={front} className="draw-galaxy draw-galaxy-front" aria-hidden="true" /></>;
}
