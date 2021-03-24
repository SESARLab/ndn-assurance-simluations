import json
from os.path import dirname, abspath

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

LOG_FILE = abspath(f"{dirname(__file__)}/../logs/attack_logs.json")
COLORS = {
    "blue": "#5E81AC",
    "green": "#A3BE8C",
    "orange": "#D08770",
    "purple": "#B48EAD",
    "red": "#BF616A",
    "yellow": "#EBCB8B",
}

if __name__ == '__main__':
    with open(LOG_FILE) as f:
        data = {k: v for k, v in json.load(f).items() if "index" in k}

    tasks = ["C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8",
             "C9", "C10", "C11", "C12", "C13", "C14",
             "R1", "R2", "R3", "R4", "R5", "R6", "R7",
             "P1", "P2", "P3"]
    indexes = list(sorted(map(int, data["evaluations_index"]["P1"].keys())))
    min_index, max_index = min(indexes), max(indexes)

    measures = {metric: [data["measurements_index"][metric][str(i)][metric] for i in range(min_index, max_index + 1)]
                for metric in ["M1", "M2", "M3"]}
    measures["M4_AVG"] = [data["measurements_index"]["M4"][str(i)]["M4"]["avg"] for i in
                          range(min_index, max_index + 1)]
    measures["M4_STD_DEV"] = [data["measurements_index"]["M4"][str(i)]["M4"]["stdDev"] for i in
                              indexes]

    plot_data = {task: [data["evaluations_index"][task][str(i)] for i in indexes] for task in
                 tasks}

    final = [plot_data["P1"][i] and plot_data["P2"][i] and plot_data["P3"][i] for i in indexes]

    plt.subplots(nrows=2, ncols=1, sharex="col")
    plt.subplot(2, 1, 1)
    # plt.plot(indexes, measures["M1"], label="M1")
    plt.plot(indexes, measures["M2"], label="M2", c=COLORS["orange"])
    plt.plot(indexes, measures["M3"], label="M3", c=COLORS["green"])
    plt.legend()
    plt.subplot(2, 1, 2)
    plt.plot(indexes, measures["M4_AVG"], label="M4 avg", c=COLORS["blue"])
    plt.plot(indexes, measures["M4_STD_DEV"], label="M4 std dev", c=COLORS["red"])
    plt.legend()
    plt.show()

    data = [[int(v) for v in plot_data[k]] for k in tasks]
    plt.imshow(data, interpolation="nearest", aspect=len(indexes) / 35,
               cmap=ListedColormap([COLORS["orange"], COLORS["blue"]]))
    plt.yticks(range(len(tasks)), tasks)
    plt.show()
