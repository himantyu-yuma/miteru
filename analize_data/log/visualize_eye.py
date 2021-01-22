import cv2
import numpy as np
import datetime
import glob
import json
import re

# img = np.full((720, 1280, 4), 0, dtype=np.uint8)
# # img = cv2.imread('img/rayout.png').copy()

# # 左上→右上
# cv2.arrowedLine(img, (400, 200), (600, 200), (0, 255, 0, 255), thickness=4)
# # 左上→左下
# cv2.arrowedLine(img, (300, 200), (300, 400), (0, 255, 0, 255), thickness=4)

# # 右上→左上
# cv2.arrowedLine(img, (600, 150), (400, 150), (0, 255, 0, 255), thickness=4)
# # 右上→左下
# cv2.arrowedLine(img, (600, 230), (400, 350), (0, 255, 0, 255), thickness=4)

# # 左下→左上
# cv2.arrowedLine(img, (350, 400), (350, 200), (0, 255, 0, 255), thickness=4)
# # 左下→右上
# cv2.arrowedLine(img, (400, 400), (650, 250), (0, 255, 0, 255), thickness=4)

# cv2.imwrite('img/test.png', img)

# test = datetime.datetime.fromisoformat('2021-01-14T04:45:36.398+00:00')
# # print(test.timestamp())

