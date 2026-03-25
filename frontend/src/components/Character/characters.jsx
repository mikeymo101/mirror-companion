/**
 * SVG character designs — fox, bunny, dragon, cat.
 * Each accepts a `state` prop for animation class.
 */

export function FoxCharacter({ state }) {
  return (
    <svg viewBox="0 0 200 200" className={`char-svg char-svg--${state}`}>
      {/* Body */}
      <ellipse cx="100" cy="130" rx="45" ry="40" fill="#f97316" />
      {/* Belly */}
      <ellipse cx="100" cy="138" rx="28" ry="25" fill="#fed7aa" />
      {/* Head */}
      <circle cx="100" cy="80" r="35" fill="#f97316" />
      {/* Ears */}
      <polygon points="72,55 60,20 85,45" fill="#f97316" />
      <polygon points="128,55 140,20 115,45" fill="#f97316" />
      <polygon points="74,52 66,28 84,46" fill="#fed7aa" />
      <polygon points="126,52 134,28 116,46" fill="#fed7aa" />
      {/* Face */}
      <ellipse cx="100" cy="88" rx="18" ry="12" fill="#fed7aa" />
      {/* Eyes */}
      <circle cx="86" cy="75" r="5" fill="#1e1e1e" className="char-eye" />
      <circle cx="114" cy="75" r="5" fill="#1e1e1e" className="char-eye" />
      <circle cx="87.5" cy="73.5" r="1.5" fill="white" />
      <circle cx="115.5" cy="73.5" r="1.5" fill="white" />
      {/* Nose */}
      <ellipse cx="100" cy="85" rx="4" ry="3" fill="#1e1e1e" />
      {/* Mouth */}
      <path d="M 94 90 Q 100 96 106 90" fill="none" stroke="#1e1e1e" strokeWidth="1.5" className="char-mouth" />
      {/* Tail */}
      <path d="M 140 140 Q 170 120 165 95 Q 162 85 155 90" fill="#f97316" stroke="none" />
      <path d="M 165 95 Q 162 85 155 90" fill="white" stroke="none" />
    </svg>
  );
}

export function BunnyCharacter({ state }) {
  return (
    <svg viewBox="0 0 200 200" className={`char-svg char-svg--${state}`}>
      {/* Long ears */}
      <ellipse cx="78" cy="30" rx="12" ry="35" fill="#f9a8d4" />
      <ellipse cx="122" cy="30" rx="12" ry="35" fill="#f9a8d4" />
      <ellipse cx="78" cy="30" rx="7" ry="28" fill="#fce7f3" />
      <ellipse cx="122" cy="30" rx="7" ry="28" fill="#fce7f3" />
      {/* Body */}
      <ellipse cx="100" cy="140" rx="42" ry="38" fill="#f9a8d4" />
      {/* Belly */}
      <ellipse cx="100" cy="145" rx="26" ry="24" fill="#fce7f3" />
      {/* Head */}
      <circle cx="100" cy="85" r="35" fill="#f9a8d4" />
      {/* Cheeks */}
      <circle cx="75" cy="90" r="8" fill="#fda4af" opacity="0.5" />
      <circle cx="125" cy="90" r="8" fill="#fda4af" opacity="0.5" />
      {/* Eyes */}
      <circle cx="86" cy="80" r="5" fill="#1e1e1e" className="char-eye" />
      <circle cx="114" cy="80" r="5" fill="#1e1e1e" className="char-eye" />
      <circle cx="87.5" cy="78.5" r="1.5" fill="white" />
      <circle cx="115.5" cy="78.5" r="1.5" fill="white" />
      {/* Nose */}
      <ellipse cx="100" cy="90" rx="4" ry="3" fill="#fda4af" />
      {/* Mouth */}
      <path d="M 95 94 Q 100 99 105 94" fill="none" stroke="#1e1e1e" strokeWidth="1.5" className="char-mouth" />
      {/* Whiskers */}
      <line x1="70" y1="88" x2="85" y2="90" stroke="#d1d5db" strokeWidth="1" />
      <line x1="70" y1="93" x2="85" y2="93" stroke="#d1d5db" strokeWidth="1" />
      <line x1="115" y1="90" x2="130" y2="88" stroke="#d1d5db" strokeWidth="1" />
      <line x1="115" y1="93" x2="130" y2="93" stroke="#d1d5db" strokeWidth="1" />
      {/* Feet */}
      <ellipse cx="82" cy="175" rx="14" ry="8" fill="#f9a8d4" />
      <ellipse cx="118" cy="175" rx="14" ry="8" fill="#f9a8d4" />
    </svg>
  );
}

