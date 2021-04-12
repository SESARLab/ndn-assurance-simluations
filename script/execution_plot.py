import json
from collections import Iterable
from os.path import dirname, abspath

import matplotlib.pyplot as plt

LOG_FILES = [abspath(f"{dirname(__file__)}/../logs/execution_mut_logs.json")]
LOG_FILES = [abspath(f"{dirname(__file__)}/../logs/execution_logs_{i}.json") for i in [1, 2, 3, 4, 5]]


def mean(it) -> float:
    try:
        return float(sum(it)) / len(it)
    except ZeroDivisionError:
        return 0.0


if __name__ == '__main__':
    logs = dict()
    for log_file in LOG_FILES:
        with open(log_file) as f:
            logs[log_file] = {k: v for k, v in json.load(f).items() if "index" in k}

    indexes = {int(k) for log_file in LOG_FILES for k in logs[log_file]["duration_index"].keys() if int(k) <= 1000}
    values = {
        i: mean(list(
            filter(lambda v: v is not None, [logs[log_file]["duration_index"].get(str(i)) for log_file in LOG_FILES])))
        for i in indexes}

    plt.plot(
        list(sorted(values.keys())),
        list(map(lambda i: values[i] / 1e9, sorted(values.keys()))),
        c="k", linewidth=0.5)
    plt.xlabel("Iteration", loc="right")
    plt.ylabel("Execution time (s)", loc="top")
    plt.tight_layout()
    plt.savefig("../plots/execution.pdf", format="pdf")
    plt.savefig("../plots/execution.png", format="png")
    plt.show()
