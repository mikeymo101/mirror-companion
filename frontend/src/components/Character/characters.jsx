/**
 * SVG character designs — simple, round, cartoon blob-style.
 * Inspired by Rudi (Grok) — minimal features, personality through animation.
 * Each accepts a `state` prop for CSS animation class.
 */

export function FoxCharacter({ state }) {
  return (
    <svg viewBox="0 0 200 200" className={`char-svg char-svg--${state}`}>
      <defs>
        <radialGradient id="foxGlow" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stopColor="#fb923c" stopOpacity="0.3" />
          <stop offset="100%" stopColor="#f97316" stopOpacity="0" />
        </radialGradient>
      </defs>
      {/* Ambient glow */}
      <circle cx="100" cy="105" r="75" fill="url(#foxGlow)" className="char-glow" />
      {/* Tail */}
      <ellipse cx="148" cy="118" rx="22" ry="12" fill="#f97316" transform="rotate(-30 148 118)" className="char-tail" />
      <ellipse cx="155" cy="110" rx="8" ry="5" fill="#fff7ed" transform="rotate(-30 155 110)" className="char-tail" />
      {/* Body — one round blob */}
      <ellipse cx="100" cy="115" rx="52" ry="48" fill="#f97316" className="char-body" />
      {/* Belly */}
      <ellipse cx="100" cy="125" rx="32" ry="28" fill="#fed7aa" />
      {/* Ears */}
      <polygon points="65,72 52,38 80,62" fill="#f97316" className="char-ear-l" />
      <polygon points="135,72 148,38 120,62" fill="#f97316" className="char-ear-r" />
      <polygon points="67,70 58,46 78,63" fill="#fed7aa" />
      <polygon points="133,70 142,46 122,63" fill="#fed7aa" />
      {/* Eyes */}
      <g className="char-eyes">
        <circle cx="82" cy="95" r="8" fill="white" />
        <circle cx="118" cy="95" r="8" fill="white" />
        <circle cx="84" cy="95" r="5" fill="#1e1e1e" className="char-pupil" />
        <circle cx="120" cy="95" r="5" fill="#1e1e1e" className="char-pupil" />
        <circle cx="86" cy="93" r="2" fill="white" />
        <circle cx="122" cy="93" r="2" fill="white" />
      </g>
      {/* Nose */}
      <ellipse cx="100" cy="105" rx="5" ry="3.5" fill="#1e1e1e" />
      {/* Mouth */}
      <path d="M 93 110 Q 100 117 107 110" fill="none" stroke="#1e1e1e" strokeWidth="2" strokeLinecap="round" className="char-mouth" />
    </svg>
  );
}

export function BunnyCharacter({ state }) {
  return (
    <svg viewBox="0 0 200 200" className={`char-svg char-svg--${state}`}>
      <defs>
        <radialGradient id="bunnyGlow" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stopColor="#f9a8d4" stopOpacity="0.3" />
          <stop offset="100%" stopColor="#ec4899" stopOpacity="0" />
        </radialGradient>
      </defs>
      <circle cx="100" cy="110" r="75" fill="url(#bunnyGlow)" className="char-glow" />
      {/* Long ears */}
      <ellipse cx="72" cy="40" rx="14" ry="38" fill="#f9a8d4" className="char-ear-l" />
      <ellipse cx="128" cy="40" rx="14" ry="38" fill="#f9a8d4" className="char-ear-r" />
      <ellipse cx="72" cy="40" rx="8" ry="30" fill="#fce7f3" />
      <ellipse cx="128" cy="40" rx="8" ry="30" fill="#fce7f3" />
      {/* Body */}
      <ellipse cx="100" cy="118" rx="50" ry="46" fill="#f9a8d4" className="char-body" />
      {/* Belly */}
      <ellipse cx="100" cy="126" rx="30" ry="26" fill="#fce7f3" />
      {/* Cheeks */}
      <circle cx="70" cy="108" r="10" fill="#fda4af" opacity="0.4" />
      <circle cx="130" cy="108" r="10" fill="#fda4af" opacity="0.4" />
      {/* Eyes */}
      <g className="char-eyes">
        <circle cx="82" cy="98" r="9" fill="white" />
        <circle cx="118" cy="98" r="9" fill="white" />
        <circle cx="84" cy="98" r="5.5" fill="#1e1e1e" className="char-pupil" />
        <circle cx="120" cy="98" r="5.5" fill="#1e1e1e" className="char-pupil" />
        <circle cx="86" cy="96" r="2" fill="white" />
        <circle cx="122" cy="96" r="2" fill="white" />
      </g>
      {/* Nose */}
      <ellipse cx="100" cy="108" rx="4" ry="3" fill="#fda4af" />
      {/* Mouth */}
      <path d="M 94 113 Q 100 119 106 113" fill="none" stroke="#1e1e1e" strokeWidth="2" strokeLinecap="round" className="char-mouth" />
    </svg>
  );
}

