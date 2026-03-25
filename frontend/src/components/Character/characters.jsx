/**
 * SVG character designs — cute cartoon style.
 * Dragon/Dino has talking mouth, arm gestures, body movement.
 */

export function DragonCharacter({ state }) {
  const isTalking = state === 'talking';
  const isHappy = state === 'happy';
  const isSleepy = state === 'sleepy';
  const isListening = state === 'listening';

  return (
    <svg viewBox="0 0 200 240" className={`char-svg char-svg--${state}`}>
      <defs>
        <radialGradient id="dinoGlow" cx="50%" cy="45%" r="50%">
          <stop offset="0%" stopColor="#7cbee7" stopOpacity="0.2" />
          <stop offset="100%" stopColor="#2589cf" stopOpacity="0" />
        </radialGradient>
      </defs>

      {/* Ambient glow */}
      <circle cx="100" cy="120" r="95" fill="url(#dinoGlow)" className="char-glow" />

      {/* --- TAIL --- chunky dino tail */}
      <g className="char-tail">
        <path d="M 145 170 Q 175 165, 185 150 Q 190 140, 183 145"
          fill="#7cbee7" stroke="none" />
        <ellipse cx="185" cy="145" rx="6" ry="5" fill="#2589cf" />
      </g>

      {/* --- FEET --- big stompy dino feet */}
      <g className="char-foot-l">
        <ellipse cx="78" cy="218" rx="18" ry="9" fill="#2589cf" />
        {/* Toes */}
        <circle cx="66" cy="216" r="4" fill="#2589cf" />
        <circle cx="74" cy="213" r="4" fill="#2589cf" />
        <circle cx="82" cy="212" r="4" fill="#2589cf" />
      </g>
      <g className="char-foot-r">
        <ellipse cx="122" cy="218" rx="18" ry="9" fill="#2589cf" />
        <circle cx="118" cy="212" r="4" fill="#2589cf" />
        <circle cx="126" cy="213" r="4" fill="#2589cf" />
        <circle cx="134" cy="216" r="4" fill="#2589cf" />
      </g>

      {/* --- LEGS --- */}
      <rect x="70" y="195" width="18" height="25" rx="8" fill="#7cbee7" className="char-leg-l" />
      <rect x="112" y="195" width="18" height="25" rx="8" fill="#7cbee7" className="char-leg-r" />

      {/* --- BODY --- big round dino belly */}
      <ellipse cx="100" cy="155" rx="55" ry="52" fill="#7cbee7" className="char-body" />
      {/* Belly */}
      <ellipse cx="100" cy="163" rx="35" ry="33" fill="#c1e4f9" />

      {/* --- ARMS --- little T-rex arms! */}
      <g className="char-arm-l">
        <ellipse cx="50" cy="140" rx="12" ry="7" fill="#7cbee7" transform="rotate(-25 50 140)" />
        {/* Little claws */}
        <circle cx="40" cy="137" r="3" fill="#2589cf" />
        <circle cx="43" cy="133" r="3" fill="#2589cf" />
      </g>
      <g className="char-arm-r">
        <ellipse cx="150" cy="140" rx="12" ry="7" fill="#7cbee7" transform="rotate(25 150 140)" />
        <circle cx="160" cy="137" r="3" fill="#2589cf" />
        <circle cx="157" cy="133" r="3" fill="#2589cf" />
      </g>

      {/* --- HEAD --- big round head */}
      <circle cx="100" cy="90" r="45" fill="#7cbee7" className="char-head" />

      {/* Back spikes on head */}
      <g className="char-spikes">
        <ellipse cx="68" cy="55" rx="6" ry="11" fill="#f7921e" transform="rotate(-15 68 55)" />
        <ellipse cx="88" cy="44" rx="6" ry="13" fill="#f7921e" transform="rotate(-5 88 44)" />
        <ellipse cx="110" cy="42" rx="6" ry="14" fill="#f7921e" />
        <ellipse cx="130" cy="48" rx="6" ry="12" fill="#f7921e" transform="rotate(10 130 48)" />
      </g>

      {/* --- EYES --- big cartoon eyes */}
      <g className="char-eyes">
        {/* Eye whites */}
        <ellipse cx="80" cy="85" rx="15" ry={isSleepy ? 5 : isHappy ? 10 : 16} fill="white" />
        <ellipse cx="120" cy="85" rx="15" ry={isSleepy ? 5 : isHappy ? 10 : 16} fill="white" />

        {!isSleepy && !isHappy && (
          <>
            {/* Pupils */}
            <circle cx={isListening ? 83 : 82} cy="87" r="8" fill="#231f1c" className="char-pupil" />
            <circle cx={isListening ? 123 : 122} cy="87" r="8" fill="#231f1c" className="char-pupil" />
            {/* Eye shine */}
            <circle cx="86" cy="83" r="3.5" fill="white" opacity="0.9" />
            <circle cx="126" cy="83" r="3.5" fill="white" opacity="0.9" />
            {/* Small secondary shine */}
            <circle cx="79" cy="90" r="1.5" fill="white" opacity="0.5" />
            <circle cx="119" cy="90" r="1.5" fill="white" opacity="0.5" />
          </>
        )}

        {/* Happy eyes — curved U shapes */}
        {isHappy && (
          <>
            <path d="M 68 83 Q 80 73, 92 83" fill="none" stroke="#231f1c" strokeWidth="3.5" strokeLinecap="round" />
            <path d="M 108 83 Q 120 73, 132 83" fill="none" stroke="#231f1c" strokeWidth="3.5" strokeLinecap="round" />
          </>
        )}

        {/* Sleepy — tiny lines */}
        {isSleepy && (
          <>
            <line x1="70" y1="85" x2="90" y2="85" stroke="#231f1c" strokeWidth="2.5" strokeLinecap="round" />
            <line x1="110" y1="85" x2="130" y2="85" stroke="#231f1c" strokeWidth="2.5" strokeLinecap="round" />
          </>
        )}
      </g>

      {/* --- SNOUT / NOSE AREA --- */}
      <ellipse cx="100" cy="105" rx="18" ry="11" fill="#c1e4f9" />
      {/* Nostrils */}
      <circle cx="93" cy="103" r="2.5" fill="#2589cf" />
      <circle cx="107" cy="103" r="2.5" fill="#2589cf" />

      {/* --- MOUTH --- closed */}
      {!isTalking && !isHappy && (
        <path d="M 88 113 Q 100 121, 112 113"
          fill="none" stroke="#231f1c" strokeWidth="2.5" strokeLinecap="round" />
      )}

      {/* --- MOUTH --- open when talking */}
      {isTalking && (
        <g className="char-mouth-open">
          <ellipse cx="100" cy="117" rx="14" ry="10" fill="#231f1c" />
          {/* Upper mouth/teeth area */}
          <ellipse cx="100" cy="113" rx="12" ry="5" fill="#2589cf" />
          {/* Tongue */}
          <ellipse cx="100" cy="122" rx="7" ry="5" fill="#a85a5a" />
          {/* Tiny teeth */}
          <rect x="92" y="112" width="4" height="4" rx="1" fill="white" />
          <rect x="104" y="112" width="4" height="4" rx="1" fill="white" />
        </g>
      )}

      {/* --- MOUTH --- happy big grin */}
      {isHappy && (
        <g>
          <path d="M 83 110 Q 100 128, 117 110"
            fill="#231f1c" stroke="none" />
          <path d="M 85 111 Q 100 115, 115 111"
            fill="#2589cf" stroke="none" />
          <ellipse cx="100" cy="120" rx="6" ry="4" fill="#a85a5a" />
        </g>
      )}

      {/* --- CHEEK BLUSH --- */}
      <circle cx="62" cy="102" r="8" fill="#f7921e" opacity="0.2" />
      <circle cx="138" cy="102" r="8" fill="#f7921e" opacity="0.2" />

      {/* --- SPARKLES --- */}
      <circle cx="165" cy="60" r="3" fill="#ffc849" className="char-sparkle s1" />
      <circle cx="32" cy="70" r="2.5" fill="#ffc849" className="char-sparkle s2" />
      <circle cx="170" cy="130" r="2" fill="#7cbee7" className="char-sparkle s3" />
      <circle cx="28" cy="140" r="2" fill="#7cbee7" className="char-sparkle s4" />
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
      <circle cx="82" cy="95" r="9" fill="white" />
      <circle cx="118" cy="95" r="9" fill="white" />
      <ellipse cx="84" cy="95" rx="5" ry="6" fill="#1e1e1e" className="char-pupil" />
      <ellipse cx="120" cy="95" rx="5" ry="6" fill="#1e1e1e" className="char-pupil" />
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
