**Audio Analysis and Chord Extraction Application**
This project contains two main components for analyzing audio files and extracting chord information:

Chord Extract.py: A GUI-based application for extracting chords from audio files using the Chordino library.
FileAnalysis.py: A script for analyzing audio features and computing similarity between two audio tracks using Librosa.
Requirements
To run these scripts, you will need the following Python packages:

tkinter
librosa
matplotlib
numpy
scipy
chord_extractor
fluidsynth (for MIDI to WAV conversion)
You can install the necessary Python packages using pip:

bash
Copy code
pip install tkinter librosa matplotlib numpy scipy chord_extractor
Additional Software
For MIDI to WAV conversion, you need to install fluidsynth. You can download and install it from here.

Usage
Chord Extract.py
This is a GUI-based application that allows you to extract chord information from an audio file. It supports MP3, WAV, and MIDI files. For MIDI files, you need to provide a SoundFont file for conversion to WAV.

How to Run
Ensure you have all the required packages installed.

Run the script:

bash
Copy code
python Chord\ Extract.py
Features
File Selection: Select an audio file (MP3, WAV, MIDI) for chord extraction.
SoundFont Selection: If using a MIDI file, select a SoundFont file for conversion.
Time Signature: Input the time signature (e.g., 4/4).
Tempo: Input the tempo in BPM (Beats Per Minute).
Extract Chords: Extract chords and save the results to a CSV file.
FileAnalysis.py
This script analyzes audio features and computes similarity between two audio tracks. It uses the Librosa library for feature extraction and Matplotlib for plotting.

How to Run
Ensure you have all the required packages installed.

Update the original_path and backing_path variables with the paths to your audio files.

Run the script:

bash
Copy code
python FileAnalysis.py
Features
Load and Extract Features: Load audio files and extract features like MFCCs, Harmonics, Spectral Contrast, Chroma, and Tonnetz.
Compute Similarity: Compute similarity scores between two audio tracks.
Plot Features: Plot and save the extracted features.
Plot Similarity Scores: Plot and save the similarity scores.
