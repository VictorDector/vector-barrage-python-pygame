"""Procedural audio services for Vector Barrage.

All audible cues in the public candidate are synthesized at runtime from simple
waveforms defined in this module. No historical or third-party audio files are
required by the application.
"""

from __future__ import annotations

from array import array
from dataclasses import dataclass
from math import pi, sin
import sys
from typing import Protocol, Sequence


class AudioService(Protocol):
    """Semantic audio operations consumed by the application coordinator."""

    def play_menu_music(self) -> None: ...

    def play_gameplay_music(self) -> None: ...

    def play_enemy_destroyed(self) -> None: ...

    def play_new_record(self) -> None: ...

    def stop_music(self) -> None: ...


class NullAudioService:
    """No-op audio service for tests and environments without audio."""

    def play_menu_music(self) -> None:
        return None

    def play_gameplay_music(self) -> None:
        return None

    def play_enemy_destroyed(self) -> None:
        return None

    def play_new_record(self) -> None:
        return None

    def stop_music(self) -> None:
        return None


@dataclass(frozen=True, slots=True)
class ToneSegment:
    """One synthesized sine-wave or silence segment."""

    frequency_hz: float
    duration_ms: int
    volume: float = 0.25

    def __post_init__(self) -> None:
        if self.frequency_hz < 0:
            raise ValueError("frequency_hz must be non-negative")
        if self.duration_ms <= 0:
            raise ValueError("duration_ms must be positive")
        if not 0.0 <= self.volume <= 1.0:
            raise ValueError("volume must be between 0 and 1")


def synthesize_pcm(
    segments: Sequence[ToneSegment],
    *,
    sample_rate: int = 44_100,
    channels: int = 2,
    gain: float = 1.0,
) -> bytes:
    """Synthesize signed 16-bit little-endian PCM for the supplied sequence."""

    if sample_rate <= 0:
        raise ValueError("sample_rate must be positive")
    if channels <= 0:
        raise ValueError("channels must be positive")
    if not 0.0 <= gain <= 1.0:
        raise ValueError("gain must be between 0 and 1")

    pcm = array("h")
    peak = 32_767

    for segment in segments:
        frame_count = max(1, round(sample_rate * segment.duration_ms / 1000.0))
        edge = max(1, min(frame_count // 2, round(sample_rate * 0.005)))

        for frame in range(frame_count):
            if segment.frequency_hz == 0:
                value = 0
            else:
                attack = min(frame / edge, 1.0)
                release = min((frame_count - 1 - frame) / edge, 1.0)
                envelope = max(0.0, min(attack, release))
                phase = 2.0 * pi * segment.frequency_hz * frame / sample_rate
                value = round(
                    peak
                    * segment.volume
                    * gain
                    * envelope
                    * sin(phase)
                )
            pcm.extend([value] * channels)

    if sys.byteorder != "little":
        pcm.byteswap()
    return pcm.tobytes()


MENU_PATTERN = (
    ToneSegment(261.63, 170, 0.18),
    ToneSegment(329.63, 170, 0.18),
    ToneSegment(392.00, 210, 0.18),
    ToneSegment(0.00, 90, 0.0),
)

GAMEPLAY_PATTERN = (
    ToneSegment(220.00, 110, 0.13),
    ToneSegment(277.18, 110, 0.13),
    ToneSegment(329.63, 110, 0.13),
    ToneSegment(277.18, 110, 0.13),
    ToneSegment(0.00, 50, 0.0),
)

ENEMY_DESTROYED_PATTERN = (
    ToneSegment(220.00, 45, 0.28),
    ToneSegment(110.00, 70, 0.22),
)

NEW_RECORD_PATTERN = (
    ToneSegment(523.25, 110, 0.23),
    ToneSegment(659.25, 110, 0.23),
    ToneSegment(783.99, 210, 0.25),
)


class ProceduralAudioService:
    """Generate and play original runtime tones through ``pygame.mixer``.

    The service fails soft when an audio device or compatible mixer format is not
    available so audio cannot prevent the game from starting.
    """

    def __init__(
        self,
        *,
        sample_rate: int = 44_100,
        channels: int = 2,
        master_gain: float = 0.55,
    ) -> None:
        if sample_rate <= 0:
            raise ValueError("sample_rate must be positive")
        if channels <= 0:
            raise ValueError("channels must be positive")
        if not 0.0 <= master_gain <= 1.0:
            raise ValueError("master_gain must be between 0 and 1")

        self.sample_rate = sample_rate
        self.channels = channels
        self.master_gain = master_gain
        self._pygame = None
        self._disabled = False
        self._sounds: dict[str, object] = {}
        self._music_channel = None

    def _ensure_ready(self) -> bool:
        if self._disabled:
            return False

        try:
            import pygame

            if not pygame.mixer.get_init():
                pygame.mixer.init(
                    frequency=self.sample_rate,
                    size=-16,
                    channels=self.channels,
                    buffer=512,
                )

            mixer_state = pygame.mixer.get_init()
            if not mixer_state:
                self._disabled = True
                return False

            frequency, sample_format, channels = mixer_state
            if sample_format != -16 or channels <= 0:
                self._disabled = True
                return False

            self.sample_rate = frequency
            self.channels = channels
            self._pygame = pygame
            return True
        except Exception:
            self._disabled = True
            return False

    def _sound(self, key: str, pattern: Sequence[ToneSegment]):
        if key in self._sounds:
            return self._sounds[key]
        if not self._ensure_ready():
            return None

        try:
            payload = synthesize_pcm(
                pattern,
                sample_rate=self.sample_rate,
                channels=self.channels,
                gain=self.master_gain,
            )
            sound = self._pygame.mixer.Sound(buffer=payload)
        except Exception:
            self._disabled = True
            return None

        self._sounds[key] = sound
        return sound

    def _play_loop(self, key: str, pattern: Sequence[ToneSegment]) -> None:
        self.stop_music()
        sound = self._sound(key, pattern)
        if sound is not None:
            self._music_channel = sound.play(loops=-1)

    def play_menu_music(self) -> None:
        self._play_loop("menu", MENU_PATTERN)

    def play_gameplay_music(self) -> None:
        self._play_loop("gameplay", GAMEPLAY_PATTERN)

    def play_enemy_destroyed(self) -> None:
        sound = self._sound("enemy_destroyed", ENEMY_DESTROYED_PATTERN)
        if sound is not None:
            sound.play()

    def play_new_record(self) -> None:
        sound = self._sound("new_record", NEW_RECORD_PATTERN)
        if sound is not None:
            sound.play()

    def stop_music(self) -> None:
        if self._music_channel is not None:
            try:
                self._music_channel.stop()
            finally:
                self._music_channel = None
