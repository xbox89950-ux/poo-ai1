"""Voice recording utility"""
import logging
import tempfile
import wave
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

class VoiceRecorder:
    @staticmethod
    def record(duration: int = 5, output_path: Optional[str] = None) -> str:
        try:
            import sounddevice as sd
            import numpy as np

            if not output_path:
                output_path = str(Path.home() / "Desktop" / f"poo_recording_{int(time.time())}.wav")

            logger.info(f"Recording for {duration} seconds...")
            fs = 44100
            recording = sd.rec(int(duration * fs), samplerate=fs, channels=2, dtype=np.int16)
            sd.wait()

            with wave.open(output_path, 'wb') as wf:
                wf.setnchannels(2)
                wf.setsampwidth(2)
                wf.setframerate(fs)
                wf.writeframes(recording.tobytes())

            return f"Recording saved to {output_path}"
        except ImportError:
            return "sounddevice not installed. Run: pip install sounddevice numpy"
        except Exception as e:
            return f"Recording error: {e}"
