from pydub import AudioSegment
import glob
import csv


def count_duration():
    audio_files = glob.glob('output/pydub/**/*.wav')

    with open('pydub_duration.csv', mode='w', encoding='utf-8', newline='') as f:
        for audio_file in audio_files:
            print(audio_file)
            sound = AudioSegment.from_file(audio_file, 'wav')

            time = sound.duration_seconds
            writer = csv.writer(f)
            column = audio_file.replace(
                'output/pydub\\', '').replace('.wav', '').split('\\')
            writer.writerow([column[0], column[1], time])


if __name__ == "__main__":
    count_duration()
