# Jumpcutter GUI

Jumpcutter is a desktop tool that trims silent segments from lecture or talk recordings to create a shorter, more engaging video. The application provides a Tkinter-based interface on top of FFmpeg, guiding you through loading a source file, choosing output options, and processing the video while keeping audio and video in sync.

## Features
- Detects silent sections in a video by analysing the audio track and removes them automatically.
- Uses FFmpeg under the hood for reliable audio/video processing.
- Offers a simple graphical interface that explains each step of the workflow in Lithuanian.
- Keeps the codebase modular with separate `core` processing logic and `gui` orchestration modules.

## Requirements
- Python 3.8 or later.
- FFmpeg available on your system `PATH`.
- Recommended: a virtual environment to isolate dependencies.

## Installation
1. Clone this repository and move into the project directory:
   ```bash
   git clone https://github.com/your-username/jumpcutter.git
   cd jumpcutter
   ```
2. (Optional) Create and activate a virtual environment.
3. Install the Python requirements:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. Ensure FFmpeg is installed and accessible from the command line.
2. Run the GUI launcher:
   ```bash
   python -m jumpcutter.gui
   ```
3. Follow the Lithuanian prompts in the window to select an input video, adjust silence thresholds, and start processing.
4. The processed video is saved next to the source file with silent portions removed.

## Project Structure
- `jumpcutter/core.py` — processing pipeline that analyses audio, removes silence, and writes the final video.
- `jumpcutter/gui.py` — Tkinter interface that gathers user input and orchestrates processing with explanatory Lithuanian messages.
- `jumpcutter/__init__.py` — package metadata and convenience helpers.
- `jumpcutter.py` — legacy launcher kept for backwards compatibility.

---

# Jumpcutter GUI Lietuviškai

„Jumpcutter“ – tai darbalaukio įrankis, skirtas pašalinti tylias paskaitų ar pranešimų įrašų atkarpas ir taip sukurti trumpesnį, įtaigesnį vaizdo įrašą. Programa naudoja Tkinter grafinę sąsają ir FFmpeg, o lange pateikia paaiškinimus, kaip pasirinkti failą, nustatyti parametrus ir paleisti apdorojimą sinchronizuojant garsą su vaizdu.

## Funkcijos
- Automatiškai aptinka tylias garso takelio vietas ir jas iškerpa.
- Naudoja FFmpeg, todėl apdorojimas yra patikimas ir kokybiškas.
- Pateikia paprastą grafinę sąsają su aiškiais lietuviškais paaiškinimais.
- Kodo bazė suskaidyta į atskirus `core` ir `gui` modulius, todėl lengviau prižiūrėti ir plėsti.

## Reikalavimai
- Python 3.8 arba naujesnė versija.
- FFmpeg turi būti prieinamas per sistemos `PATH`.
- Rekomenduojama naudoti virtualią aplinką priklausomybėms atskirti.

## Diegimas
1. Nuklonuokite šį repozitoriją ir atverkite projekto aplanką:
   ```bash
   git clone https://github.com/your-username/jumpcutter.git
   cd jumpcutter
   ```
2. (Nebūtina) Susikurkite ir aktyvuokite virtualią aplinką.
3. Įdiekite Python priklausomybes:
   ```bash
   pip install -r requirements.txt
   ```

## Naudojimas
1. Įsitikinkite, kad FFmpeg įdiegtas ir pasiekiamas per komandų eilutę.
2. Paleiskite grafinę sąsają:
   ```bash
   python -m jumpcutter.gui
   ```
3. Lange vadovaukitės lietuviškais nurodymais: pasirinkite įvesties vaizdo įrašą, sureguliuokite tylos slenksčius ir pradėkite apdorojimą.
4. Apdorotas vaizdo įrašas išsaugomas greta pradinio failo, pašalinus tylias atkarpas.

## Projekto struktūra
- `jumpcutter/core.py` – apdorojimo eiga: garso analizė, tylos iškirpimas ir galutinio vaizdo įrašymas.
- `jumpcutter/gui.py` – Tkinter sąsaja, kuri surenka naudotojo nustatymus ir paleidžia apdorojimą su paaiškinimais.
- `jumpcutter/__init__.py` – paketo metainformacija ir pagalbinės funkcijos.
- `jumpcutter.py` – senesnis paleidimo scenarijus, paliktas suderinamumui.
