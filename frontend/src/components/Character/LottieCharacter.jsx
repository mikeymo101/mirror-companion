import { useRef, useEffect, useMemo } from 'react';
import Lottie from 'lottie-react';

/**
 * Lottie-based character — plays a Lottie animation with speed/behavior
 * adjusted per voice state. Drop a .json file in assets/animations/
 * and import it here.
 */

// Speed config per state — controls how the animation feels
const STATE_SPEEDS = {
  idle: 0.6,
  wake_word_detected: 1.5,
  listening: 0.8,
  processing: 1.2,
  talking: 1.0,
  happy: 1.8,
  sleepy: 0.3,
};

export default function LottieCharacter({ state = 'idle', animationData }) {
  const lottieRef = useRef(null);

  const speed = STATE_SPEEDS[state] || 0.6;

  // Adjust playback speed when state changes
  useEffect(() => {
    if (lottieRef.current) {
      lottieRef.current.setSpeed(speed);
    }
  }, [speed]);

  // Wrapper class for CSS effects per state
  const wrapperClass = useMemo(() => {
    const base = 'lottie-character';
    const stateClass = `lottie-character--${state}`;
    return `${base} ${stateClass}`;
  }, [state]);

  if (!animationData) return null;

  return (
    <div className={wrapperClass}>
      <Lottie
        lottieRef={lottieRef}
        animationData={animationData}
        loop
        autoplay
        style={{ width: '100%', height: '100%' }}
      />
    </div>
  );
}
