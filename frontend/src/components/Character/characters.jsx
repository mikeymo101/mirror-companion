/**
 * SVG character designs — fox, bunny, dragon, cat.
 * Each accepts a `state` prop for animation class.
 * Body parts have individual animation classes for richer movement.
 */

export function FoxCharacter({ state }) {
  return (
    <svg viewBox="0 0 200 200" className={`char-svg char-svg--${state}`}>
      {/* Glow behind character */}
      <circle cx="100" cy="110" r="80" fill="url(#foxGlow)" className="char-glow" />
      <defs>
        <radialGradient id="foxGlow">
          <stop offset="0%" stopColor="#f97316" stopOpacity="0.15" />
          <stop offset="100%" stopColor="#f97316" stopOpacity="0" />
        </radialGradient>
      </defs>
      {/* Tail */}
      <path d="M 140 140 Q 170 120 165 95 Q 162 85 155 90" fill="#f97316" stroke="none" className="char-tail" />
      <path d="M 165 95 Q 162 85 155 90" fill="white" stroke="none" className="char-tail" />
      {/* Body */}
      <ellipse cx="100" cy="130" rx="45" ry="40" fill="#f97316" />
      {/* Belly */}
      <ellipse cx="100" cy="138" rx="28" ry="25" fill="#fed7aa" />
      {/* Head */}
      <circle cx="100" cy="80" r="35" fill="#f97316" className="char-head" />
      {/* Ears */}
      <polygon points="72,55 60,20 85,45" fill="#f97316" className="char-ear-left" />
      <polygon points="128,55 140,20 115,45" fill="#f97316" className="char-ear-right" />
      <polygon points="74,52 66,28 84,46" fill="#fed7aa" className="char-ear-left" />
      <polygon points="126,52 134,28 116,46" fill="#fed7aa" className="char-ear-right" />
      {/* Face */}
      <ellipse cx="100" cy="88" rx="18" ry="12" fill="#fed7aa" />
      {/* Eyes */}
      <circle cx="86" cy="75" r="5" fill="#1e1e1e" className="char-eye" />
      <circle cx="114" cy="75" r="5" fill="#1e1e1e" className="char-eye" />
      <circle cx="87.5" cy="73.5" r="1.5" fill="white" className="char-eye-shine" />
      <circle cx="115.5" cy="73.5" r="1.5" fill="white" className="char-eye-shine" />
      {/* Nose */}
      <ellipse cx="100" cy="85" rx="4" ry="3" fill="#1e1e1e" />
      {/* Mouth */}
      <path d="M 94 90 Q 100 96 106 90" fill="none" stroke="#1e1e1e" strokeWidth="1.5" className="char-mouth" />
      {/* Paws */}
      <ellipse cx="78" cy="168" rx="12" ry="7" fill="#f97316" className="char-paw-left" />
      <ellipse cx="122" cy="168" rx="12" ry="7" fill="#f97316" className="char-paw-right" />
    </svg>
  );
}

