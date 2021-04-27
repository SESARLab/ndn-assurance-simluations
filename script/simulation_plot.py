import json
from os.path import dirname, abspath
from typing import List, Dict, Any
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np
import pandas as pd

tasks, S_START, S_END, ATTACK_START, ATTACK_END, LOG_FILE = (
    ["C4", "C5", "C6", "R2", "P1"],
    None,
    400,
    None,
    None,
    abspath(f"{dirname(__file__)}/../logs/execution_new_rule.json"),
)
tasks, S_START, S_END, ATTACK_START, ATTACK_END, LOG_FILE = (
    ["C6", "C7", "C11", "R2", "R5", "P1"],
    200,
    650,
    249,
    259,
    abspath(f"{dirname(__file__)}/../logs/attack_new_rule.json"),
)

METRICS = [f"M{i + 1}" for i in range(12)]
METRICS.remove("M5")

METRICS = [f"M{i + 1}" for i in range(12)]
TASKS = (
    [f"C{i+1}" for i in range(15)]
    + [f"R{i+1}" for i in range(8)]
    + [f"P{i+1}" for i in range(3)]
)


def vertical_lines(ax=None):
    if ATTACK_START is None:
        return
    if ax is None:
        ax = plt
    ax.axvline(
        x=ATTACK_START, c="k", linestyle="dashed", linewidth=1, label="Attack start"
    ),
    ax.axvline(x=ATTACK_END, c="k", linestyle="dotted", linewidth=1, label="Attack end")


def access(path: List[str], dictionary: Dict[str, Any], default=np.NaN) -> Any:
    try:
        if len(path) == 0:
            return dictionary
        else:
            return access(path=path[1:], dictionary=dictionary[path[0]])
    except KeyError:
        return default


def access_min(path: List[str], dictionary: Dict[str, Any], default=np.NaN) -> Any:
    acc_dict = access(path=path, dictionary=dictionary, default=default)
    try:
        return min(map(lambda d: d["min"], acc_dict.values()))
    except:
        return default


if __name__ == "__main__":
    if tasks is None:
        tasks = TASKS

    with open(LOG_FILE) as f:
        data = {k: v for k, v in json.load(f).items() if "index" in k}

    measurements_data = (
        pd.DataFrame.from_dict(
            {
                i: {
                    "M2": access(["measurements_index", "M2", str(i), "M2"], data),
                    "M3": access(["measurements_index", "M3", str(i), "M3"], data),
                    "M4 avg": access(
                        ["measurements_index", "M4", str(i), "M4", "avg"], data
                    ),
                    "M4 stdDev": access(
                        ["measurements_index", "M4", str(i), "M4", "stdDev"], data
                    ),
                    "M8 min": access_min(
                        ["measurements_index", "M8", str(i), "M8"], data
                    ),
                }
                for i in range(1, 801)
            },
            orient="index",
        )
        .sort_index()
        .dropna()
    )
    evaluations_data = (
        pd.DataFrame.from_dict(
            {
                i: {t: access(["evaluations_index", t, str(i)], data) for t in tasks}
                for i in range(1, 801)
            },
            orient="index",
        )
        .sort_index()
        .dropna()
    )

    plt.subplots(nrows=2, ncols=1, sharex="col")
    plt.subplot(2, 1, 1)
    labels = ["m2, m3", "m4 avg", "m4.stdDev", "m8.min"]
    columns = ["M2", "M4 avg", "M4 stdDev", "M8 min"]
    style = ["solid", "dotted", "dashdot", "dashed"]
    for col, lab, sty in zip(columns, labels, style):
        plt.plot(
            measurements_data.index,
            measurements_data[col],
            label=lab,
            linestyle=sty,
            c="k",
        )
    # plt.subplots_adjust(left=0, right=1, top=1, bottom=0, wspace=0, hspace=0)
    vertical_lines()
    plt.ylabel("Metric", loc="top")
    plt.xlim((min(measurements_data.index), max(measurements_data.index)))
    plt.legend(
        bbox_to_anchor=(0, 1, 1, 0),
        loc="lower left",
        mode="expand",
        ncol=3,
        frameon=False,
    )
    plt.semilogy()

    ax = plt.subplot(2, 1, 2)
    ax.imshow(
        evaluations_data.transpose().astype(float).values,
        interpolation="nearest",
        aspect="auto",
        cmap=ListedColormap(["k", "w"]),
    )
    vertical_lines()
    for i, t in enumerate(tasks):
        ax.axhline(y=0.5 + i, c="k", linewidth=0.5, linestyle="dashed")
    plt.yticks(range(len(tasks)), list(map(lambda t: t.lower(), tasks)))
    plt.xlabel("Time (s)", loc="right")
    plt.ylabel("Task", loc="top")
    plt.tight_layout()
    ax.set_xlim(S_START, S_END)
    if ATTACK_START is not None:
        plt.savefig("../plots/attack.pdf", format="pdf")
        plt.savefig("../plots/attack.png", format="png")
    else:
        plt.savefig("../plots/certification.pdf", format="pdf")
        plt.savefig("../plots/certification.png", format="png")
    plt.show()
