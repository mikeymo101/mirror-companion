import { useState, useEffect, useRef } from 'react';
import './ListeningWave.css';

const BAR_COUNT = 24;

export default function ListeningWave({ active = false }) {
  const [bars, setBars] = useState(() => Array(BAR_COUNT).fill(0.1));
  const animFrameRef = useRef(null);
  const activeRef = useRef(active);

  useEffect(() => {
    activeRef.current = active;
  }, [active]);

  useEffect(() => {
    if (!active) {
      setBars(Array(BAR_COUNT).fill(0.1));
      return;
    }

    let lastTime = 0;
    const interval = 80; // ms between updates

    const animate = (time) => {
      if (!activeRef.current) return;

      if (time - lastTime > interval) {
        lastTime = time;
        setBars((prev) =>
          prev.map((_, i) => {
            // Create a wave-like pattern with some randomness
            const center = BAR_COUNT / 2;
            const distFromCenter = Math.abs(i - center) / center;
            const base = 1 - distFromCenter * 0.5;
            const random = 0.3 + Math.random() * 0.7;
            return base * random;
          })
        );
      }

      animFrameRef.current = requestAnimationFrame(animate);
    };

    animFrameRef.current = requestAnimationFrame(animate);

    return () => {
      if (animFrameRef.current) {
        cancelAnimationFrame(animFrameRef.current);
      }
    };
  }, [active]);

  return (
    <div className={`listening-wave ${active ? 'listening-wave--active' : ''}`}>
      {bars.map((height, i) => (
        <div
          key={i}
          className="listening-wave__bar"
          style={{
            height: `${Math.max(4, height * 40)}px`,
            opacity: active ? 0.4 + height * 0.6 : 0.15,
          }}
        />
      ))}
    </div>
  );
}
