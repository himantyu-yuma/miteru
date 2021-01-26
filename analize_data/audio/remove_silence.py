import glob
import os
import json


def pydub_segment(input_file):
    from pydub import AudioSegment
    import pydub.silence

    def export_chunk(chunks):
        """チャンクを分割してエクスポート

        Args:
            chunks (array): 分割されたチャンク配列
        """
        out_dir = os.path.join(os.path.dirname(input_file).replace('input', 'output/pydub'), os.path.basename(input_file).replace('.wav', ''))
        os.makedirs(out_dir, exist_ok=True)
        for i, chunk in enumerate(chunks):
            out_path = os.path.join(out_dir, f'{i}.wav')
            chunk.export(out_path, format='wav')

    def combine_chunk(chunks):
        """チャンクをまとめてエクスポート

        Args:
            chunks (array): 分割されたチャンク配列
        """
        chunk = chunks[0]
        for i, c in enumerate(chunks):
            if i == 0:
                continue
            chunk += c
        chunk.export(input_file.replace('input', 'output/pydub'), format='wav')

    sound = AudioSegment.from_file(input_file, format="wav")
    chunks = pydub.silence.split_on_silence(
        sound,
        # 1500ms以上の無音がある箇所で分割
        # min_silence_len=1,
        min_silence_len=1000,
        # -30dBFS以下で無音とみなす
        silence_thresh=-40,
        # 分割後500msだけ、無音を残す
        keep_silence=500
    )
    export_chunk(chunks)
    # 発話区間をjsonに書き出し
    non_silent = pydub.silence.detect_nonsilent(
        sound, min_silence_len=1000, silence_thresh=-30)
    non_silentt_dir = [{'speaker': '', 'start': segment_pair[0],
                        'end': segment_pair[1]} for segment_pair in non_silent]
    # print(non_silentt_dir)
    # ディレクトリ作る
    out_dir = os.path.dirname(input_file).replace(
        'input/', 'output/pydub_seg/')
    os.makedirs(out_dir, exist_ok=True)
    filename = os.path.basename(input_file).replace('.wav', '.json')
    out_path = os.path.join(out_dir, filename)
    # jsonファイル作成
    with open(out_path, mode='w', encoding='utf-8') as f:
        json.dump(non_silentt_dir, f, ensure_ascii=False)


def cnn_segment(input_file):
    from inaSpeechSegmenter import Segmenter
    from inaSpeechSegmenter import seg2csv
    from pydub import AudioSegment

    seg = Segmenter(vad_engine='smn', detect_gender=False)

    segmentation = seg(input_file)

    seg2csv(segmentation, input_file.replace(
        'input', 'output/csv').replace('.wav', '.csv'))

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
    # audio_files = glob.glob('input/**/*.wav')
    audio_files = glob.glob('input/exp5/*.wav')
    # pydub_segment(audio_files[0])
    for audio_file in audio_files:
        pydub_segment(audio_file)

    # for audio_file in audio_files:
    #     try:
    #         cnn_segment(audio_file)
    #     except:
    #         print('無理')
    # print(audio_files)

    # modify_json()
