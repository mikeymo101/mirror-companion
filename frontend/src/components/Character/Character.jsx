import './Character.css';
import CHARACTER_MAP from './characters';

const STATE_CONFIG = {
  idle: {
    className: 'character--idle',
    glowColor: '#6366f1',
    outerGlow: '#818cf8',
  },
  wake_word_detected: {
    className: 'character--wake',
    glowColor: '#8b5cf6',
    outerGlow: '#a78bfa',
  },
  listening: {
    className: 'character--listening',
    glowColor: '#06b6d4',
    outerGlow: '#22d3ee',
  },
  processing: {
    className: 'character--processing',
    glowColor: '#8b5cf6',
    outerGlow: '#a78bfa',
  },
  talking: {
    className: 'character--talking',
    glowColor: '#f472b6',
    outerGlow: '#f9a8d4',
  },
  happy: {
    className: 'character--happy',
    glowColor: '#fbbf24',
    outerGlow: '#fcd34d',
  },
  sleepy: {
    className: 'character--sleepy',
    glowColor: '#4338ca',
    outerGlow: '#6366f1',
  },
};

export default function Character({ state = 'idle', characterType = null }) {
  const config = STATE_CONFIG[state] || STATE_CONFIG.idle;
  const CharacterSVG = characterType ? CHARACTER_MAP[characterType] : null;

  return (
    <div className={`character ${config.className}`}>
      {/* Outer ripple rings */}
      <div className="character__ripple character__ripple--1" />
      <div className="character__ripple character__ripple--2" />
      <div className="character__ripple character__ripple--3" />

      {CharacterSVG ? (
        /* Render actual character SVG */
        <div className="character__avatar">
          <CharacterSVG state={state} />
        </div>
      ) : (
        /* Fallback: orb display */
        <svg
          className="character__orb"
          viewBox="0 0 200 200"
          xmlns="http://www.w3.org/2000/svg"
        >
          <defs>
            <radialGradient id="orbGradient" cx="50%" cy="50%" r="50%">
              <stop offset="0%" stopColor={config.outerGlow} stopOpacity="0.9" />
              <stop offset="50%" stopColor={config.glowColor} stopOpacity="0.6" />
              <stop offset="100%" stopColor={config.glowColor} stopOpacity="0" />
            </radialGradient>
            <filter id="orbGlow">
              <feGaussianBlur stdDeviation="8" result="blur" />
              <feMerge>
                <feMergeNode in="blur" />
                <feMergeNode in="SourceGraphic" />
              </feMerge>
            </filter>
          </defs>
          <circle cx="100" cy="100" r="90" fill="url(#orbGradient)" className="character__glow-bg" />
          <circle cx="100" cy="100" r="45" fill={config.glowColor} opacity="0.3" filter="url(#orbGlow)" className="character__core" />
          <circle cx="100" cy="100" r="20" fill={config.outerGlow} opacity="0.6" className="character__inner" />
        </svg>
      )}
    </div>
  );
}
