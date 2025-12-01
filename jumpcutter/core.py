"""Core „Jumpcutter“ vaizdo apdorojimo logika."""

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
    """Eksportuoja garso takelį iš ``video`` į laikiną ``temp_audio_path`` failą."""
    video.audio.write_audiofile(temp_audio_path, logger=None)


def _detect_nonsilent_parts(
    audio_path: str, min_silence_len: int, silence_thresh: int
) -> List[TimeRange]:
    """Randa ir grąžina visų tylos atkarpų laiko intervalus."""
    sound = AudioSegment.from_file(audio_path)
    nonsilent_parts = detect_nonsilent(
        sound, min_silence_len=min_silence_len, silence_thresh=silence_thresh
    )
    return [(start / 1000, end / 1000) for start, end in nonsilent_parts]


def _process_segment(
    video: VideoFileClip, start: float, end: float, min_silence_len: int
) -> VideoFileClip:
    """Sukuria apdorotą ``VideoFileClip`` konkrečiai laiko atkarpai."""
    segment_duration = end - start
    segment = video.subclip(start, end)

    # Jei atkarpa trumpesnė nei nustatyta minimali tyla, ją išsaugome kaip yra.
    if segment_duration >= (min_silence_len / 1000):
        return segment

    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp_input, \
            tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp_output:
        segment.write_videofile(
            temp_input.name, codec="libx264", audio_codec="aac", logger=None
        )

        # FFmpeg pagreitinimas, jei reikėtų korekcijų ateityje.
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
    """Sukuria naują video, kuriame tylos atkarpos praleidžiamos."""
    if not os.path.isfile(video_path):
        print(f"Klaida: failas '{video_path}' nerastas.")
        return

    print(f"\nApdorojamas failas: {video_path}")
    print("[1/4] Įkeliame video failą į atmintį...")
    video = VideoFileClip(video_path)

    print("[2/4] Išskiriame garso takelį...")
    temp_audio_path = "temp_audio.wav"
    _export_audio(video, temp_audio_path)

    print("[3/4] Ieškome kalbos (ne tylos) atkarpų garse...")
    nonsilent_times = _detect_nonsilent_parts(
        temp_audio_path, min_silence_len=min_silence_len, silence_thresh=silence_thresh
    )

    print("[4/4] Sujungiame rastas atkarpas į naują video failą...")
    clips = []
    for start, end in tqdm(nonsilent_times, desc="Apdorojame vaizdo segmentus"):
        try:
            clips.append(_process_segment(video, start, end, min_silence_len))
        except Exception as exc:  # pragma: no cover - logging is side-effect only
            print(f"Klaida pagreitinant segmentą {start}-{end}: {exc}. Segmentas praleidžiamas.")
            continue

    final_video = concatenate_videoclips(clips)
    final_video.write_videofile(output_path, codec="libx264", audio_codec="aac")

    # Tvarkome temp failus ir pranešame vartotojui.
    if os.path.exists(temp_audio_path):
        os.remove(temp_audio_path)

    print(f"Darbas baigtas! Naujas failas: {output_path}")
