import os
import subprocess
import tempfile
import tkinter as tk
from tkinter import filedialog, ttk
from moviepy.editor import VideoFileClip
from pydub import AudioSegment
from pydub.silence import detect_nonsilent
from tqdm import tqdm


# ================== CORE LOGIC ==================
def jumpcutter(video_path, output_path, silence_thresh=-40, min_silence_len=500):
    if not os.path.isfile(video_path):
        print(f"Error: The file '{video_path}' does not exist.")
        return

    print(f"\nProcessing: {video_path}")
    print("[1/4] Loading video...")
    video = VideoFileClip(video_path)
    audio = video.audio

    print("[2/4] Exporting audio for silence detection...")
    temp_audio_path = "temp_audio.wav"
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
        segment_duration = end - start
        segment = video.subclip(start, end)

        # Pagreitiname segmentą su FFmpeg, jei reikia
        if segment_duration < (min_silence_len / 1000):
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
                        "-filter_complex", f"[0:v]setpts={1}*PTS[v]; [0:a]atempo={1}[a]",
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

    # Išsaugome naują vaizdo įrašą
    from moviepy.editor import concatenate_videoclips

    final_video = concatenate_videoclips(clips)

    final_video.write_videofile(output_path, codec="libx264", audio_codec="aac")

# ================== GUI ==================
class JumpCutterApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("JumpCutter")
        self.geometry("500x500")
        self._create_widgets()


    def _update_thresh_desc(self, value):
        value = int(float(value))
        if value <= -55:
            desc = "Labai jautru (tyla studijoje)"
        elif value <= -45:
            desc = "Rekomenduojama kalbiniams įrašams"
        elif value <= -35:
            desc = "Vidutinis slenkstis (gatvės triukšmas)"
        else:
            desc = "Mažas jautrumas (triukšminga aplinka)"
        self.thresh_desc.config(text=f"{value} dB: {desc}")

    def _update_silence_len_desc(self, value):
        self.silence_len_desc.config(text=f"Minimali tyla: {int(float(value))} ms")

    def _create_widgets(self):
        # Parametrų įvedimas
        main_frame = tk.Frame(self)
        main_frame.pack(pady=10)

        # Tylos slenkstis
        thresh_frame = tk.Frame(main_frame)
        thresh_frame.pack(pady=5)

        tk.Label(thresh_frame, text="Tylos slenkstis:").pack()
        self.silence_thresh = tk.Scale(
            thresh_frame,
            from_=-60,
            to=-30,
            resolution=5,  # Nustatomas 5 db žingsnis
            orient="horizontal",
            command=self._update_thresh_desc
        )
        self.silence_thresh.set(-40)
        self.silence_thresh.pack()

        self.thresh_desc = tk.Label(thresh_frame, text="", fg="gray")
        self.thresh_desc.pack()
        self._update_thresh_desc(-40)

        # Minimali tylos trukmė
        silence_len_frame = tk.Frame(main_frame)
        silence_len_frame.pack(pady=5)

        tk.Label(silence_len_frame, text="Minimali tylos trukmė:").pack()
        self.min_silence_len = tk.Scale(
            silence_len_frame,
            from_=100,
            to=2000,
            resolution=100,  # Nustatomas 100 ms žingsnis
            orient="horizontal",
            command=self._update_silence_len_desc
        )
        self.min_silence_len.set(500)
        self.min_silence_len.pack()

        self.silence_len_desc = tk.Label(silence_len_frame, text="", fg="gray")
        self.silence_len_desc.pack()
        self._update_silence_len_desc(500)


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
            )
            self.status_label.config(text=f"Baigta! Išsaugota: {output_path}", fg="blue")
        except Exception as e:
            self.status_label.config(text=f"Klaida: {str(e)}", fg="red")
        finally:
            self.progress.stop()
            self.progress.pack_forget()


# ================== PALEIDIMAS ==================
if __name__ == "__main__":
    app = JumpCutterApp()
    app.mainloop()