def make_video(dir_name, p_A, p_B, p_C):
    log_files = glob.glob(f'{dir_name}/*.json')
    # log_files = glob.glob('集団1/*.json')
    log_data = []
    # print(log_files)

    for log_file in log_files:
        with open(log_file, mode='r', encoding='utf-8') as f:
            # ログデータをまとまりにする
            log_data += json.load(f)
    # print(log_data)
    # # 左上
    # p_A = '梶\u3000縁'
    # # 右上
    # p_B = '濱田和貴'
    # # 左下
    # p_C = '大内 颯'

    video_name = f'{dir_name}.mp4'
    video = cv2.VideoWriter(
        video_name, cv2.VideoWriter_fourcc(*'MP4V'), 30.0, (1280, 720))
    frame_rate = 30
    m_sec = 1/frame_rate

    # img = np.full((720, 1280, 4), 0, dtype=np.uint8)
    img = np.full((720, 1280, 3), (255, 0, 0), dtype=np.uint8)
    # before_time = datetime.datetime.fromisoformat(
    #     log_data[0]['time'].replace('Z', '+00:00')).timestamp()

    # ログの最初の時間
    init_time = datetime.datetime.fromisoformat(
        log_data[0]['time'].replace('Z', '+00:00')).timestamp()
    before_time = 0
    current_time = 0

    for log in log_data:
        # current_time = datetime.datetime.fromisoformat(
        #    log['time'].replace('Z', '+00:00')).timestamp()

        # current_time = before_time - m_sec
        # log_time = datetime.datetime.fromisoformat(
        #     log['time'].replace('Z', '+00:00')).timestamp()

        # if current_time - before_time < m_sec:
        #     for i in range(int((current_time - before_time)//m_sec)):
        #         video.write(img)

        # before_time = current_time
        # print(log)

        log_time = datetime.datetime.fromisoformat(
            log['time'].replace('Z', '+00:00')).timestamp() - init_time

            
        # if current_time - before_time < m_sec:
        while log_time > current_time:
            video.write(img)
            current_time += 1/frame_rate

        # 矢印を描く
        # 左上→右上
        if log['from'] == p_A and log['to'] == p_B:
            # cv2.arrowedLine(img, (400, 200), (600, 200), (0, 255, 0, 255), thickness=4)
            cv2.arrowedLine(img, (400, 200), (600, 200),
                            (0, 255, 0), thickness=4)
        # 左上→左下
        elif log['from'] == p_A and log['to'] == p_C:
            # cv2.arrowedLine(img, (300, 200), (300, 400), (0, 255, 0, 255), thickness=4)
            cv2.arrowedLine(img, (300, 200), (300, 400),
                            (0, 255, 0), thickness=4)
        # 左上→none
        elif log['from'] == p_A and log['to'] == 'none':
            # cv2.arrowedLine(img, (600, 150), (400, 150), (127, 127, 127, 255), thickness=4)
            # cv2.arrowedLine(img, (300, 200), (300, 400), (127, 127, 127, 255), thickness=4)
            cv2.arrowedLine(img, (400, 200), (600, 200),
                            (127, 127, 127), thickness=4)
            cv2.arrowedLine(img, (300, 200), (300, 400),
                            (127, 127, 127), thickness=4)
        # 右上→左上
        elif log['from'] == p_B and log['to'] == p_A:
            # cv2.arrowedLine(img, (600, 150), (400, 200), (0, 255, 0, 255), thickness=4)
            cv2.arrowedLine(img, (600, 150), (400, 150),
                            (0, 255, 0), thickness=4)
        # 右上→左下
        elif log['from'] == p_B and log['to'] == p_C:
            # cv2.arrowedLine(img, (600, 230), (400, 400), (0, 255, 0, 255), thickness=4)
            cv2.arrowedLine(img, (600, 230), (400, 350),
                            (0, 255, 0), thickness=4)
        # 右上→none
        elif log['from'] == p_B and log['to'] == 'none':
            # cv2.arrowedLine(img, (600, 150), (400, 150), (127, 127, 127, 255), thickness=4)
            # cv2.arrowedLine(img, (600, 230), (400, 350), (127, 127, 127, 255), thickness=4)
            cv2.arrowedLine(img, (600, 150), (400, 150),
                            (127, 127, 127), thickness=4)
            cv2.arrowedLine(img, (600, 230), (400, 350),
                            (127, 127, 127), thickness=4)
        # 左下→左上
        elif log['from'] == p_C and log['to'] == p_A:
            # cv2.arrowedLine(img, (350, 400), (350, 200), (0, 255, 0, 255), thickness=4)
            cv2.arrowedLine(img, (350, 400), (350, 200),
                            (0, 255, 0), thickness=4)
        # 左下→右上
        elif log['from'] == p_C and log['to'] == p_B:
            # cv2.arrowedLine(img, (400, 400), (650, 250), (0, 255, 0, 255), thickness=4)
            cv2.arrowedLine(img, (400, 400), (650, 250),
                            (0, 255, 0), thickness=4)
        # 左下→none
        elif log['from'] == p_C and log['to'] == 'none':
            # cv2.arrowedLine(img, (350, 400), (350, 200), (127, 127, 127, 255), thickness=4)
            # cv2.arrowedLine(img, (400, 400), (650, 250), (127, 127, 127, 255), thickness=4)
            cv2.arrowedLine(img, (350, 400), (350, 200),
                            (127, 127, 127), thickness=4)
            cv2.arrowedLine(img, (400, 400), (650, 250),
                            (127, 127, 127), thickness=4)
        # else:
        #     continue
        # f_name = re.sub('\.', '-', str(current_time))
        # print(f_name)
        # break
        # cv2.imwrite(f'img/test/{f_name}.png', img)
        # video.write(img)
        # before_time = current_time

    video.release()


if __name__ == "__main__":
    # make_video('集団1', '小山　悠斗'.replace('　', '\u3000'), '中西　芽衣'.replace('　', '\u3000'), '工藤　輝空'.replace('　', '\u3000'))
    make_video('集団2', '米川　大樹'.replace('　', '\u3000'), '武市'.replace('　', '\u3000'), '奥山和樹'.replace('　', '\u3000'))
    make_video('集団5', '廣吉和貴'.replace('　', '\u3000'), '佐々木凜'.replace('　', '\u3000'), '岡田絢音'.replace('　', '\u3000'))
    make_video('集団6', '梶　縁'.replace('　', '\u3000'), '濱田和貴'.replace('　', '\u3000'), '大内 颯'.replace('　', '\u3000'))