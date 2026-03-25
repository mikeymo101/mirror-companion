import { useState, useEffect, useRef, useCallback } from 'react';

const VOICE_STATES = {
  IDLE: 'idle',
  WAKE_WORD_DETECTED: 'wake_word_detected',
  LISTENING: 'listening',
  PROCESSING: 'processing',
  TALKING: 'talking',
};

// Check if browser supports Web Speech API
// Disabled for now — Chromium on Pi needs Google servers for this, which is unreliable
// Falls back to audio recording + Whisper API instead
const SpeechRecognition = null;
const hasSpeechRecognition = false;

export default function useVoice() {
  const [currentState, setCurrentState] = useState(VOICE_STATES.IDLE);
  const [transcript, setTranscript] = useState('');
  const [response, setResponse] = useState('');
  const [error, setError] = useState(null);
  const [isConnected, setIsConnected] = useState(false);

  const wsRef = useRef(null);
  const recognitionRef = useRef(null);
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  const spaceHeldRef = useRef(false);
  const interimTranscriptRef = useRef('');

  const connectWebSocket = useCallback(() => {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const hostname = window.location.hostname;
    const wsUrl = `${protocol}//${hostname}:8000/api/voice/ws`;

    try {
      const ws = new WebSocket(wsUrl);

      ws.onopen = () => {
        setIsConnected(true);
        setError(null);
        console.log('[useVoice] WebSocket connected');
      };

      ws.onmessage = (event) => {
        // Binary message = TTS audio
        if (event.data instanceof Blob) {
          setCurrentState(VOICE_STATES.TALKING);
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

        // JSON message
        try {
          const data = JSON.parse(event.data);
          switch (data.type) {
            case 'response':
              setTranscript(data.transcription || '');
              setResponse(data.response_text || '');
              break;
            case 'silence':
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

  // Send text directly (skips Whisper — much faster)
  const sendText = useCallback((text) => {
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN && text.trim()) {
      setTranscript(text);
      setCurrentState(VOICE_STATES.PROCESSING);
      wsRef.current.send(JSON.stringify({
        type: 'text',
        text: text.trim(),
      }));
    } else {
      setError('Not connected to server');
      setCurrentState(VOICE_STATES.IDLE);
    }
  }, []);

  // Send audio as fallback (when SpeechRecognition unavailable)
  const sendAudio = useCallback((audioBlob) => {
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      setCurrentState(VOICE_STATES.PROCESSING);
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

  const startListening = useCallback(async () => {
    setError(null);
    setResponse('');
    setCurrentState(VOICE_STATES.LISTENING);
    interimTranscriptRef.current = '';

    // Prefer Web Speech API (instant, free, no API call)
    if (hasSpeechRecognition) {
      try {
        const recognition = new SpeechRecognition();
        recognition.continuous = true;
        recognition.interimResults = true;
        recognition.lang = 'en-US';

        recognition.onresult = (event) => {
          let interim = '';
          let final = '';
          for (let i = event.resultIndex; i < event.results.length; i++) {
            const result = event.results[i];
            if (result.isFinal) {
              final += result[0].transcript;
            } else {
              interim += result[0].transcript;
            }
          }
          if (final) {
            interimTranscriptRef.current += final;
          }
          // Show live transcript
          setTranscript(interimTranscriptRef.current + interim);
        };

        recognition.onerror = (event) => {
          console.error('[useVoice] Speech recognition error:', event.error);
          recognitionRef.current = null;
          if (event.error === 'network' || event.error === 'service-not-allowed' || event.error === 'not-allowed') {
            // Fall back to audio recording
            console.log('[useVoice] Falling back to audio recording');
            startAudioRecording();
          } else if (event.error !== 'aborted') {
            setError(`Speech recognition: ${event.error}`);
            setCurrentState(VOICE_STATES.IDLE);
          }
        };

        recognition.start();
        recognitionRef.current = recognition;
      } catch (err) {
        console.error('[useVoice] SpeechRecognition failed, falling back to audio:', err);
        startAudioRecording();
      }
    } else {
      // Fallback to audio recording
      startAudioRecording();
    }
  }, []);

  const startAudioRecording = useCallback(async () => {
    try {
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

      mediaRecorder.start(100);
      mediaRecorderRef.current = mediaRecorder;
    } catch (err) {
      console.error('[useVoice] Microphone access denied:', err);
      setError('Microphone access denied');
      setCurrentState(VOICE_STATES.IDLE);
    }
  }, [sendAudio]);

  const stopListening = useCallback(() => {
    // Stop Speech Recognition and send the text
    if (recognitionRef.current) {
      recognitionRef.current.stop();
      recognitionRef.current = null;
      const finalText = interimTranscriptRef.current;
      if (finalText.trim()) {
        sendText(finalText);
      } else {
        setCurrentState(VOICE_STATES.IDLE);
      }
      return;
    }

    // Stop audio recording (fallback)
    if (mediaRecorderRef.current && mediaRecorderRef.current.state === 'recording') {
      mediaRecorderRef.current.stop();
      mediaRecorderRef.current = null;
    }
  }, [sendText]);

  // Spacebar push-to-talk
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

  // Demo mode
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
