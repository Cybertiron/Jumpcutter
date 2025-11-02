"""Core video processing logic for Jumpcutter."""

from __future__ import annotations

import os
import subprocess
import tempfile
from typing import List, Tuple

from moviepy.editor import VideoFileClip, concatenate_videoclips
from pydub import AudioSegment
from pydub.silence import detect_nonsilent
from tqdm import tqdm


TimeRange = Tuple[float, float]


def _export_audio(video: VideoFileClip, temp_audio_path: str) -> None:
    """Export the audio track of the given ``video`` to ``temp_audio_path``."""
    video.audio.write_audiofile(temp_audio_path, logger=None)


def _detect_nonsilent_parts(
    audio_path: str, min_silence_len: int, silence_thresh: int
) -> List[TimeRange]:
    """Return a list of non-silent time ranges from the supplied audio file."""
    sound = AudioSegment.from_file(audio_path)
    nonsilent_parts = detect_nonsilent(
        sound, min_silence_len=min_silence_len, silence_thresh=silence_thresh
    )
    return [(start / 1000, end / 1000) for start, end in nonsilent_parts]


def _process_segment(
    video: VideoFileClip, start: float, end: float, min_silence_len: int
) -> VideoFileClip:
    """Return a processed ``VideoFileClip`` for the given time range."""
    segment_duration = end - start
    segment = video.subclip(start, end)

    # Speed up short segments with FFmpeg if needed
    if segment_duration >= (min_silence_len / 1000):
        return segment

    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp_input, \
            tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp_output:
        segment.write_videofile(
            temp_input.name, codec="libx264", audio_codec="aac", logger=None
        )

        ffmpeg_cmd = [
            "ffmpeg",
            "-y",
            "-i",
            temp_input.name,
            "-filter_complex",
            f"[0:v]setpts={1}*PTS[v]; [0:a]atempo={1}[a]",
            "-map",
            "[v]",
            "-map",
            "[a]",
            "-c:v",
            "libx264",
            "-c:a",
            "aac",
            temp_output.name,
        ]

        subprocess.run(ffmpeg_cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        return VideoFileClip(temp_output.name)


def jumpcutter(
    video_path: str,
    output_path: str,
    silence_thresh: int = -40,
    min_silence_len: int = 500,
) -> None:
    """Generate a new video that skips silent segments."""
    if not os.path.isfile(video_path):
        print(f"Error: The file '{video_path}' does not exist.")
        return

    print(f"\nProcessing: {video_path}")
    print("[1/4] Loading video...")
    video = VideoFileClip(video_path)

    print("[2/4] Exporting audio for silence detection...")
    temp_audio_path = "temp_audio.wav"
    _export_audio(video, temp_audio_path)

    print("[3/4] Detecting non-silent audio segments...")
    nonsilent_times = _detect_nonsilent_parts(
        temp_audio_path, min_silence_len=min_silence_len, silence_thresh=silence_thresh
    )

    print("[4/4] Creating new video by concatenating non-silent parts...")
    clips = []
    for start, end in tqdm(nonsilent_times, desc="Processing video segments"):
        try:
            clips.append(_process_segment(video, start, end, min_silence_len))
        except Exception as exc:  # pragma: no cover - logging is side-effect only
            print(f"Klaida pagreitinant segmentą {start}-{end}: {exc}. Segmentas praleidžiamas.")
            continue

    final_video = concatenate_videoclips(clips)
    final_video.write_videofile(output_path, codec="libx264", audio_codec="aac")
