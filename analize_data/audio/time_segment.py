# 無音区間or発話区間の合計時間を計測
import csv
import glob


def time_speech(reader):
    time = 0
    for row in reader:
        if row[0] == 'speech':
            time += float(row[2]) - float(row[1])
    return time


def time_not_speech(reader):
    time = 0
    for row in reader:
        if not row[0] == 'speech':
            time += float(row[2]) - float(row[1])
    return time


def check_diff(arr):
    # 一旦辞書形式でまとめる
    data = {}
    for row in arr:
        key = row[0]
        if key not in data:
            data[key] = {}
        data[key][row[1].replace('.csv', '')] = row[2]
    # print(data)
    for key, items in data.items():
        # print('session1', items['視線有1'] - items['視線無1'])
        # print('session2', items['視線有2'] - items['視線無2'])
        # print('session3', items['視線有3'] - items['視線無3'])
        print(key, items['視線有1'] + items['視線有2'] + items['視線有3'] -
                items['視線無1'] - items['視線無2'] - items['視線無3'])


if __name__ == "__main__":
    speech_time_arr = []
    silence_time_arr = []
    csv_files = glob.glob('output/csv/**/*.csv')
    for csv_file in csv_files:
        with open(csv_file, mode='r', encoding='utf-8', newline='') as f:
            h = next(csv.reader(f, delimiter='\t'))
            reader = list(csv.reader(f, delimiter='\t'))
        row = [csv_file.split('/')[-2], csv_file.split('/')
               [-1], time_not_speech(reader)]
        silence_time_arr.append(row)
        row = [csv_file.split('/')[-2], csv_file.split('/')
               [-1], time_speech(reader)]
        speech_time_arr.append(row)
        # print(csv_file, time_speech(reader))

    print('speech time:')
    check_diff(speech_time_arr)
    print('silence time:')
    check_diff(silence_time_arr)

    with open('output/csv/speech_time.csv', mode='w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(speech_time_arr)
    with open('output/csv/silence_time.csv', mode='w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(silence_time_arr)

    # check_diff(time_arr)
