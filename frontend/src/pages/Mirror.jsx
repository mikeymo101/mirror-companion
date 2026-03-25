import { useMemo } from 'react';
import Character from '../components/Character/Character';
import ListeningWave from '../components/ListeningWave/ListeningWave';
import Clock from '../components/Clock/Clock';
import useVoice from '../hooks/useVoice';
import './Mirror.css';

const STATUS_TEXT = {
  idle: null,
  wake_word_detected: 'Mirror Mirror...',
  listening: 'Listening...',
  processing: 'Thinking...',
  talking: '',
};

export default function Mirror({ character }) {
  const {
    currentState,
    transcript,
    response,
    error,
    isConnected,
    simulateInteraction,
    VOICE_STATES,
  } = useVoice();

  const characterState = useMemo(() => {
    switch (currentState) {
      case VOICE_STATES.WAKE_WORD_DETECTED:
        return 'wake_word_detected';
      case VOICE_STATES.LISTENING:
        return 'listening';
      case VOICE_STATES.PROCESSING:
        return 'processing';
      case VOICE_STATES.TALKING:
        return 'talking';
      default:
        return 'idle';
    }
  }, [currentState, VOICE_STATES]);

  const statusText = STATUS_TEXT[characterState];
  const isListening = currentState === VOICE_STATES.LISTENING;
  const isTalking = currentState === VOICE_STATES.TALKING;

  return (
    <div className="mirror" onClick={simulateInteraction}>
      {/* Clock at top */}
      <div className="mirror__clock">
        <Clock />
      </div>

      {/* Main content area */}
      <div className="mirror__center">
        {/* Character */}
        <Character state={characterState} characterType={character?.type} />

        {/* Character name */}
        {character?.name && characterState === 'idle' && (
          <div className="mirror__character-name">{character.name}</div>
        )}

        {/* Listening wave visualization */}
        <div className="mirror__wave">
          <ListeningWave active={isListening} />
        </div>

        {/* Transcript display */}
        {transcript && (currentState === VOICE_STATES.PROCESSING || isTalking) && (
          <div className="mirror__transcript">
            "{transcript}"
          </div>
        )}

        {/* Response display */}
        {response && isTalking && (
          <div className="mirror__response">
            {response}
          </div>
        )}

        {/* Status text */}
        {statusText && (
          <div className={`mirror__status ${characterState !== 'idle' ? 'mirror__status--active' : ''}`}>
            {statusText}
          </div>
        )}
      </div>

      {/* Connection indicator */}
      {!isConnected && (
        <div className="mirror__connection">
          <span className="mirror__connection-dot" />
          Offline — hold Space to test
        </div>
      )}

      {/* Error display */}
      {error && (
        <div className="mirror__error">
          {error}
        </div>
      )}

      {/* Spacebar hint */}
      <div className="mirror__hint">
        Hold Space to talk
      </div>
    </div>
  );
}
