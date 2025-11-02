"""Grafinė „Jumpcutter“ naudotojo sąsaja."""

import os
import tkinter as tk
from tkinter import filedialog, ttk

from .core import jumpcutter


class JumpCutterApp(tk.Tk):
    """Tkinter pagrindu sukurta sąsaja „Jumpcutter“ nustatymams ir paleidimui."""

    def __init__(self) -> None:
        super().__init__()
        self.title("JumpCutter")
        self.geometry("300x300")
        self._create_widgets()

    # --- UI helpers -------------------------------------------------
    def _update_thresh_desc(self, value: str) -> None:
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

    def _update_silence_len_desc(self, value: str) -> None:
        self.silence_len_desc.config(text=f"Minimali tyla: {int(float(value))} ms")

    # --- UI setup ---------------------------------------------------
    def _create_widgets(self) -> None:
        main_frame = tk.Frame(self)
        main_frame.pack(pady=10)

        # Silence threshold controls
        thresh_frame = tk.Frame(main_frame)
        thresh_frame.pack(pady=5)

        tk.Label(thresh_frame, text="Tylos slenkstis:").pack()
        self.silence_thresh = tk.Scale(
            thresh_frame,
            from_=-60,
            to=-30,
            resolution=5,
            orient="horizontal",
            command=self._update_thresh_desc,
        )
        self.silence_thresh.set(-40)
        self.silence_thresh.pack()

        self.thresh_desc = tk.Label(thresh_frame, text="", fg="gray")
        self.thresh_desc.pack()
        self._update_thresh_desc(-40)

        # Minimum silence length controls
        silence_len_frame = tk.Frame(main_frame)
        silence_len_frame.pack(pady=5)

        tk.Label(silence_len_frame, text="Minimali tylos trukmė:").pack()
        self.min_silence_len = tk.Scale(
            silence_len_frame,
            from_=100,
            to=2000,
            resolution=100,
            orient="horizontal",
            command=self._update_silence_len_desc,
        )
        self.min_silence_len.set(500)
        self.min_silence_len.pack()

        self.silence_len_desc = tk.Label(silence_len_frame, text="", fg="gray")
        self.silence_len_desc.pack()
        self._update_silence_len_desc(500)

        # Video selection button
        tk.Button(self, text="Pasirinkti video", command=self._select_file).pack(pady=20)

        # Progress indicator and status label
        self.progress = ttk.Progressbar(self, mode="indeterminate")
        self.status_label = tk.Label(self, text="", fg="gray")
        self.status_label.pack()

    # --- Actions ----------------------------------------------------
    def _select_file(self) -> None:
        file_path = filedialog.askopenfilename(
            title="Pasirinkite video failą",
            filetypes=[("Video Files", "*.mp4 *.mkv *.webm *.mov")],
        )
        if file_path:
            self._process_video(file_path)

    def _process_video(self, input_path: str) -> None:
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
        except Exception as exc:  # pragma: no cover - logging is side-effect only
            self.status_label.config(text=f"Klaida: {exc}", fg="red")
        finally:
            self.progress.stop()
            self.progress.pack_forget()


__all__ = ["JumpCutterApp"]