export function BunnyCharacter({ state }) {
  return (
    <svg viewBox="0 0 200 200" className={`char-svg char-svg--${state}`}>
      {/* Glow */}
      <circle cx="100" cy="110" r="80" fill="url(#bunnyGlow)" className="char-glow" />
      <defs>
        <radialGradient id="bunnyGlow">
          <stop offset="0%" stopColor="#f9a8d4" stopOpacity="0.15" />
          <stop offset="100%" stopColor="#f9a8d4" stopOpacity="0" />
        </radialGradient>
      </defs>
      {/* Long ears */}
      <ellipse cx="78" cy="30" rx="12" ry="35" fill="#f9a8d4" className="char-ear-left" />
      <ellipse cx="122" cy="30" rx="12" ry="35" fill="#f9a8d4" className="char-ear-right" />
      <ellipse cx="78" cy="30" rx="7" ry="28" fill="#fce7f3" className="char-ear-left" />
      <ellipse cx="122" cy="30" rx="7" ry="28" fill="#fce7f3" className="char-ear-right" />
      {/* Body */}
      <ellipse cx="100" cy="140" rx="42" ry="38" fill="#f9a8d4" />
      {/* Belly */}
      <ellipse cx="100" cy="145" rx="26" ry="24" fill="#fce7f3" />
      {/* Head */}
      <circle cx="100" cy="85" r="35" fill="#f9a8d4" className="char-head" />
      {/* Cheeks */}
      <circle cx="75" cy="90" r="8" fill="#fda4af" opacity="0.5" className="char-cheek" />
      <circle cx="125" cy="90" r="8" fill="#fda4af" opacity="0.5" className="char-cheek" />
      {/* Eyes */}
      <circle cx="86" cy="80" r="5" fill="#1e1e1e" className="char-eye" />
      <circle cx="114" cy="80" r="5" fill="#1e1e1e" className="char-eye" />
      <circle cx="87.5" cy="78.5" r="1.5" fill="white" className="char-eye-shine" />
      <circle cx="115.5" cy="78.5" r="1.5" fill="white" className="char-eye-shine" />
      {/* Nose */}
      <ellipse cx="100" cy="90" rx="4" ry="3" fill="#fda4af" />
      {/* Mouth */}
      <path d="M 95 94 Q 100 99 105 94" fill="none" stroke="#1e1e1e" strokeWidth="1.5" className="char-mouth" />
      {/* Whiskers */}
      <g className="char-whiskers">
        <line x1="70" y1="88" x2="85" y2="90" stroke="#d1d5db" strokeWidth="1" />
        <line x1="70" y1="93" x2="85" y2="93" stroke="#d1d5db" strokeWidth="1" />
        <line x1="115" y1="90" x2="130" y2="88" stroke="#d1d5db" strokeWidth="1" />
        <line x1="115" y1="93" x2="130" y2="93" stroke="#d1d5db" strokeWidth="1" />
      </g>
      {/* Feet */}
      <ellipse cx="82" cy="175" rx="14" ry="8" fill="#f9a8d4" className="char-paw-left" />
      <ellipse cx="118" cy="175" rx="14" ry="8" fill="#f9a8d4" className="char-paw-right" />
    </svg>
  );
}

