import json
from typing import Dict, List, Any
from os.path import dirname, abspath
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

INVALID_SIGNATURE, NO_DEFAULT_IDENTITY, SAFE_IDENTITY_RESTORED, LOG_FILE = (
    260,
    268,
    277,
    abspath(f"{dirname(__file__)}/../logs/misconfiguration_logs.json"),
)
METRICS = [f"M{i + 1}" for i in range(12)]
TASKS = ["C13", "C14"] + ["R6", "R7"] + [f"P{i+1}" for i in range(3)]
S_START = 200
S_END = 520


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


def vertical_lines(ax):
    ax.axvline(
        x=INVALID_SIGNATURE,
        c="k",
        linestyle="solid",
        linewidth=1,
        label=f"Invalid signature",
    )
    ax.axvline(
        x=NO_DEFAULT_IDENTITY,
        c="k",
        linestyle="dashed",
        linewidth=1,
        label=f"No default identity",
    )
    ax.axvline(
        x=SAFE_IDENTITY_RESTORED,
        c="k",
        linestyle="dotted",
        linewidth=1,
        label=f"Safe identity restored",
    )


if __name__ == "__main__":
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
                for i in range(1, S_END)
            },
            orient="index",
        )
        .sort_index()
        .dropna()
    )
    evaluations_data = (
        pd.DataFrame.from_dict(
            {
                i: {t: access(["evaluations_index", t, str(i)], data) for t in TASKS}
                for i in range(1, S_END)
            },
            orient="index",
        )
        .sort_index()
        .dropna()
    )

    plt.subplots(nrows=2, ncols=1, sharex="col")
    ax = plt.subplot(2, 1, 1)
    labels = ["m2, m3", "m4 avg", "m4.stdDev", "m8.min"]
    columns = ["M2", "M4 avg", "M4 stdDev", "M8 min"]
    style = ["solid", "dotted", "dashdot", "dashed"]
    for col, lab, sty in zip(columns, labels, style):
        ax.plot(
            measurements_data.index,
            measurements_data[col],
            label=lab,
            linestyle=sty,
            c="k",
        )
    # plt.subplots_adjust(left=0, right=1, top=1, bottom=0, wspace=0, hspace=0)
    vertical_lines(ax)
    plt.ylabel("Metric", loc="top")
    plt.xlim((min(measurements_data.index), max(measurements_data.index)))
    ax.legend(
        bbox_to_anchor=(0, 1, 1, 0),
        loc="lower left",
        mode="expand",
        ncol=3,
        frameon=False,
    )
    ax.semilogy()

    ax = plt.subplot(2, 1, 2)
    ax.imshow(
        evaluations_data.astype(float).transpose(),
        interpolation="nearest",
        aspect="auto",
        cmap=ListedColormap(["k", "w"]),
    )
    vertical_lines(ax)
    for i, t in enumerate(TASKS):
        plt.axhline(y=0.5 + i, c="k", linewidth=0.5, linestyle="dashed")
    plt.yticks(range(len(TASKS)), list(map(lambda t: t.lower(), TASKS)))
    plt.xlabel("Time (s)", loc="right")
    plt.ylabel("Task", loc="top")
    plt.tight_layout()
    plt.xlim(S_START, S_END)
    plt.savefig("../plots/misconfiguration.pdf", format="pdf")
    plt.savefig("../plots/misconfiguration.png", format="png")
    plt.show()
