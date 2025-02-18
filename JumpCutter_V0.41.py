import os
import subprocess
import sys
import tempfile
import tkinter as tk
from tkinter import filedialog, ttk
from moviepy.editor import VideoFileClip
from pydub import AudioSegment
from pydub.silence import detect_nonsilent
from tqdm import tqdm


# ================== CORE LOGIC ==================
def jumpcutter(video_path, output_path, silence_thresh=-40, min_silence_len=500, speed_up=2.0):
    if not os.path.isfile(video_path):
        print(f"Error: The file '{video_path}' does not exist.")
        return

    print(f"\nProcessing: {video_path}")
    print("[1/4] Loading video...")
    video = VideoFileClip(video_path)
    audio = video.audio

    print("[2/4] Exporting audio for silence detection...")
    temp_audio_path = "temp_audio.wav"
    audio = video.audio

    # Priverstinai keičiame audio dažnį į 48 kHz
    audio = audio.set_fps(48000)   # <─── Čia pridedamas audio resampling
    audio.write_audiofile(temp_audio_path, logger=None)

    print("[3/4] Detecting non-silent audio segments...")
    sound = AudioSegment.from_file(temp_audio_path)
    nonsilent_parts = detect_nonsilent(
        sound, min_silence_len=min_silence_len, silence_thresh=silence_thresh
    )
    nonsilent_times = [(start / 1000, end / 1000) for start, end in nonsilent_parts]

    print("[4/4] Creating new video by concatenating non-silent parts...")
    clips = []
    for start, end in tqdm(nonsilent_times, desc="Processing video segments"):
        segment = video.subclip(start, end)

        # Pagreitiname segmentą su FFmpeg, jei reikia
        if (end - start) < (min_silence_len / 1000):
            try:
                # Sukuriame laikinus failus
                with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp_input, \
                        tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp_output:

                    # Išsaugome originalų segmentą
                    segment.write_videofile(temp_input.name, codec="libx264", audio_codec="aac", logger=None)

                    # FFmpeg komanda pagreitinimui
                    ffmpeg_cmd = [
                        "ffmpeg",
                        "-y",  # Perrašyti failą be patvirtinimo
                        "-i", temp_input.name,
                        "-filter_complex", f"[0:v]setpts={1 / speed_up}*PTS[v];[0:a]atempo={speed_up}[a]",
                        "-map", "[v]",
                        "-map", "[a]",
                        "-c:v", "libx264",
                        "-c:a", "aac",
                        temp_output.name
                    ]

                    # Paleidžiame FFmpeg
                    subprocess.run(ffmpeg_cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                    # Įkeliame pagreitintą segmentą
                    sped_up_clip = VideoFileClip(temp_output.name)
                    clips.append(sped_up_clip)

            except Exception as e:
                print(f"Klaida pagreitinant segmentą {start}-{end}: {e}. Segmentas praleidžiamas.")
                continue
        else:
            clips.append(segment)


# ================== GUI ==================
class JumpCutterApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("JumpCutter 4.0")
        self.geometry("500x400")
        self._create_widgets()

    def _create_widgets(self):
        # Parametrų įvedimas
        tk.Label(self, text="Įveskite parametrus:").pack(pady=10)

        # Tylos slenkstis
        tk.Label(self, text="Tylos slenkstis (dB):").pack()
        self.silence_thresh = tk.Entry(self)
        self.silence_thresh.insert(0, "-40")
        self.silence_thresh.pack()

        # Minimali tylos trukmė
        tk.Label(self, text="Minimali tylos trukmė (ms):").pack()
        self.min_silence_len = tk.Entry(self)
        self.min_silence_len.insert(0, "500")
        self.min_silence_len.pack()

        # Greičio daugiklis
        tk.Label(self, text="Pagreitėjimo daugiklis:").pack()
        # Greičio daugiklis (nuo 1.0 iki 2.0)
        self.speed_up = tk.Scale(self, from_=1.0, to=2.0, resolution=0.1, orient="horizontal")
        self.speed_up.set(1.5)  # Numatytasis daugiklis
        self.speed_up.pack()

        # Failo pasirinkimo mygtukas
        tk.Button(self, text="Pasirinkti video", command=self._select_file).pack(pady=20)

        # Progreso juosta
        self.progress = ttk.Progressbar(self, mode="indeterminate")

        # Statuso žinutė
        self.status_label = tk.Label(self, text="", fg="gray")
        self.status_label.pack()

    def _select_file(self):
        file_path = filedialog.askopenfilename(
            title="Pasirinkite video failą",
            filetypes=[("Video Files", "*.mp4 *.mkv *.webm *.mov")]
        )
        if file_path:
            self._process_video(file_path)

    def _process_video(self, input_path):
        self.progress.pack(pady=10)
        self.progress.start()
        self.status_label.config(text="Apdorojama...", fg="green")

        try:
            output_path = f"jumpcutted_{os.path.basename(input_path)}"
            jumpcutter(
                input_path,
                output_path,
                silence_thresh=int(self.silence_thresh.get()),
                min_silence_len=int(self.min_silence_len.get()),
                speed_up=float(self.speed_up.get())
            )
            self.status_label.config(text=f"Baigta! Išsaugota: {output_path}", fg="blue")
        except Exception as e:
            self.status_label.config(text=f"Klaida: {str(e)}", fg="red")
        finally:
            self.progress.stop()
            self.progress.pack_forget()


# ================== PALEIDIMAS ==================
if __name__ == "__main__":
    if len(sys.argv) > 1:
        # CLI režimas
        for input_file in sys.argv[1:]:
            output_file = f"jumpcutted_{os.path.basename(input_file)}"
            jumpcutter(input_file, output_file)
        input("Uždarykite programą paspaudę Enter...")
    else:
        # GUI režimas
        app = JumpCutterApp()
        app.mainloop()