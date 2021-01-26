import matplotlib.pyplot as plt
import numpy as np
import glob
import json
import datetime

import soundfile as sf


def combine_log(log_files):
    log_data = []
    for i, log_file in enumerate(log_files):
        with open(log_file, mode='r', encoding='utf-8') as f:
            log_data += json.load(f)
        # if i == 4:
        #     break
    return log_data


def convert_time(iso_time):
    return datetime.datetime.fromisoformat(iso_time.replace('Z', '+00:00')).timestamp()


def count_look(log_data, target, first_time):
    # y = [1 if data['to'] == '笠原有真' else 0 for data in log_data]
    y = []
    x = []
    look_count = 0
    # targetを見てる人
    lookers = []
    # target = '工藤　輝空'
    # target = '小山　悠斗'
    # target = '中西　芽衣'
    # target = '梶　縁'
    for data in log_data:
        _to = data['to']
        _from = data['from']
        _time = data['time']

        # print(convert_time(_time) - first_time)
        if convert_time(_time) - first_time >= 120:
            break
        # first_time以下だったらパス
        if convert_time(_time) - first_time < 0:
            continue
        # # to|fromが笠原　fromがtargetだったらパス
        # if '笠原' in _to or '笠原' in _from or _from == target:
        #     # pass
        #     continue
        # elif _to == 'none' and _from not in lookers:
        if _to == 'none' and _from not in lookers:
            continue
        elif _to == target and '笠原' not in _from:
            look_count += 1
            lookers.append(_from)
        elif _to == 'none' and _from in lookers:
            lookers.remove(_from)
            look_count -= 1
        else:
            continue
        y.append(look_count)
        x.append(convert_time(_time) - first_time)

    return (x, y)


def plot_wave(audio_file):
    data, samplerate = sf.read(audio_file)
    t = np.arange(0, len(data))/samplerate
    return (t, data)
    # plt.figure(figsize=(18, 6))
    # plt.plot(t, data)
    # plt.show()


def plot_speak(speaker_tag):
    x = []
    speaker_file = glob.glob('../audio/output/pydub_seg/**/視線有*.json')
    with open(speaker_file, mode='r', encoding='utf-8') as f:
        speaker_data = json.load(f)
    for datum in speaker_data:
        if datum['speaker'] == speaker_tag:
            x.append((datum['start'], datum['end']))
    return x


if __name__ == "__main__":
    # exp1
    log_files = glob.glob('集団1/*.json')
    participants = ('工藤　輝空', '小山　悠斗', '中西　芽衣')
    audio_files = glob.glob('../audio/input/exp1/視線有*.wav')
    speaker_files = glob.glob('../audio/output/pydub_seg/exp1/視線有*.json')
    diff_times = (620.8, 911.3, 1151.766)
    main_title = '集団1'

    # # exp2
    # log_files = glob.glob('集団2/*.json')
    # participants = ('奥山和樹', '武市', '米川　大樹')
    # audio_files = glob.glob('../audio/input/exp2/視線有*.wav')
    # speaker_files = glob.glob('../audio/output/pydub_seg/exp2/視線有*.json')
    # diff_times = (415.8, 672.2, 898.233)
    # main_title = '集団2'

    # # exp5
    # log_files = glob.glob('集団5/*.json')
    # participants = ('岡田絢音', '佐々木凜', '廣吉和貴')
    # audio_files = glob.glob('../audio/input/exp5/視線有*.wav')
    # speaker_files = glob.glob('../audio/output/pydub_seg/exp5/視線有*.json')
    # diff_times = (367.3, 637.6, 842.867)
    # main_title = '集団5'

    # # exp6
    # log_files = glob.glob('集団6/*.json')
    # participants = ('大内 颯', '梶　縁', '濱田和貴')
    # audio_files = glob.glob('../audio/input/exp6/視線有*.wav')
    # speaker_files = glob.glob('../audio/output/pydub_seg/exp6/視線有*.json')
    # diff_times = (460.266, 722.7, 1039.033)
    # main_title = '集団6'

    sub_titles = ['視線有1', '視線有2', '視線有3']
    # フォント
    font = {'family': 'Yu Gothic'}

    # ループ用のやつ
    tmp_zip = zip(audio_files, diff_times, sub_titles, speaker_files)
    for (audio_file, diff_time, sub_title, speaker_file) in tmp_zip:
        # audio_file = audio_files[0]
        # diff_time = diff_times[0]
        # graph_title = main_titles[0] + sub_titles[0]
        graph_title = main_title + sub_title

        # ログをひとまとめにする
        log_data = combine_log(log_files)

        # 図のサイズとか行数とか定義
        fig, ax = plt.subplots(3, 1, figsize=(18, 6))
        fig.suptitle(graph_title, **font)

        first_time = convert_time(log_data[0]['time']) + diff_time
        # 時間，波形のタプル
        audio_data = plot_wave(audio_file)

        # plotするデータを取得
        plot_data = [count_look(log_data, participant, first_time)
                     for participant in participants]
        speaker_data = [plot_speak(speaker) for speaker in participants]
        print(speaker_files)

        # x1, y1 = count_look(log_data, participant_a, first_time)
        # x2, y2 = count_look(log_data, participant_b, first_time)
        # x3, y3 = count_look(log_data, participant_c, first_time)
        graph_data = zip(ax, plot_data, participants, speaker_data)
        for (axe, data, participant, spd) in graph_data:
            axe.set_title(participant, **font)
            axe.set_ylim(0, 2)
            axe.plot(audio_data[0], audio_data[1])
            axe.plot(data[0], data[1], marker='.', linestyle='None')
            for v in spd:
                axe.axvspan(v[0]/1000, v[1]/1000)

        # ax[0].plot(audio_data[0], audio_data[1])
        # ax[0].plot(x1, y1, marker='.', linestyle='None')

        # ax[1].plot(audio_data[0], audio_data[1])
        # ax[1].plot(x2, y2, marker='.', linestyle='None')

        # ax[2].plot(audio_data[0], audio_data[1])
        # ax[2].plot(x3, y3, marker='.', linestyle='None')

        # plt.set_yticks([-1, 0, 1, 2])

        plt.tight_layout()
        # plt.show()
        plt.savefig(f"image/{graph_title}.png")
        # fig.show()