export function DragonCharacter({ state }) {
  return (
    <svg viewBox="0 0 200 200" className={`char-svg char-svg--${state}`}>
      {/* Wings */}
      <path d="M 55 110 Q 20 80 30 60 Q 40 70 50 75 Q 35 55 40 40 Q 50 55 60 65 Q 50 45 55 30 Q 62 50 68 70 L 68 110 Z" fill="#c084fc" opacity="0.7" />
      <path d="M 145 110 Q 180 80 170 60 Q 160 70 150 75 Q 165 55 160 40 Q 150 55 140 65 Q 150 45 145 30 Q 138 50 132 70 L 132 110 Z" fill="#c084fc" opacity="0.7" />
      {/* Body */}
      <ellipse cx="100" cy="135" rx="40" ry="38" fill="#8b5cf6" />
      {/* Belly */}
      <ellipse cx="100" cy="142" rx="25" ry="24" fill="#ddd6fe" />
      {/* Head */}
      <circle cx="100" cy="82" r="33" fill="#8b5cf6" />
      {/* Head bumps/horns */}
      <circle cx="78" cy="55" r="6" fill="#a78bfa" />
      <circle cx="100" cy="48" r="6" fill="#a78bfa" />
      <circle cx="122" cy="55" r="6" fill="#a78bfa" />
      {/* Eyes */}
      <circle cx="86" cy="78" r="6" fill="#1e1e1e" className="char-eye" />
      <circle cx="114" cy="78" r="6" fill="#1e1e1e" className="char-eye" />
      <circle cx="88" cy="76" r="2" fill="white" />
      <circle cx="116" cy="76" r="2" fill="white" />
      {/* Snout */}
      <ellipse cx="100" cy="93" rx="12" ry="8" fill="#a78bfa" />
      {/* Nostrils */}
      <circle cx="95" cy="92" r="2" fill="#7c3aed" />
      <circle cx="105" cy="92" r="2" fill="#7c3aed" />
      {/* Smile */}
      <path d="M 92 97 Q 100 104 108 97" fill="none" stroke="#1e1e1e" strokeWidth="1.5" className="char-mouth" />
      {/* Tail */}
      <path d="M 60 155 Q 40 170 35 160 Q 30 150 45 155" fill="#8b5cf6" />
      {/* Little sparkles */}
      <circle cx="155" cy="75" r="2" fill="#fbbf24" className="char-sparkle" opacity="0.8" />
      <circle cx="45" cy="85" r="1.5" fill="#fbbf24" className="char-sparkle" opacity="0.6" />
      <circle cx="160" cy="105" r="1.5" fill="#fbbf24" className="char-sparkle" opacity="0.7" />
    </svg>
  );
}

export function CatCharacter({ state }) {
  return (
    <svg viewBox="0 0 200 200" className={`char-svg char-svg--${state}`}>
      {/* Body */}
      <ellipse cx="100" cy="140" rx="42" ry="38" fill="#06b6d4" />
      {/* Belly */}
      <ellipse cx="100" cy="148" rx="26" ry="24" fill="#cffafe" />
      {/* Head */}
      <circle cx="100" cy="82" r="35" fill="#06b6d4" />
      {/* Ears */}
      <polygon points="70,55 58,18 88,48" fill="#06b6d4" />
      <polygon points="130,55 142,18 112,48" fill="#06b6d4" />
      <polygon points="72,52 64,28 86,48" fill="#cffafe" />
      <polygon points="128,52 136,28 114,48" fill="#cffafe" />
      {/* Eyes */}
      <ellipse cx="85" cy="78" rx="5" ry="6" fill="#1e1e1e" className="char-eye" />
      <ellipse cx="115" cy="78" rx="5" ry="6" fill="#1e1e1e" className="char-eye" />
      <circle cx="86.5" cy="76.5" r="1.5" fill="white" />
      <circle cx="116.5" cy="76.5" r="1.5" fill="white" />
      {/* Nose */}
      <polygon points="97,88 103,88 100,92" fill="#f9a8d4" />
      {/* Mouth */}
      <path d="M 93 93 Q 96 97 100 93 Q 104 97 107 93" fill="none" stroke="#1e1e1e" strokeWidth="1.5" className="char-mouth" />
      {/* Whiskers */}
      <line x1="62" y1="85" x2="82" y2="88" stroke="#a5f3fc" strokeWidth="1.5" />
      <line x1="62" y1="92" x2="82" y2="92" stroke="#a5f3fc" strokeWidth="1.5" />
      <line x1="62" y1="99" x2="82" y2="96" stroke="#a5f3fc" strokeWidth="1.5" />
      <line x1="138" y1="85" x2="118" y2="88" stroke="#a5f3fc" strokeWidth="1.5" />
      <line x1="138" y1="92" x2="118" y2="92" stroke="#a5f3fc" strokeWidth="1.5" />
      <line x1="138" y1="99" x2="118" y2="96" stroke="#a5f3fc" strokeWidth="1.5" />
      {/* Tail */}
      <path d="M 140 150 Q 165 140 170 120 Q 172 110 165 115" fill="none" stroke="#06b6d4" strokeWidth="8" strokeLinecap="round" />
      {/* Paws */}
      <ellipse cx="80" cy="175" rx="12" ry="7" fill="#06b6d4" />
      <ellipse cx="120" cy="175" rx="12" ry="7" fill="#06b6d4" />
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
