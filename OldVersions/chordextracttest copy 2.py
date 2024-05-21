import csv
import subprocess
import os
from chord_extractor.extractors import Chordino

def convert_midi_to_wav(midi_file, soundfont_file, output_file):
    # Construct the FluidSynth command line command
    command = f'fluidsynth -ni "{soundfont_file}" "{midi_file}" -F "{output_file}" -r 44100'
    try:
        # Execute the command
        subprocess.run(command, check=True, shell=True)
        print("MIDI to WAV conversion successful.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to convert MIDI to WAV: {e}")

def main():
    # Initialize Chordino
    chordino = Chordino()

    file_path = r'Lana Del Rey - Summertime Sadness (Lyrics).mp3'
    
    # Determine if the file is MIDI and convert to WAV if true
    if file_path.endswith('.mid'):
        soundfont_file = r'N:\ChordExtract Test\GeneralUser GS 1.471\GeneralUser GS v1.471.sf2'
        wav_file_path = file_path[:-4] + '.wav'  # Change MIDI file extension to WAV
        convert_midi_to_wav(file_path, soundfont_file, wav_file_path)
        audio_file_path = wav_file_path
    else:
        audio_file_path = file_path

    # Check if the WAV file was actually created
    if not os.path.exists(audio_file_path):
        print("Conversion failed, WAV file was not created.")
        return

    # Extract chords using Chordino
    chords = chordino.extract(audio_file_path)

    # User input for time signature and tempo
    time_signature = input("Enter the time signature (e.g., 4/4, 6/8): ")
    beats_per_bar, base = map(int, time_signature.split('/'))
    tempo = int(input("Enter the BPM (Tempo): "))
    seconds_per_beat = 60 / tempo

    output_format = 'time-based' if base != 4 else 'beat-based'

    csv_path = 'music_data.csv'

    with open(csv_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["useBase1"])
        writer.writerow([f"timeSignature={time_signature}"])
        writer.writerow([f"tempoBPM={tempo}"])

        for chord in chords:
            if chord.chord != 'N':  # Skip 'N' chords
                time_from_first = chord.timestamp - chords[0].timestamp
                if output_format == 'time-based':
                    pos_in_seconds = round(time_from_first)  # Round to nearest whole second
                    writer.writerow([pos_in_seconds, chord.chord])
                else:
                    total_beats = time_from_first / seconds_per_beat
                    bar = int(total_beats // beats_per_bar) + 1
                    beat = round(total_beats % beats_per_bar) + 1  # Round to nearest whole beat
                    if beat > beats_per_bar:
                        beat = 1
                        bar += 1
                    writer.writerow([bar, beat, chord.chord])

    print(f'Data written to {csv_path}')

if __name__ == '__main__':
    main()
