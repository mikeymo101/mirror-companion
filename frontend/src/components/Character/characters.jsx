/**
 * SVG character designs — cute, front-facing, cartoon style.
 * Dragon has separate open/closed mouth for talking animation.
 * Each accepts a `state` prop for CSS animation classes.
 */

export function DragonCharacter({ state }) {
  const isTalking = state === 'talking';
  const isHappy = state === 'happy';
  const isSleepy = state === 'sleepy';

  return (
    <svg viewBox="0 0 200 220" className={`char-svg char-svg--${state}`}>
      <defs>
        <radialGradient id="dragonGlow" cx="50%" cy="45%" r="50%">
          <stop offset="0%" stopColor="#a78bfa" stopOpacity="0.25" />
          <stop offset="100%" stopColor="#7c3aed" stopOpacity="0" />
        </radialGradient>
      </defs>

      {/* Ambient glow */}
      <circle cx="100" cy="110" r="95" fill="url(#dragonGlow)" className="char-glow" />

      {/* --- WINGS --- */}
      <g className="char-wing-l">
        <path d="M 38 95 C 15 70, 10 45, 25 35 C 30 50, 38 60, 45 68 C 30 55, 20 38, 30 25 C 38 42, 48 55, 55 68 L 55 95 Z"
          fill="#c084fc" opacity="0.75" />
      </g>
      <g className="char-wing-r">
        <path d="M 162 95 C 185 70, 190 45, 175 35 C 170 50, 162 60, 155 68 C 170 55, 180 38, 170 25 C 162 42, 152 55, 145 68 L 145 95 Z"
          fill="#c084fc" opacity="0.75" />
      </g>

      {/* --- TAIL --- */}
      <path d="M 55 165 Q 30 180, 20 170 Q 14 160, 25 164"
        fill="none" stroke="#7c3aed" strokeWidth="6" strokeLinecap="round" className="char-tail" />

      {/* --- BODY --- big round belly */}
      <ellipse cx="100" cy="140" rx="52" ry="48" fill="#8b5cf6" />
      {/* Belly patch */}
      <ellipse cx="100" cy="148" rx="32" ry="30" fill="#ddd6fe" />
      {/* Belly lines */}
      <path d="M 88 138 Q 92 134, 96 138" fill="none" stroke="#c4b5fd" strokeWidth="1" opacity="0.6" />
      <path d="M 96 138 Q 100 134, 104 138" fill="none" stroke="#c4b5fd" strokeWidth="1" opacity="0.6" />
      <path d="M 104 138 Q 108 134, 112 138" fill="none" stroke="#c4b5fd" strokeWidth="1" opacity="0.6" />

      {/* --- ARMS --- little stubby arms */}
      <g className="char-arm-l">
        <ellipse cx="56" cy="135" rx="10" ry="6" fill="#7c3aed" transform="rotate(-20 56 135)" />
      </g>
      <g className="char-arm-r">
        <ellipse cx="144" cy="135" rx="10" ry="6" fill="#7c3aed" transform="rotate(20 144 135)" />
      </g>

      {/* --- FEET --- */}
      <ellipse cx="78" cy="185" rx="14" ry="8" fill="#7c3aed" />
      <ellipse cx="122" cy="185" rx="14" ry="8" fill="#7c3aed" />

      {/* --- HEAD --- */}
      <circle cx="100" cy="85" r="40" fill="#8b5cf6" className="char-head" />

      {/* Head spikes */}
      <ellipse cx="72" cy="52" rx="6" ry="10" fill="#a78bfa" transform="rotate(-10 72 52)" />
      <ellipse cx="100" cy="42" rx="6" ry="12" fill="#a78bfa" />
      <ellipse cx="128" cy="52" rx="6" ry="10" fill="#a78bfa" transform="rotate(10 128 52)" />

      {/* --- EYES --- */}
      <g className="char-eyes">
        {/* Eye whites */}
        <ellipse cx="82" cy="82" rx="13" ry={isSleepy ? 4 : 14} fill="white" />
        <ellipse cx="118" cy="82" rx="13" ry={isSleepy ? 4 : 14} fill="white" />

        {/* Pupils — shift with state */}
        {!isSleepy && (
          <>
            <circle cx="85" cy="84" r="7" fill="#1e1e1e" className="char-pupil" />
            <circle cx="121" cy="84" r="7" fill="#1e1e1e" className="char-pupil" />
            {/* Eye shine */}
            <circle cx="88" cy="80" r="3" fill="white" opacity="0.9" />
            <circle cx="124" cy="80" r="3" fill="white" opacity="0.9" />
          </>
        )}

        {/* Happy eyes — curved lines */}
        {isHappy && (
          <>
            <path d="M 72 82 Q 82 72, 92 82" fill="none" stroke="#1e1e1e" strokeWidth="3" strokeLinecap="round" />
            <path d="M 108 82 Q 118 72, 128 82" fill="none" stroke="#1e1e1e" strokeWidth="3" strokeLinecap="round" />
          </>
        )}
      </g>

      {/* --- SNOUT --- */}
      <ellipse cx="100" cy="100" rx="16" ry="10" fill="#a78bfa" />

      {/* Nostrils */}
      <circle cx="93" cy="98" r="2.5" fill="#7c3aed" />
      <circle cx="107" cy="98" r="2.5" fill="#7c3aed" />

      {/* --- MOUTH --- closed (hidden when talking) */}
      {!isTalking && !isHappy && (
        <path d="M 90 107 Q 100 115, 110 107"
          fill="none" stroke="#1e1e1e" strokeWidth="2.5" strokeLinecap="round" className="char-mouth-closed" />
      )}

      {/* --- MOUTH --- open (visible when talking) */}
      {isTalking && (
        <g className="char-mouth-open">
          <ellipse cx="100" cy="112" rx="12" ry="8" fill="#1e1e1e" />
          <ellipse cx="100" cy="109" rx="10" ry="4" fill="#7c3aed" />
          {/* Tongue */}
          <ellipse cx="100" cy="116" rx="6" ry="4" fill="#f472b6" />
        </g>
      )}

      {/* --- MOUTH --- happy big smile */}
      {isHappy && (
        <path d="M 85 105 Q 100 120, 115 105"
          fill="none" stroke="#1e1e1e" strokeWidth="2.5" strokeLinecap="round" />
      )}

      {/* --- SPARKLES --- */}
      <circle cx="160" cy="55" r="3" fill="#fbbf24" className="char-sparkle s1" />
      <circle cx="38" cy="65" r="2.5" fill="#fbbf24" className="char-sparkle s2" />
      <circle cx="168" cy="120" r="2" fill="#c084fc" className="char-sparkle s3" />
      <circle cx="30" cy="130" r="2" fill="#c084fc" className="char-sparkle s4" />
    </svg>
  );
}

