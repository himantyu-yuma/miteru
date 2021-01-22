import glob


def pydub_segment(input_file):
    from pydub import AudioSegment
    from pydub.silence import split_on_silence

    sound = AudioSegment.from_file(input_file, format="wav")
    chunks = split_on_silence(
        sound,
        # 1500ms以上の無音がある箇所で分割
        min_silence_len=1,
        # -30dBFS以下で無音とみなす
        silence_thresh=-30,
        # 分割後500msだけ、無音を残す
        keep_silence=0
    )

    chunk = chunks[0]

    for i, c in enumerate(chunks):
        if i == 0:
            continue
        chunk += c

    # 分割数の表示
    # print(chunks)

    chunk.export(input_file.replace('input', 'output/pydub'), format='wav')


def cnn_segment(input_file):
    from inaSpeechSegmenter import Segmenter
    from inaSpeechSegmenter import seg2csv
    from pydub import AudioSegment

    seg = Segmenter(vad_engine='smn', detect_gender=False)

    segmentation = seg(input_file)

    seg2csv(segmentation, input_file.replace('input', 'output/csv').replace('.wav', '.csv'))

    # print(segmentation)

    out_audio = AudioSegment.from_wav(input_file)[0:0]

    speech_segment_index = 0
    for segment in segmentation:
        # segmentはタプル
        # タプルの第1要素が区間のラベル
        segment_label = segment[0]

        if (segment_label == 'speech'):  # 音声区間

            # 区間の開始時刻の単位を秒からミリ秒に変換
            start_time = segment[1] * 1000
            end_time = segment[2] * 1000

            # 分割結果をwavに出力
            newAudio = AudioSegment.from_wav(input_file)
            out_audio += newAudio[start_time:end_time]

    out_audio.export(input_file.replace('input', 'output/cnn'), format='wav')


if __name__ == "__main__":
    audio_files = glob.glob('input/**/*.wav')
    for audio_file in audio_files:
        pydub_segment(audio_file)
    for audio_file in audio_files:
        try:
            cnn_segment(audio_file)
        except:
            print('無理')
    # print(audio_files)