"""
Audio Service — microphone recording, speaker playback, and device management.

Uses PyAudio for recording and subprocess for playback.
"""

import os
import logging
import struct
import subprocess
import wave
from typing import Optional

import numpy as np

logger = logging.getLogger("mirror-companion.audio")


class AudioService:
    """
    Manages audio input/output for the mirror companion.

    Handles microphone recording with PyAudio and audio playback
    through the system speaker.
    """

    def __init__(self):
        self._sample_rate = 16000  # Standard for speech recognition

    def list_audio_devices(self) -> dict:
        """
        List available audio input and output devices.

        Returns:
            Dict with 'input_devices' and 'output_devices' lists.
        """
        devices = {"input_devices": [], "output_devices": []}

        try:
            import pyaudio

            pa = pyaudio.PyAudio()
            for i in range(pa.get_device_count()):
                info = pa.get_device_info_by_index(i)
                device_entry = {"index": i, "name": info["name"]}
                if info["maxInputChannels"] > 0:
                    devices["input_devices"].append(device_entry)
                if info["maxOutputChannels"] > 0:
                    devices["output_devices"].append(device_entry)
            pa.terminate()
            logger.info(
                f"Found {len(devices['input_devices'])} input, "
                f"{len(devices['output_devices'])} output device(s)."
            )

        except Exception as e:
            logger.error(f"Error listing audio devices: {e}", exc_info=True)

        return devices

    def record_audio(
        self,
        duration_seconds: float,
        output_path: str,
        device_index: int = -1,
    ) -> str:
        """
        Record audio from the microphone and save as a WAV file.

        Args:
            duration_seconds: How long to record in seconds.
            output_path: Path to save the WAV file.
            device_index: Audio input device index (-1 for default).

        Returns:
            Path to the saved WAV file.
        """
        try:
            import pyaudio

            chunk_size = 1024
            pa = pyaudio.PyAudio()

            stream_kwargs = {
                "rate": self._sample_rate,
                "channels": 1,
                "format": pyaudio.paInt16,
                "input": True,
                "frames_per_buffer": chunk_size,
            }
            if device_index >= 0:
                stream_kwargs["input_device_index"] = device_index

            stream = pa.open(**stream_kwargs)

            total_chunks = int(self._sample_rate * duration_seconds / chunk_size)
            frames = []

            logger.info(
                f"Recording {duration_seconds}s of audio to {output_path}..."
            )

            for _ in range(total_chunks):
                data = stream.read(chunk_size, exception_on_overflow=False)
                frames.append(data)

            stream.stop_stream()
            stream.close()
            pa.terminate()

            # Save as WAV file
            with wave.open(output_path, "w") as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)  # 16-bit
                wf.setframerate(self._sample_rate)
                wf.writeframes(b"".join(frames))

            logger.info(f"Audio recorded successfully: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"Error recording audio: {e}", exc_info=True)
            raise

    def play_audio(self, file_path: str) -> bool:
        """
        Play an audio file through the system speaker.

        Uses aplay for WAV files on Linux/Pi, or ffplay as fallback.

        Args:
            file_path: Path to the audio file (mp3, wav, etc.)

        Returns:
            True if playback succeeded.
        """
        if not os.path.exists(file_path):
            logger.error(f"Audio file not found: {file_path}")
            return False

        try:
            ext = os.path.splitext(file_path)[1].lower()

            if ext == ".wav":
                result = subprocess.run(
                    ["aplay", file_path],
                    capture_output=True,
                    timeout=60,
                )
                if result.returncode != 0:
                    logger.warning(f"aplay failed, trying ffplay: {result.stderr}")
                    raise FileNotFoundError("aplay failed")
            else:
                result = subprocess.run(
                    [
                        "ffplay",
                        "-nodisp",
                        "-autoexit",
                        "-loglevel",
                        "quiet",
                        file_path,
                    ],
                    capture_output=True,
                    timeout=60,
                )
                if result.returncode != 0:
                    logger.error(f"ffplay failed: {result.stderr}")
                    return False

            logger.info(f"Audio playback complete: {file_path}")
            return True

        except FileNotFoundError:
            try:
                subprocess.run(
                    ["mpv", "--no-video", file_path],
                    capture_output=True,
                    timeout=60,
                )
                return True
            except FileNotFoundError:
                logger.error(
                    "No audio player found. Install ffplay (ffmpeg) or mpv."
                )
                return False

        except Exception as e:
            logger.error(f"Error playing audio: {e}", exc_info=True)
            return False

    def get_audio_level(self, device_index: int = -1) -> Optional[float]:
        """
        Get the current microphone input level for audio visualization.

        Returns:
            Float between 0.0 and 1.0 representing audio level, or None on error.
        """
        try:
            import pyaudio

            chunk_size = 1024
            pa = pyaudio.PyAudio()

            stream_kwargs = {
                "rate": self._sample_rate,
                "channels": 1,
                "format": pyaudio.paInt16,
                "input": True,
                "frames_per_buffer": chunk_size,
            }
            if device_index >= 0:
                stream_kwargs["input_device_index"] = device_index

            stream = pa.open(**stream_kwargs)
            data = stream.read(chunk_size, exception_on_overflow=False)
            stream.stop_stream()
            stream.close()
            pa.terminate()

            audio_array = np.frombuffer(data, dtype=np.int16).astype(np.float32)
            rms = np.sqrt(np.mean(audio_array ** 2))
            level = min(rms / 32767.0 * 10, 1.0)

            return round(level, 3)

        except Exception as e:
            logger.error(f"Error getting audio level: {e}", exc_info=True)
            return None
