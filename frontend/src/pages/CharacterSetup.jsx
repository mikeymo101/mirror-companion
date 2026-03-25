import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import CHARACTER_MAP from '../components/Character/characters';
import './CharacterSetup.css';

export default function CharacterSetup() {
  const navigate = useNavigate();
  const [options, setOptions] = useState([]);
  const [selectedType, setSelectedType] = useState(null);
  const [name, setName] = useState('');
  const [step, setStep] = useState('choose'); // 'choose' | 'name' | 'saving'
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch(`http://${window.location.hostname}:8000/api/character/options`)
      .then((res) => res.json())
      .then((data) => setOptions(data.options || []))
      .catch(() => setError('Could not load characters'));
  }, []);

  const handleSelect = (type) => {
    setSelectedType(type);
    setStep('name');
  };

  const handleSave = async () => {
    if (!name.trim()) return;
    setStep('saving');
    try {
      const option = options.find((o) => o.type === selectedType);
      const res = await fetch(`http://${window.location.hostname}:8000/api/character/setup`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: name.trim(),
          type: selectedType,
          personality: option?.personality || `A friendly ${selectedType}`,
        }),
      });
      const data = await res.json();
      if (data.success) {
        navigate('/');
      } else {
        setError('Something went wrong');
        setStep('name');
      }
    } catch {
      setError('Could not save character');
      setStep('name');
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') handleSave();
  };

  const SelectedSVG = selectedType ? CHARACTER_MAP[selectedType] : null;

  return (
    <div className="setup">
      {step === 'choose' && (
        <>
          <h1 className="setup__title">Choose Your Friend!</h1>
          <p className="setup__subtitle">Who would you like to live in the mirror?</p>
          <div className="setup__grid">
            {options.map((opt) => {
              const CharSVG = CHARACTER_MAP[opt.type];
              return (
                <button
                  key={opt.type}
                  className="setup__card"
                  onClick={() => handleSelect(opt.type)}
                  style={{ '--card-color': opt.color }}
                >
                  <div className="setup__card-preview">
                    {CharSVG && <CharSVG state="idle" />}
                  </div>
                  <div className="setup__card-name">{opt.display_name}</div>
                  <div className="setup__card-desc">{opt.description}</div>
                </button>
              );
            })}
          </div>
        </>
      )}

      {step === 'name' && (
        <div className="setup__naming">
          <div className="setup__naming-preview">
            {SelectedSVG && <SelectedSVG state="happy" />}
          </div>
          <h1 className="setup__title">What's their name?</h1>
          <input
            className="setup__input"
            type="text"
            placeholder="Type a name..."
            value={name}
            onChange={(e) => setName(e.target.value)}
            onKeyDown={handleKeyDown}
            autoFocus
            maxLength={20}
          />
          <div className="setup__buttons">
            <button className="setup__btn setup__btn--back" onClick={() => setStep('choose')}>
              Back
            </button>
            <button
              className="setup__btn setup__btn--go"
              onClick={handleSave}
              disabled={!name.trim()}
            >
              Let's Go!
            </button>
          </div>
        </div>
      )}

      {step === 'saving' && (
        <div className="setup__saving">
          <div className="setup__naming-preview">
            {SelectedSVG && <SelectedSVG state="happy" />}
          </div>
          <h1 className="setup__title">{name} is getting ready...</h1>
        </div>
      )}

      {error && <div className="setup__error">{error}</div>}
    </div>
  );
}
