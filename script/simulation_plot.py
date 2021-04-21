import json
from os.path import dirname, abspath

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

ATTACK_START, ATTACK_END, LOG_FILE = None, None, abspath(f"{dirname(__file__)}/../logs/certification_logs.json")
ATTACK_START, ATTACK_END, LOG_FILE = 276, 283, abspath(f"{dirname(__file__)}/../logs/attack_logs.json")
ATTACK_START, ATTACK_END, LOG_FILE = None, None, abspath(f"{dirname(__file__)}/../logs/execution_new_rule.json")
ATTACK_START, ATTACK_END, LOG_FILE = 380, 390, abspath(f"{dirname(__file__)}/../logs/attack_new_rule.json")

METRICS = [f"M{i + 1}" for i in range(12)]
METRICS.remove("M5")


def plot_attack_lines():
    if ATTACK_START is not None and ATTACK_END is not None:
        return [plt.axvline(x=ATTACK_START, c="k", linestyle="dashed", linewidth=1,
                            label=f"Attack start"),
                plt.axvline(x=ATTACK_END, c="k", linestyle="dotted", linewidth=1,
                            label=f"Attack end")]
    else:
        return []


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
                for metric in METRICS}

    evaluations = {task: [data["evaluations_index"][task][str(i)] for i in indexes] for task in
                   tasks}

    plt.subplots(nrows=2, ncols=1, sharex="col")
    plt.subplot(2, 1, 1)
    # plt.plot(indexes, measures["M1"], label="M1")
    if ATTACK_START is not None:
        plt.plot(indexes, measures["M2"], label="M2, M3", c="k", linestyle="dotted")
    else:
        plt.plot(indexes, measures["M2"], label="M2", c="k", linestyle="dotted")
        plt.plot(indexes, measures["M3"], label="M3", c="k", linestyle="dashed")
    plt.plot(indexes, list(map(lambda m: m["avg"], measures["M4"])), label="M4 avg", c="k", linestyle="dashdot")
    plt.plot(indexes, list(map(lambda m: m["stdDev"], measures["M4"])), label="M4 std dev", c="k", linestyle="solid")
    if ATTACK_START is not None:
        plt.plot(indexes, list(map(lambda m: min(m[i]["min"] for i in m.keys()), measures["M8"])), label="M8 min",
                 c="k", linestyle="dashed")
    plot_attack_lines()
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0, wspace=0, hspace=0)
    plt.ylabel("Metric", loc="top")
    plt.xlim((min_index, max_index))
    plt.legend(bbox_to_anchor=(0, 1, 1, 0), loc="lower left", mode="expand", ncol=3)
    plt.semilogy()

    # plt.plot(indexes, list(map(lambda m: sum(m.values()), measures["M6"])), label="M6 sum", c="k", linestyle="--")
    # # plt.plot(indexes, measures["M4_STD_DEV"], label="M4 std dev", c="k", linestyle="-")
    # plot_attack_lines()
    # plt.xlabel("Time (s)", loc="right")
    # plt.ylabel("Metric", loc="top")
    # plt.legend()
    # plt.tight_layout()

    plt.subplot(2, 1, 2)
    if ATTACK_START is not None:
        tasks = ["C5", "C6", "C7", "C11", "R2", "R5", "P1"]
    else:
        tasks = ["C4", "C5", "C6", "R2", "P1"]
    data = [[int(v) for v in evaluations[k]] for k in tasks]
    plt.imshow(data, interpolation="nearest", aspect=len(indexes) / 35,
               cmap=ListedColormap(["k", "w"]))
    for i, t in enumerate(tasks):
        plt.axhline(y=0.5 + i, c="k", linewidth=0.5, linestyle="dashed")
    lines = plot_attack_lines()
    # patches = [Patch(facecolor=COLORS[c], label=f"{v}", edgecolor="k") for v, c in VALUES.items()]
    # plt.legend(handles=patches + lines)
    plt.yticks(range(len(tasks)), tasks)
    plt.xlabel("Time (s)", loc="right")
    plt.ylabel("Task", loc="top")
    plt.tight_layout()
    if ATTACK_START is not None:
        plt.savefig("../plots/attack.pdf", format="pdf")
        plt.savefig("../plots/attack.png", format="png")
    else:
        plt.savefig("../plots/certification.pdf", format="pdf")
        plt.savefig("../plots/certification.png", format="png")
    plt.show()
