#!/usr/bin/env python
import json
from os.path import dirname, abspath
from collections import defaultdict

import matplotlib.pyplot as plt
import pandas as pd
from sklearn import linear_model

LOG_FILES = {
    "P1": [abspath(f"{dirname(__file__)}/../logs/p1_logs_{i}.json") for i in [1, 2, 3]],
    "P1∧P2": [
        abspath(f"{dirname(__file__)}/../logs/p1+p2_logs_{i}.json") for i in [1, 2, 3]
    ],
    "P2∧P3": [
        abspath(f"{dirname(__file__)}/../logs/p2+p3_logs_{i}.json") for i in [1, 2, 3]
    ],
    "P1∧P2∧P3": [
        abspath(f"{dirname(__file__)}/../logs/p1+p2+p3_logs_{i}.json")
        for i in [1, 2, 3]
    ],
}

if __name__ == "__main__":
    logs_data = defaultdict(lambda: defaultdict(lambda: 0))
    for sim_name, log_files in LOG_FILES.items():
        for log_file in log_files:
            with open(log_file) as f:
                for timestamp, duration in json.load(f)["duration_index"].items():
                    logs_data[int(timestamp)][sim_name] += float(duration)

    plot_data = pd.DataFrame.from_dict(logs_data).transpose().sort_index()
    plot_data /= len(log_files)
    plot_data /= 10e9
    plot_data = plot_data[:501]

    for c in plot_data.columns:
        l_reg = linear_model.LinearRegression()
        l_reg.fit(
            plot_data.index.values.reshape(-1, 1), plot_data[[c]].values.reshape(-1, 1)
        )
        plot_data[f"_reg_{c}"] = l_reg.predict(plot_data.index.values.reshape(-1, 1))

    styles = [
        "solid",
        "dashed",
        "dashdot",
        "dotted",
        "solid",
        "solid",
        "solid",
        "solid",
    ]
    widths = [0.75] * 4 + [0.5] * 4
    colors = ["k"] * len(plot_data.columns)
    for column, style, linewidth, color in zip(
        plot_data.columns, styles, widths, colors
    ):
        plot_data[column].rolling(7).mean().plot(
            linestyle=style, linewidth=linewidth, c=color, legend=True
        )
    plt.xlabel("Time (s)", loc="right")
    plt.ylabel("Execution time (s)", loc="top")
    plt.legend(frameon=False)
    plt.tight_layout()
    plt.savefig("../plots/rule_evaluation.pdf", format="pdf")
    plt.savefig("../plots/rule_evaluation.png", format="png")
    plt.show()