export function FoxCharacter({ state }) {
  return (
    <svg viewBox="0 0 200 200" className={`char-svg char-svg--${state}`}>
      <ellipse cx="100" cy="115" rx="52" ry="48" fill="#f97316" />
      <ellipse cx="100" cy="125" rx="32" ry="28" fill="#fed7aa" />
      <polygon points="65,72 52,38 80,62" fill="#f97316" />
      <polygon points="135,72 148,38 120,62" fill="#f97316" />
      <polygon points="67,70 58,46 78,63" fill="#fed7aa" />
      <polygon points="133,70 142,46 122,63" fill="#fed7aa" />
      <circle cx="82" cy="95" r="8" fill="white" />
      <circle cx="118" cy="95" r="8" fill="white" />
      <circle cx="84" cy="95" r="5" fill="#1e1e1e" className="char-pupil" />
      <circle cx="120" cy="95" r="5" fill="#1e1e1e" className="char-pupil" />
      <circle cx="86" cy="93" r="2" fill="white" />
      <circle cx="122" cy="93" r="2" fill="white" />
      <ellipse cx="100" cy="105" rx="5" ry="3.5" fill="#1e1e1e" />
      <path d="M 93 110 Q 100 117 107 110" fill="none" stroke="#1e1e1e" strokeWidth="2" strokeLinecap="round" />
    </svg>
  );
}

export function BunnyCharacter({ state }) {
  return (
    <svg viewBox="0 0 200 200" className={`char-svg char-svg--${state}`}>
      <ellipse cx="72" cy="40" rx="14" ry="38" fill="#f9a8d4" />
      <ellipse cx="128" cy="40" rx="14" ry="38" fill="#f9a8d4" />
      <ellipse cx="72" cy="40" rx="8" ry="30" fill="#fce7f3" />
      <ellipse cx="128" cy="40" rx="8" ry="30" fill="#fce7f3" />
      <ellipse cx="100" cy="118" rx="50" ry="46" fill="#f9a8d4" />
      <ellipse cx="100" cy="126" rx="30" ry="26" fill="#fce7f3" />
      <circle cx="82" cy="98" r="9" fill="white" />
      <circle cx="118" cy="98" r="9" fill="white" />
      <circle cx="84" cy="98" r="5.5" fill="#1e1e1e" className="char-pupil" />
      <circle cx="120" cy="98" r="5.5" fill="#1e1e1e" className="char-pupil" />
      <circle cx="86" cy="96" r="2" fill="white" />
      <circle cx="122" cy="96" r="2" fill="white" />
      <ellipse cx="100" cy="108" rx="4" ry="3" fill="#fda4af" />
      <path d="M 94 113 Q 100 119 106 113" fill="none" stroke="#1e1e1e" strokeWidth="2" strokeLinecap="round" />
    </svg>
  );
}

export function CatCharacter({ state }) {
  return (
    <svg viewBox="0 0 200 200" className={`char-svg char-svg--${state}`}>
      <ellipse cx="100" cy="118" rx="50" ry="46" fill="#06b6d4" />
      <ellipse cx="100" cy="128" rx="30" ry="26" fill="#cffafe" />
      <polygon points="63,72 50,32 82,62" fill="#06b6d4" />
      <polygon points="137,72 150,32 118,62" fill="#06b6d4" />
      <polygon points="66,70 56,42 80,63" fill="#cffafe" />
      <polygon points="134,70 144,42 120,63" fill="#cffafe" />
      <circle cx="82" cy="95" r="9" fill="white" />
      <circle cx="118" cy="95" r="9" fill="white" />
      <ellipse cx="84" cy="95" rx="5" ry="6" fill="#1e1e1e" className="char-pupil" />
      <ellipse cx="120" cy="95" rx="5" ry="6" fill="#1e1e1e" className="char-pupil" />
      <circle cx="86" cy="93" r="2" fill="white" />
      <circle cx="122" cy="93" r="2" fill="white" />
      <polygon points="97,105 103,105 100,109" fill="#f9a8d4" />
      <path d="M 92 111 Q 96 115 100 111 Q 104 115 108 111" fill="none" stroke="#1e1e1e" strokeWidth="2" strokeLinecap="round" />
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