export function DragonCharacter({ state }) {
  return (
    <svg viewBox="0 0 200 200" className={`char-svg char-svg--${state}`}>
      {/* Glow behind dragon */}
      <circle cx="100" cy="110" r="90" fill="url(#dragonGlow)" className="char-glow" />
      <defs>
        <radialGradient id="dragonGlow">
          <stop offset="0%" stopColor="#8b5cf6" stopOpacity="0.2" />
          <stop offset="60%" stopColor="#c084fc" stopOpacity="0.08" />
          <stop offset="100%" stopColor="#8b5cf6" stopOpacity="0" />
        </radialGradient>
      </defs>
      {/* Left wing */}
      <g className="char-wing-left">
        <path d="M 55 110 Q 20 80 30 60 Q 40 70 50 75 Q 35 55 40 40 Q 50 55 60 65 Q 50 45 55 30 Q 62 50 68 70 L 68 110 Z" fill="#c084fc" opacity="0.7" />
      </g>
      {/* Right wing */}
      <g className="char-wing-right">
        <path d="M 145 110 Q 180 80 170 60 Q 160 70 150 75 Q 165 55 160 40 Q 150 55 140 65 Q 150 45 145 30 Q 138 50 132 70 L 132 110 Z" fill="#c084fc" opacity="0.7" />
      </g>
      {/* Tail */}
      <path d="M 60 155 Q 35 170 25 155 Q 18 142 30 148 Q 22 135 30 138" fill="none" stroke="#8b5cf6" strokeWidth="6" strokeLinecap="round" className="char-tail" />
      <circle cx="25" cy="150" r="3" fill="#c084fc" className="char-tail-tip" />
      {/* Body */}
      <ellipse cx="100" cy="135" rx="40" ry="38" fill="#8b5cf6" />
      {/* Belly scales */}
      <ellipse cx="100" cy="142" rx="25" ry="24" fill="#ddd6fe" />
      <path d="M 85 130 Q 90 126 95 130" fill="none" stroke="#c4b5fd" strokeWidth="0.8" opacity="0.5" />
      <path d="M 95 130 Q 100 126 105 130" fill="none" stroke="#c4b5fd" strokeWidth="0.8" opacity="0.5" />
      <path d="M 105 130 Q 110 126 115 130" fill="none" stroke="#c4b5fd" strokeWidth="0.8" opacity="0.5" />
      {/* Head */}
      <circle cx="100" cy="82" r="33" fill="#8b5cf6" className="char-head" />
      {/* Head spikes */}
      <g className="char-spikes">
        <ellipse cx="78" cy="53" rx="5" ry="7" fill="#a78bfa" />
        <ellipse cx="100" cy="46" rx="5" ry="8" fill="#a78bfa" />
        <ellipse cx="122" cy="53" rx="5" ry="7" fill="#a78bfa" />
      </g>
      {/* Eyes */}
      <g className="char-eyes">
        <circle cx="86" cy="78" r="7" fill="white" opacity="0.9" />
        <circle cx="114" cy="78" r="7" fill="white" opacity="0.9" />
        <circle cx="86" cy="78" r="5" fill="#1e1e1e" className="char-eye" />
        <circle cx="114" cy="78" r="5" fill="#1e1e1e" className="char-eye" />
        <circle cx="88" cy="76" r="2" fill="white" className="char-eye-shine" />
        <circle cx="116" cy="76" r="2" fill="white" className="char-eye-shine" />
      </g>
      {/* Snout */}
      <ellipse cx="100" cy="93" rx="12" ry="8" fill="#a78bfa" />
      {/* Nostrils with smoke puffs */}
      <circle cx="95" cy="92" r="2.5" fill="#7c3aed" />
      <circle cx="105" cy="92" r="2.5" fill="#7c3aed" />
      <circle cx="92" cy="88" r="2" fill="rgba(200,200,255,0.15)" className="char-smoke char-smoke-1" />
      <circle cx="108" cy="87" r="1.5" fill="rgba(200,200,255,0.15)" className="char-smoke char-smoke-2" />
      {/* Smile */}
      <path d="M 92 97 Q 100 104 108 97" fill="none" stroke="#1e1e1e" strokeWidth="1.5" className="char-mouth" />
      {/* Arms/claws */}
      <ellipse cx="68" cy="145" rx="8" ry="5" fill="#7c3aed" className="char-paw-left" />
      <ellipse cx="132" cy="145" rx="8" ry="5" fill="#7c3aed" className="char-paw-right" />
      {/* Sparkles */}
      <circle cx="155" cy="65" r="2.5" fill="#fbbf24" className="char-sparkle char-sparkle-1" />
      <circle cx="40" cy="80" r="2" fill="#fbbf24" className="char-sparkle char-sparkle-2" />
      <circle cx="165" cy="110" r="2" fill="#fbbf24" className="char-sparkle char-sparkle-3" />
      <circle cx="35" cy="120" r="1.5" fill="#fbbf24" className="char-sparkle char-sparkle-4" />
      <circle cx="150" cy="40" r="1.5" fill="#c084fc" className="char-sparkle char-sparkle-5" />
      <circle cx="50" cy="50" r="1.5" fill="#c084fc" className="char-sparkle char-sparkle-6" />
      {/* Fire particles (visible when talking) */}
      <g className="char-fire">
        <circle cx="90" cy="82" r="3" fill="#fbbf24" opacity="0" />
        <circle cx="110" cy="80" r="2.5" fill="#f97316" opacity="0" />
        <circle cx="95" cy="78" r="2" fill="#ef4444" opacity="0" />
        <circle cx="105" cy="76" r="2" fill="#fbbf24" opacity="0" />
      </g>
    </svg>
  );
}

