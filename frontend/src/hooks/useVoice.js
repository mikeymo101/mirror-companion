import { useState, useEffect, useRef, useCallback } from 'react';

const VOICE_STATES = {
  IDLE: 'idle',
  WAKE_WORD_DETECTED: 'wake_word_detected',
  LISTENING: 'listening',
  PROCESSING: 'processing',
  TALKING: 'talking',
};

export default function useVoice() {
  const [currentState, setCurrentState] = useState(VOICE_STATES.IDLE);
  const [transcript, setTranscript] = useState('');
  const [response, setResponse] = useState('');
  const [error, setError] = useState(null);
  const [isConnected, setIsConnected] = useState(false);

  const wsRef = useRef(null);
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  const spaceHeldRef = useRef(false);

  const connectWebSocket = useCallback(() => {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const hostname = window.location.hostname;
    // Connect directly to backend port 8000 for WebSocket (avoids Vite proxy issues)
    const wsUrl = `${protocol}//${hostname}:8000/api/voice/ws`;

    try {
      const ws = new WebSocket(wsUrl);

      ws.onopen = () => {
        setIsConnected(true);
        setError(null);
        console.log('[useVoice] WebSocket connected');
      };

      ws.onmessage = (event) => {
        // Binary message = audio bytes from TTS
        if (event.data instanceof Blob) {
          const url = URL.createObjectURL(event.data);
          const audio = new Audio(url);
          audio.onended = () => {
            URL.revokeObjectURL(url);
            setCurrentState(VOICE_STATES.IDLE);
          };
          audio.play().catch((err) => {
            console.error('[useVoice] Audio playback failed:', err);
            setCurrentState(VOICE_STATES.IDLE);
          });
          return;
        }

        // Text message = JSON
        try {
          const data = JSON.parse(event.data);

          switch (data.type) {
            case 'wake_word':
              setCurrentState(VOICE_STATES.WAKE_WORD_DETECTED);
              setTimeout(() => setCurrentState(VOICE_STATES.LISTENING), 500);
              break;

            case 'transcript':
              setTranscript(data.text);
              setCurrentState(VOICE_STATES.PROCESSING);
              break;

            case 'response':
              setTranscript(data.transcription || '');
              setResponse(data.response_text || data.text || '');
              setCurrentState(VOICE_STATES.TALKING);
              break;

            case 'silence':
              setCurrentState(VOICE_STATES.IDLE);
              break;

            case 'done':
              setCurrentState(VOICE_STATES.IDLE);
              break;

            case 'error':
              setError(data.message);
              setCurrentState(VOICE_STATES.IDLE);
              break;

            default:
              break;
          }
        } catch (err) {
          console.error('[useVoice] Failed to parse message:', err);
        }
      };

      ws.onclose = () => {
        setIsConnected(false);
        console.log('[useVoice] WebSocket disconnected');
        // Reconnect after 3 seconds
        setTimeout(connectWebSocket, 3000);
      };

      ws.onerror = (err) => {
        console.error('[useVoice] WebSocket error:', err);
        setError('Connection error');
      };

      wsRef.current = ws;
    } catch (err) {
      console.error('[useVoice] Failed to connect:', err);
      setError('Failed to connect to server');
      setTimeout(connectWebSocket, 3000);
    }
  }, []);

  const playAudio = useCallback((base64Audio) => {
    try {
      const audioBytes = atob(base64Audio);
      const arrayBuffer = new ArrayBuffer(audioBytes.length);
      const view = new Uint8Array(arrayBuffer);
      for (let i = 0; i < audioBytes.length; i++) {
        view[i] = audioBytes.charCodeAt(i);
      }
      const blob = new Blob([arrayBuffer], { type: 'audio/mp3' });
      const url = URL.createObjectURL(blob);
      const audio = new Audio(url);

      audio.onended = () => {
        URL.revokeObjectURL(url);
        setCurrentState(VOICE_STATES.IDLE);
      };

      audio.play().catch((err) => {
        console.error('[useVoice] Audio playback failed:', err);
        setCurrentState(VOICE_STATES.IDLE);
      });
    } catch (err) {
      console.error('[useVoice] Failed to play audio:', err);
      setCurrentState(VOICE_STATES.IDLE);
    }
  }, []);

  const startListening = useCallback(async () => {
    try {
      setError(null);
      setCurrentState(VOICE_STATES.LISTENING);
      audioChunksRef.current = [];

      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream, {
        mimeType: MediaRecorder.isTypeSupported('audio/webm;codecs=opus')
          ? 'audio/webm;codecs=opus'
          : 'audio/webm',
      });

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };

      mediaRecorder.onstop = () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' });
        sendAudio(audioBlob);
        stream.getTracks().forEach((track) => track.stop());
      };

      mediaRecorder.start(100); // collect data in 100ms chunks
      mediaRecorderRef.current = mediaRecorder;
    } catch (err) {
      console.error('[useVoice] Failed to start recording:', err);
      setError('Microphone access denied');
      setCurrentState(VOICE_STATES.IDLE);
    }
  }, []);

  const stopListening = useCallback(() => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state === 'recording') {
      mediaRecorderRef.current.stop();
      mediaRecorderRef.current = null;
      setCurrentState(VOICE_STATES.PROCESSING);
    }
  }, []);

  const sendAudio = useCallback((audioBlob) => {
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      const reader = new FileReader();
      reader.onloadend = () => {
        const base64 = reader.result.split(',')[1];
        wsRef.current.send(JSON.stringify({
          type: 'audio',
          audio: base64,
        }));
      };
      reader.readAsDataURL(audioBlob);
    } else {
      setError('Not connected to server');
      setCurrentState(VOICE_STATES.IDLE);
    }
  }, []);

  // Spacebar push-to-talk for testing
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.code === 'Space' && !e.repeat && !spaceHeldRef.current) {
        e.preventDefault();
        spaceHeldRef.current = true;
        startListening();
      }
    };

    const handleKeyUp = (e) => {
      if (e.code === 'Space' && spaceHeldRef.current) {
        e.preventDefault();
        spaceHeldRef.current = false;
        stopListening();
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    window.addEventListener('keyup', handleKeyUp);

    return () => {
      window.removeEventListener('keydown', handleKeyDown);
      window.removeEventListener('keyup', handleKeyUp);
    };
  }, [startListening, stopListening]);

  // Connect WebSocket on mount
  useEffect(() => {
    connectWebSocket();

    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, [connectWebSocket]);

  // Simulate state cycle for demo when backend is not connected
  const simulateInteraction = useCallback(() => {
    if (!isConnected) {
      setCurrentState(VOICE_STATES.WAKE_WORD_DETECTED);
      setTimeout(() => setCurrentState(VOICE_STATES.LISTENING), 600);
      setTimeout(() => {
        setTranscript("What's your favorite color?");
        setCurrentState(VOICE_STATES.PROCESSING);
      }, 3000);
      setTimeout(() => {
        setResponse("I love purple! It's the color of magic and dreams.");
        setCurrentState(VOICE_STATES.TALKING);
      }, 4500);
      setTimeout(() => setCurrentState(VOICE_STATES.IDLE), 7000);
    }
  }, [isConnected]);

  return {
    currentState,
    transcript,
    response,
    error,
    isConnected,
    startListening,
    stopListening,
    simulateInteraction,
    VOICE_STATES,
  };
}
