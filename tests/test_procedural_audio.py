"""Pygame-independent contracts for procedural public audio."""

from __future__ import annotations

from array import array
import sys

import pytest

from vector_barrage.audio import (
    ENEMY_DESTROYED_PATTERN,
    GAMEPLAY_PATTERN,
    MENU_PATTERN,
    NEW_RECORD_PATTERN,
    NullAudioService,
    ProceduralAudioService,
    ToneSegment,
    synthesize_pcm,
)


def _decode_pcm16(payload: bytes) -> list[int]:
    samples = array("h")
    samples.frombytes(payload)
    if sys.byteorder != "little":
        samples.byteswap()
    return list(samples)


def test_pcm_length_matches_duration_sample_rate_and_channels() -> None:
    payload = synthesize_pcm(
        [ToneSegment(440.0, 100, 0.25)],
        sample_rate=1_000,
        channels=2,
    )
    assert len(payload) == 100 * 2 * 2


def test_zero_frequency_segment_produces_digital_silence() -> None:
    payload = synthesize_pcm(
        [ToneSegment(0.0, 50, 0.0)],
        sample_rate=1_000,
        channels=1,
    )
    assert set(payload) <= {0}


def test_stereo_pcm_duplicates_each_mono_sample_per_channel() -> None:
    samples = _decode_pcm16(
        synthesize_pcm(
            [ToneSegment(125.0, 40, 0.5)],
            sample_rate=1_000,
            channels=2,
        )
    )
    assert samples
    assert all(left == right for left, right in zip(samples[::2], samples[1::2]))


def test_semantic_patterns_are_nonempty_and_distinct() -> None:
    payloads = {
        synthesize_pcm(pattern, sample_rate=4_000, channels=1)
        for pattern in (
            MENU_PATTERN,
            GAMEPLAY_PATTERN,
            ENEMY_DESTROYED_PATTERN,
            NEW_RECORD_PATTERN,
        )
    }
    assert len(payloads) == 4


@pytest.mark.parametrize(
    "kwargs",
    [
        {"frequency_hz": -1.0, "duration_ms": 10},
        {"frequency_hz": 440.0, "duration_ms": 0},
        {"frequency_hz": 440.0, "duration_ms": 10, "volume": -0.1},
        {"frequency_hz": 440.0, "duration_ms": 10, "volume": 1.1},
    ],
)
def test_tone_segment_rejects_invalid_parameters(kwargs: dict[str, object]) -> None:
    with pytest.raises(ValueError):
        ToneSegment(**kwargs)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "kwargs",
    [
        {"sample_rate": 0},
        {"channels": 0},
        {"gain": -0.1},
        {"gain": 1.1},
    ],
)
def test_pcm_synthesis_rejects_invalid_runtime_parameters(
    kwargs: dict[str, object],
) -> None:
    with pytest.raises(ValueError):
        synthesize_pcm([ToneSegment(440.0, 10)], **kwargs)  # type: ignore[arg-type]


def test_null_audio_service_retains_no_op_fallback_contract() -> None:
    audio = NullAudioService()
    assert audio.play_menu_music() is None
    assert audio.play_gameplay_music() is None
    assert audio.play_enemy_destroyed() is None
    assert audio.play_new_record() is None
    assert audio.stop_music() is None


def test_procedural_audio_service_constructor_has_no_pygame_side_effect() -> None:
    service = ProceduralAudioService(sample_rate=22_050, channels=1, master_gain=0.4)
    assert service.sample_rate == 22_050
    assert service.channels == 1
    assert service.master_gain == pytest.approx(0.4)