export function CatCharacter({ state }) {
  return (
    <svg viewBox="0 0 200 200" className={`char-svg char-svg--${state}`}>
      {/* Glow */}
      <circle cx="100" cy="110" r="80" fill="url(#catGlow)" className="char-glow" />
      <defs>
        <radialGradient id="catGlow">
          <stop offset="0%" stopColor="#06b6d4" stopOpacity="0.15" />
          <stop offset="100%" stopColor="#06b6d4" stopOpacity="0" />
        </radialGradient>
      </defs>
      {/* Tail */}
      <path d="M 140 150 Q 165 140 170 120 Q 172 110 165 115" fill="none" stroke="#06b6d4" strokeWidth="8" strokeLinecap="round" className="char-tail" />
      {/* Body */}
      <ellipse cx="100" cy="140" rx="42" ry="38" fill="#06b6d4" />
      {/* Belly */}
      <ellipse cx="100" cy="148" rx="26" ry="24" fill="#cffafe" />
      {/* Head */}
      <circle cx="100" cy="82" r="35" fill="#06b6d4" className="char-head" />
      {/* Ears */}
      <polygon points="70,55 58,18 88,48" fill="#06b6d4" className="char-ear-left" />
      <polygon points="130,55 142,18 112,48" fill="#06b6d4" className="char-ear-right" />
      <polygon points="72,52 64,28 86,48" fill="#cffafe" className="char-ear-left" />
      <polygon points="128,52 136,28 114,48" fill="#cffafe" className="char-ear-right" />
      {/* Eyes */}
      <ellipse cx="85" cy="78" rx="5" ry="6" fill="#1e1e1e" className="char-eye" />
      <ellipse cx="115" cy="78" rx="5" ry="6" fill="#1e1e1e" className="char-eye" />
      <circle cx="86.5" cy="76.5" r="1.5" fill="white" className="char-eye-shine" />
      <circle cx="116.5" cy="76.5" r="1.5" fill="white" className="char-eye-shine" />
      {/* Nose */}
      <polygon points="97,88 103,88 100,92" fill="#f9a8d4" />
      {/* Mouth */}
      <path d="M 93 93 Q 96 97 100 93 Q 104 97 107 93" fill="none" stroke="#1e1e1e" strokeWidth="1.5" className="char-mouth" />
      {/* Whiskers */}
      <g className="char-whiskers">
        <line x1="62" y1="85" x2="82" y2="88" stroke="#a5f3fc" strokeWidth="1.5" />
        <line x1="62" y1="92" x2="82" y2="92" stroke="#a5f3fc" strokeWidth="1.5" />
        <line x1="62" y1="99" x2="82" y2="96" stroke="#a5f3fc" strokeWidth="1.5" />
        <line x1="138" y1="85" x2="118" y2="88" stroke="#a5f3fc" strokeWidth="1.5" />
        <line x1="138" y1="92" x2="118" y2="92" stroke="#a5f3fc" strokeWidth="1.5" />
        <line x1="138" y1="99" x2="118" y2="96" stroke="#a5f3fc" strokeWidth="1.5" />
      </g>
      {/* Paws */}
      <ellipse cx="80" cy="175" rx="12" ry="7" fill="#06b6d4" className="char-paw-left" />
      <ellipse cx="120" cy="175" rx="12" ry="7" fill="#06b6d4" className="char-paw-right" />
    </svg>
  );
}

const CHARACTER_MAP = {
  fox: FoxCharacter,
  bunny: BunnyCharacter,
  dragon: DragonCharacter,
  cat: CatCharacter,
};

export default CHARACTER_MAP;
