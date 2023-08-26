import os
import magenta.music as mm
from magenta.models.melody_rnn import melody_rnn_sequence_generator

output_dir = 'generated_music'
os.makedirs(output_dir, exist_ok=True)

model_name = 'attention_rnn'
melody_rnn = melody_rnn_sequence_generator.MelodyRnnSequenceGenerator(model_name=model_name)

temperature = 1.0
num_music_pieces = 3
steps_per_music_piece = 128

try:
    preferred_genre = input("Enter your preferred genre (e.g., classical, jazz, rock): ")
    preferred_tempo = int(input("Enter your preferred tempo (BPM): "))
except ValueError:
    print("Invalid input. Using default values.")
    preferred_genre = "classical"
    preferred_tempo = 120

chord_progressions = {
    "classical": ["C", "Am", "F", "G"],
    "jazz": ["Cmaj7", "Dm7", "Em7", "A7"],
    "rock": ["C", "G", "Am", "F"],
}

drum_pattern = mm.DrumTrack([36, 0, 42, 0, 36, 0, 42, 0],
                            start_step=0,
                            steps_per_bar=steps_per_music_piece // 4,
                            steps_per_quarter=4)

for i in range(num_music_pieces):
    try:
        melody_sequence = melody_rnn.generate(temperature=temperature,
                                              steps=steps_per_music_piece,
                                              primer_sequence=None)

        chords = [chord_progressions.get(preferred_genre, ["C"])[i % len(
            chord_progressions.get(preferred_genre, ["C"]))] for i in range(steps_per_music_piece)]
        chord_sequence = mm.ChordSequence(chords)
        melody_with_chords_sequence = mm.sequences_lib.concatenate_sequences(
            melody_sequence, chord_sequence)

        music_sequence = mm.sequences_lib.concatenate_sequences(
            melody_with_chords_sequence, drum_pattern)
        music_sequence.tempos[0].qpm = preferred_tempo

        midi_file = os.path.join(output_dir, f'music_piece_{i + 1}.mid')
        mm.sequence_proto_to_midi_file(music_sequence, midi_file)
        print(f'Music piece {i + 1} generated and saved as {midi_file}')
    except Exception as e:
        print(f"An error occurred while generating music piece {i + 1}: {e}")

print('Music generation complete!')
