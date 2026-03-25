import './Character.css';
import LottieCharacter from './LottieCharacter';
import CHARACTER_MAP from './characters';

// Import Lottie animation files directly — add new ones here
import dragonLottie from '../../assets/animations/dragon.json';

const LOTTIE_MAP = {
  dragon: dragonLottie,
};

const STATE_CONFIG = {
  idle: { className: 'character--idle' },
  wake_word_detected: { className: 'character--wake' },
  listening: { className: 'character--listening' },
  processing: { className: 'character--processing' },
  talking: { className: 'character--talking' },
  happy: { className: 'character--happy' },
  sleepy: { className: 'character--sleepy' },
};

export default function Character({ state = 'idle', characterType = null }) {
  const config = STATE_CONFIG[state] || STATE_CONFIG.idle;
  const lottieData = characterType ? LOTTIE_MAP[characterType] || null : null;

  const CharacterSVG = characterType ? CHARACTER_MAP[characterType] : null;

  return (
    <div className={`character ${config.className}`}>
      {/* Ripple rings */}
      <div className="character__ripple character__ripple--1" />
      <div className="character__ripple character__ripple--2" />
      <div className="character__ripple character__ripple--3" />

      {lottieData ? (
        /* Lottie animation */
        <div className="character__avatar">
          <LottieCharacter state={state} animationData={lottieData} />
        </div>
      ) : CharacterSVG ? (
        /* SVG fallback */
        <div className="character__avatar">
          <CharacterSVG state={state} />
        </div>
      ) : (
        /* Orb fallback */
        <svg className="character__orb" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <radialGradient id="orbGradient" cx="50%" cy="50%" r="50%">
              <stop offset="0%" stopColor="#818cf8" stopOpacity="0.9" />
              <stop offset="50%" stopColor="#6366f1" stopOpacity="0.6" />
              <stop offset="100%" stopColor="#6366f1" stopOpacity="0" />
            </radialGradient>
          </defs>
          <circle cx="100" cy="100" r="90" fill="url(#orbGradient)" />
          <circle cx="100" cy="100" r="45" fill="#6366f1" opacity="0.3" />
          <circle cx="100" cy="100" r="20" fill="#818cf8" opacity="0.6" />
        </svg>
      )}
    </div>
  );
}
