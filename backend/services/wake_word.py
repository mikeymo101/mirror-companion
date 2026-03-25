"""
Wake Word Service — OpenWakeWord "Mirror Mirror" detection.

Listens for the wake word using OpenWakeWord (free, offline, no account needed)
and triggers a callback. Runs in a background thread.
"""

import os
import logging
import threading
import numpy as np
from typing import Callable, Optional

logger = logging.getLogger("mirror-companion.wake_word")


class WakeWordService:
    """
    Listens for the "Mirror Mirror" wake word using OpenWakeWord.

    Usage:
        service = WakeWordService(on_wake_word=my_callback)
        service.start_listening()
        # ... later ...
        service.stop_listening()
    """

    def __init__(self, on_wake_word: Optional[Callable] = None):
        self.on_wake_word = on_wake_word
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._model = None
        self._audio_stream = None
        self._pyaudio = None

        # Sensitivity threshold (0.0 to 1.0, higher = fewer false positives)
        self.threshold = float(os.environ.get("WAKE_WORD_THRESHOLD", "0.5"))

        # Custom model path (optional — if user trains a custom "mirror mirror" model)
        self.custom_model_path = os.environ.get("WAKE_WORD_MODEL_PATH", "")

    def _initialize(self):
        """Initialize OpenWakeWord model and audio stream."""
        try:
            import openwakeword
            from openwakeword.model import Model
            import pyaudio

            # Download default models if needed (first run only)
            openwakeword.utils.download_models()

            # Initialize the model
            if self.custom_model_path and os.path.exists(self.custom_model_path):
                # Use custom trained "mirror mirror" model
                self._model = Model(
                    wakeword_models=[self.custom_model_path],
                    inference_framework="onnx",
                )
                logger.info(f"Loaded custom wake word model: {self.custom_model_path}")
            else:
                # Use built-in "hey jarvis" as a placeholder until custom model is trained
                # OpenWakeWord ships with: alexa, hey_mycroft, hey_jarvis, etc.
                self._model = Model(
                    wakeword_models=["hey_jarvis"],
                    inference_framework="onnx",
                )
                logger.info(
                    "Using built-in 'hey jarvis' wake word as placeholder. "
                    "Train a custom 'mirror mirror' model for production use."
                )

            # Set up PyAudio for microphone capture
            self._pyaudio = pyaudio.PyAudio()
            self._audio_stream = self._pyaudio.open(
                rate=16000,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=1280,  # 80ms chunks at 16kHz
            )

            logger.info("OpenWakeWord engine initialized successfully.")
            return True

        except ImportError as e:
            logger.error(
                f"Missing dependency: {e}. "
                "Install with: pip install openwakeword pyaudio"
            )
            return False
        except Exception as e:
            logger.error(f"Failed to initialize OpenWakeWord: {e}", exc_info=True)
            return False

    def _listen_loop(self):
        """Background thread loop that continuously listens for the wake word."""
        if not self._initialize():
            logger.error("Cannot start listening — initialization failed.")
            return

        try:
            logger.info("Wake word listener started. Listening...")

            while self._running:
                # Read audio chunk from microphone
                audio_bytes = self._audio_stream.read(1280, exception_on_overflow=False)
                audio_data = np.frombuffer(audio_bytes, dtype=np.int16)

                # Run wake word detection
                prediction = self._model.predict(audio_data)

                # Check all model scores against threshold
                for model_name, score in prediction.items():
                    if score > self.threshold:
                        logger.info(
                            f"Wake word detected! (model={model_name}, score={score:.3f})"
                        )
                        # Reset the model to avoid repeated triggers
                        self._model.reset()

                        if self.on_wake_word:
                            try:
                                self.on_wake_word()
                            except Exception as e:
                                logger.error(
                                    f"Error in wake word callback: {e}", exc_info=True
                                )
                        break

        except Exception as e:
            logger.error(f"Error in wake word listen loop: {e}", exc_info=True)
        finally:
            self._cleanup()

    def _cleanup(self):
        """Clean up audio resources."""
        if self._audio_stream is not None:
            try:
                self._audio_stream.stop_stream()
                self._audio_stream.close()
            except Exception:
                pass
            self._audio_stream = None

        if self._pyaudio is not None:
            try:
                self._pyaudio.terminate()
            except Exception:
                pass
            self._pyaudio = None

        self._model = None
        logger.info("Wake word resources cleaned up.")

    def start_listening(self):
        """Start listening for the wake word in a background thread."""
        if self._running:
            logger.warning("Wake word listener is already running.")
            return

        self._running = True
        self._thread = threading.Thread(
            target=self._listen_loop,
            daemon=True,
            name="wake-word-listener",
        )
        self._thread.start()
        logger.info("Wake word listener thread started.")

    def stop_listening(self):
        """Stop listening for the wake word and clean up resources."""
        if not self._running:
            logger.warning("Wake word listener is not running.")
            return

        logger.info("Stopping wake word listener...")
        self._running = False

        if self._thread is not None:
            self._thread.join(timeout=5.0)
            self._thread = None

        logger.info("Wake word listener stopped.")

    @property
    def is_listening(self) -> bool:
        """Check if the wake word listener is currently active."""
        return self._running