export function DragonCharacter({ state }) {
  return (
    <svg viewBox="0 0 200 200" className={`char-svg char-svg--${state}`}>
      <defs>
        <radialGradient id="dragonGlow" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stopColor="#a78bfa" stopOpacity="0.35" />
          <stop offset="70%" stopColor="#8b5cf6" stopOpacity="0.1" />
          <stop offset="100%" stopColor="#7c3aed" stopOpacity="0" />
        </radialGradient>
      </defs>
      {/* Ambient glow */}
      <circle cx="100" cy="105" r="80" fill="url(#dragonGlow)" className="char-glow" />
      {/* Little wings */}
      <ellipse cx="48" cy="100" rx="20" ry="28" fill="#c084fc" opacity="0.8" transform="rotate(15 48 100)" className="char-wing-l" />
      <ellipse cx="152" cy="100" rx="20" ry="28" fill="#c084fc" opacity="0.8" transform="rotate(-15 152 100)" className="char-wing-r" />
      {/* Tail */}
      <path d="M 60 145 Q 38 155 30 145 Q 25 138 35 142" fill="none" stroke="#8b5cf6" strokeWidth="7" strokeLinecap="round" className="char-tail" />
      {/* Body — big round blob */}
      <ellipse cx="100" cy="115" rx="50" ry="46" fill="#8b5cf6" className="char-body" />
      {/* Belly */}
      <ellipse cx="100" cy="124" rx="30" ry="26" fill="#ddd6fe" />
      {/* Head spikes */}
      <circle cx="76" cy="72" r="7" fill="#a78bfa" className="char-spike" />
      <circle cx="100" cy="64" r="8" fill="#a78bfa" className="char-spike" />
      <circle cx="124" cy="72" r="7" fill="#a78bfa" className="char-spike" />
      {/* Eyes — big and expressive */}
      <g className="char-eyes">
        <circle cx="82" cy="95" r="11" fill="white" />
        <circle cx="118" cy="95" r="11" fill="white" />
        <circle cx="85" cy="95" r="7" fill="#1e1e1e" className="char-pupil" />
        <circle cx="121" cy="95" r="7" fill="#1e1e1e" className="char-pupil" />
        <circle cx="87" cy="92" r="3" fill="white" />
        <circle cx="123" cy="92" r="3" fill="white" />
      </g>
      {/* Snout */}
      <ellipse cx="100" cy="110" rx="14" ry="9" fill="#a78bfa" />
      {/* Nostrils */}
      <circle cx="95" cy="109" r="2.5" fill="#7c3aed" />
      <circle cx="105" cy="109" r="2.5" fill="#7c3aed" />
      {/* Smile */}
      <path d="M 91 115 Q 100 123 109 115" fill="none" stroke="#1e1e1e" strokeWidth="2" strokeLinecap="round" className="char-mouth" />
      {/* Sparkles */}
      <circle cx="160" cy="70" r="3" fill="#fbbf24" className="char-sparkle" />
      <circle cx="38" cy="82" r="2.5" fill="#fbbf24" className="char-sparkle char-sparkle-2" />
      <circle cx="165" cy="135" r="2" fill="#c084fc" className="char-sparkle char-sparkle-3" />
    </svg>
  );
}

export function CatCharacter({ state }) {
  return (
    <svg viewBox="0 0 200 200" className={`char-svg char-svg--${state}`}>
      <defs>
        <radialGradient id="catGlow" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stopColor="#22d3ee" stopOpacity="0.3" />
          <stop offset="100%" stopColor="#06b6d4" stopOpacity="0" />
        </radialGradient>
      </defs>
      <circle cx="100" cy="105" r="75" fill="url(#catGlow)" className="char-glow" />
      {/* Tail */}
      <path d="M 148 130 Q 170 115 168 95 Q 167 88 162 93" fill="none" stroke="#06b6d4" strokeWidth="7" strokeLinecap="round" className="char-tail" />
      {/* Body */}
      <ellipse cx="100" cy="118" rx="50" ry="46" fill="#06b6d4" className="char-body" />
      {/* Belly */}
      <ellipse cx="100" cy="128" rx="30" ry="26" fill="#cffafe" />
      {/* Ears */}
      <polygon points="63,72 50,32 82,62" fill="#06b6d4" className="char-ear-l" />
      <polygon points="137,72 150,32 118,62" fill="#06b6d4" className="char-ear-r" />
      <polygon points="66,70 56,42 80,63" fill="#cffafe" />
      <polygon points="134,70 144,42 120,63" fill="#cffafe" />
      {/* Eyes */}
      <g className="char-eyes">
        <circle cx="82" cy="95" r="9" fill="white" />
        <circle cx="118" cy="95" r="9" fill="white" />
        <ellipse cx="84" cy="95" rx="5" ry="6" fill="#1e1e1e" className="char-pupil" />
        <ellipse cx="120" cy="95" rx="5" ry="6" fill="#1e1e1e" className="char-pupil" />
        <circle cx="86" cy="93" r="2" fill="white" />
        <circle cx="122" cy="93" r="2" fill="white" />
      </g>
      {/* Nose */}
      <polygon points="97,105 103,105 100,109" fill="#f9a8d4" />
      {/* Mouth — cat W shape */}
      <path d="M 92 111 Q 96 115 100 111 Q 104 115 108 111" fill="none" stroke="#1e1e1e" strokeWidth="2" strokeLinecap="round" className="char-mouth" />
      {/* Whiskers */}
      <line x1="60" y1="102" x2="78" y2="106" stroke="#67e8f9" strokeWidth="1.5" opacity="0.6" className="char-whisker" />
      <line x1="60" y1="112" x2="78" y2="110" stroke="#67e8f9" strokeWidth="1.5" opacity="0.6" className="char-whisker" />
      <line x1="140" y1="102" x2="122" y2="106" stroke="#67e8f9" strokeWidth="1.5" opacity="0.6" className="char-whisker" />
      <line x1="140" y1="112" x2="122" y2="110" stroke="#67e8f9" strokeWidth="1.5" opacity="0.6" className="char-whisker" />
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
