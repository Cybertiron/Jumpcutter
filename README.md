# Jumpcutter GUI

Jumpcutter is a desktop application that removes silent parts from lectures or talks to make a shorter and more watchable video. It offers a Tkinter interface over FFmpeg, walking you through loading a source file, selecting output options, and processing the video while maintaining audio/video sync.

## Features
- Analyses the audio track to automatically detect and remove silent sections.
- Uses FFmpeg under the hood for dependable processing of audio and video.
- Provides a basic graphical interface in Lithuanian which breaks down each step in the workflow.
- Maintains modular separation between core processing logic and GUI orchestration modules.

## Requirements
- Python 3.8 or later. (Personally used 3.9 or 3.11)
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
3. Select an input video, set thresholds for silence, and begin processing by following the Lithuanian instructions in the GUI.
4. The output video will be saved in the same location as the source file with silences removed.


## Project Structure
- `jumpcutter/core.py` — Contains a processing pipeline which detects silences in audio, removes them and writes final output video.
- `jumpcutter/gui.py` — A Tkinter based interface to collect inputs from userand manage processing.Displaying all messages to user in Lithuanian.
- `jumpcutter/__init__.py` — Contains package meta data and some utility functions.<end_of_text|>
- `jumpcutter.py` — older launcher still around for keeping things compatible with older versions.

---

# Jumpcutter GUI Lietuviškai

„Jumpcutter“ yra darbalaukio programa, skirta tylos fragmentams pašalinti iš paskaitų ar pristatymų, kad vaizdo įrašai būtų trumpesni ir įtraukiantys. Ji veikia su „Tkinter“ grafine sąsaja, naudodama „FFmpeg“, ir savo lange paaiškina, kaip pasirinkti failą, nustatyti parametrus ir pradėti apdorojimą sinchronizuojant garsą su vaizdo įrašu.

## Funkcijos
- Automatiškai aptinka ir iškirpa tylias garso takelio dalis.
- Naudoja „FFmpeg“, kad apdorojimas būtų patikimas ir aukštos kokybės.
- Turi paprastą grafinę sąsają aiškia lietuvių kalba.
- Šaltinio kodas yra padalintas į atskirus pagrindinius ir gui modulius, kad būtų lengviau prižiūrėti ir išplėsti.

## REIKALAVIMAI
- Python 3.8 (ar naujesnis). (Asmeniškai naudojau 3.9 arba 3.11) 
- FFmpeg prienamas sistemos PATH.
-Rekomenduoti naudoti virtualią aplinką priklausomybėms atskirti.

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
1. Įsitikinkite, kad FFmpeg yra įdiegtas ir pasiekiamas iš komandinės eilutės.
2. Paleiskite grafinę sąsają:
   ```bash
   python -m jumpcutter.gui
   ```
3. Lange vadovaukitės lietuviškais nurodymais: pasirinkite įvesties vaizdo įrašą, sureguliuokite tylos slenksčius ir pradėkite apdorojimą.
4. Apdorotas išvesties vaizdo įrašas bus išsaugotas šalia originalaus failo, pašalinus tylias dalis.

## Projekto struktūra
- `jumpcutter/core.py` – apdorojimo eiga: garso analizė, tylos iškirpimas ir galutinio vaizdo įrašymas.
- `jumpcutter/gui.py` – Tkinter sąsaja, kuri surenka naudotojo nustatymus ir paleidžia apdorojimą su paaiškinimais.
- `jumpcutter/__init__.py` – paketo metainformacija ir pagalbinės funkcijos.
- `jumpcutter.py` – senesnis paleidimo scenarijus, paliktas suderinamumui.
