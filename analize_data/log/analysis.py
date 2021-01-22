import json
import glob
import collections

log_files = glob.glob('log/集団6/*.json')

log_data = []

for log_file in log_files:
    with open(log_file, mode='r', encoding='utf-8') as f:
        # ログデータをまとまりにする
        log_data += json.load(f)
print(len(log_data))

def part_from():
    # from毎に分けてみる
    same_from = {}
    for log in log_data:
        if log['from'] not in same_from:
            same_from[log['from']] = []

        same_from[log['from']].append({'time': log['time'], 'to': log['to']})
    return same_from
    # with open('test.json', mode='w', encoding='utf-8') as f:
        # json.dump(same_from, f, indent=4, ensure_ascii=False)


def count_look():
    # 誰が誰を何回見ているか
    count_json = {}
    same_from = part_from()
    for from_name in same_from:
        to_array = [to_name['to'] for to_name in same_from[from_name]]
        to_count = collections.Counter(to_array)
        count_json[from_name] = dict(to_count)
    # print(count_json)
    return count_json


def pairplot_count():
    # 散布図行列作成してみる
    # 特に意味無さそう
    import pandas as pd
    import seaborn as sns
    from matplotlib import pyplot as plt

    df = pd.DataFrame.from_dict(count_look(), orient='index').T
    sns.pairplot(df)
    plt.show()


def direct_network():
    import networkx as nx
    import math
    # ネットワークとして可視化してみる
    # 有向グラフにして，矢印の太さ変えてみる
    weight_list = []
    raw_data = count_look()
    # none消す
    for item in raw_data:
        del raw_data[item]['none']
    for datum in raw_data:
        tmp_arr = [(datum, x, raw_data[datum][x]) for x in raw_data[datum]]
        weight_list += tmp_arr
    # print(weight_list)
    # G = nx.DiGraph()
    G = nx.MultiDiGraph()
    G.add_weighted_edges_from(weight_list)

    # print(G.edges(data=True))

    # pos = nx.spring_layout(G, k=1)
    pos = dict()
    half = math.floor(len(list(raw_data.keys()))/2)
    left_side = list(raw_data.keys())[:half]
    right_side = list(raw_data.keys())[half:]
    pos.update((n, (1, i)) for i,n in enumerate(left_side))
    pos.update((n, (2, i)) for i,n in enumerate(right_side))
    print(pos)
    
    weight_sum = sum([x[2] for x in weight_list])
    edge_width = [x[2] / weight_sum * 100 for x in weight_list]
    print(edge_width)
    nx.draw_networkx_labels(G, pos, font_size=14,
                            font_family='Yu Gothic', font_weight='bold')
    nx.draw_networkx_edges(G, pos, alpha=0.4, edge_color='c', width=edge_width)

    from matplotlib import pyplot as plt
    # nx.draw_networkx(G)
    plt.show()

# target: 集計するtoの人
def plot_time(target):
    import matplotlib.pyplot as plt
    # fromが同じ人でわける
    same_from = part_from()
    plot_data = {}
    for _from in same_from:
        plot_data[_from] = []
    plt.plot(x, y1, marker="o", color = "red", linestyle = "--")
    plt.show()

# if __name__ == "__main__":
    # count_look()
    # print(count_look())
    # with open('out.json', mode='w', encoding='utf-8') as f:
        # json.dump(count_look(), f, indent=4, ensure_ascii=False)
    # pairplot_count()
    # direct_network()
    # plot_time('笠原')
