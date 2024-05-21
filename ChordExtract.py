import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import csv
import subprocess
import os
from chord_extractor.extractors import Chordino

# Utility functions
def round_to_nearest_half(num):
    return round(num * 2) / 2

def convert_midi_to_wav(midi_file, soundfont_file, output_file):
    command = f'fluidsynth -ni "{soundfont_file}" "{midi_file}" -F "{output_file}" -r 44100'
    try:
        subprocess.run(command, check=True, shell=True)
        print("MIDI to WAV conversion successful.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to convert MIDI to WAV: {e}")

# Main application class
class ChordExtractApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chord Extractor")
        self.root.geometry("700x500")
        self.setup_style()
        self.setup_ui()
        self.file_path = ""
        self.soundfont_path = ""

    def setup_style(self):
        style = ttk.Style(self.root)
        self.root.tk.call("source", "azure.tcl")  # Correctly source the Azure theme file
        self.root.tk.call("set_theme","dark")  # Set the theme to 'light' or 'dark'
        style.configure("TButton", font=("Helvetica", 12), padding=10)
        style.configure("TLabel", font=("Helvetica", 12))
        style.configure("TEntry", font=("Helvetica", 12))

    def setup_ui(self):
        self.frame = ttk.Frame(self.root, padding=20)
        self.frame.place(relwidth=1, relheight=1)

        self.label = ttk.Label(self.frame, text="Drag and Drop your song file here", anchor="center")
        self.label.pack(pady=20, fill=tk.X)

        self.button = ttk.Button(self.frame, text="Select File", command=self.browse_file)
        self.button.pack(pady=10)

        self.soundfont_button = ttk.Button(self.frame, text="Select SoundFont File", command=self.browse_soundfont)
        self.soundfont_button.pack(pady=10)

        self.time_signature_label = ttk.Label(self.frame, text="Time Signature (e.g., 4/4):")
        self.time_signature_label.pack(pady=5)
        self.time_signature_entry = ttk.Entry(self.frame)
        self.time_signature_entry.pack(pady=5)

        self.tempo_label = ttk.Label(self.frame, text="Tempo (BPM):")
        self.tempo_label.pack(pady=5)
        self.tempo_entry = ttk.Entry(self.frame)
        self.tempo_entry.pack(pady=5)

        self.extract_button = ttk.Button(self.frame, text="Extract Chords", command=self.extract_chords)
        self.extract_button.pack(pady=20)

    def browse_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav *.mid")])
        self.label.config(text=self.file_path)

    def browse_soundfont(self):
        self.soundfont_path = filedialog.askopenfilename(filetypes=[("SoundFont Files", "*.sf2")])
        if self.soundfont_path:
            messagebox.showinfo("SoundFont Selected", f"SoundFont file selected: {self.soundfont_path}")

    def extract_chords(self):
        if not self.file_path:
            messagebox.showwarning("No file selected", "Please select an audio file to extract chords from.")
            return

        if self.file_path.endswith('.mid') and not self.soundfont_path:
            messagebox.showwarning("No SoundFont selected", "Please select a SoundFont file to convert MIDI to WAV.")
            return

        time_signature = self.time_signature_entry.get()
        tempo = self.tempo_entry.get()

        if not time_signature or not tempo:
            messagebox.showwarning("Missing Information", "Please enter both time signature and tempo.")
            return

        beats_per_bar, base = map(int, time_signature.split('/'))
        tempo = int(tempo)
        seconds_per_beat = 60 / tempo
        output_format = 'time-based' if base != 4 else 'beat-based'

        chordino = Chordino()

        if self.file_path.endswith('.mid'):
            wav_file_path = self.file_path[:-4] + '.wav'
            convert_midi_to_wav(self.file_path, self.soundfont_path, wav_file_path)
            audio_file_path = wav_file_path
        else:
            audio_file_path = self.file_path

        if not os.path.exists(audio_file_path):
            messagebox.showerror("Error", "WAV file conversion failed.")
            return

        chords = chordino.extract(audio_file_path)

        csv_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if not csv_path:
            messagebox.showwarning("No file selected", "Please select a location to save the CSV file.")
            return

        with open(csv_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["useBase1"])
            writer.writerow([f"timeSignature={time_signature}"])
            writer.writerow([f"tempoBPM={tempo}"])

            for chord in chords:
                if chord.chord != 'N':
                    time_from_first = chord.timestamp - chords[0].timestamp
                    if output_format == 'time-based':
                        pos_in_seconds = round_to_nearest_half(time_from_first)
                        writer.writerow([pos_in_seconds, chord.chord])
                    else:
                        total_beats = time_from_first / seconds_per_beat
                        bar = int(total_beats // beats_per_bar) + 1
                        beat = int(total_beats % beats_per_bar) + 1
                        if beat > beats_per_bar:
                            beat = 1
                            bar += 1
                        writer.writerow([bar, beat, chord.chord])

        messagebox.showinfo("Success", f"Chords extracted and saved to {csv_path}")

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = ChordExtractApp(root)
    root.mainloop()
