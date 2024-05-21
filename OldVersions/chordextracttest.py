import csv
from chord_extractor.extractors import Chordino

def round_to_nearest_half(num):
    return round(num * 2) / 2

def main():
    # Initialize Chordino
    chordino = Chordino()

    # Replace this with the actual path to your audio file
    audio_file_path = 'N:\ChordExtract Test\Lana Del Rey - Summertime Sadness (Lyrics).mp3'

    # Extract chords
    chords = chordino.extract(audio_file_path)

    # User input for time signature and tempo
    time_signature = input("Enter the time signature (e.g., 4/4, 6/8): ")
    beats_per_bar, base = map(int, time_signature.split('/'))
    tempo = int(input("Enter the BPM (Tempo): "))
    seconds_per_beat = 60 / tempo

    # Determine the output format based on the time signature base
    output_format = 'time-based' if base != 4 else 'beat-based'

    # Path to the CSV file
    csv_path = 'music_data.csv'

    with open(csv_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write header information based on the selected format
        writer.writerow(["useBase1"])
        writer.writerow([f"timeSignature={time_signature}"])
        writer.writerow([f"tempoBPM={tempo}"])

        for chord in chords:
            if chord.chord != 'N':  # Skip 'N' chords
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

    print(f'Data written to {csv_path}')

if __name__ == '__main__':
    main()
