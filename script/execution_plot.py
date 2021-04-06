import json
from os.path import dirname, abspath

import matplotlib.pyplot as plt

LOG_FILE = abspath(f"{dirname(__file__)}/../logs/execution_mut_logs.json")
LOG_FILE = abspath("/tmp/ca/logs.json")

if __name__ == '__main__':
    with open(LOG_FILE) as f:
        data = {k: v for k, v in json.load(f).items() if "index" in k}

    max_index = min(max(map(int, data["duration_index"].keys())), 1000)
    plt.plot(
        list(range(max_index + 1)),
        list(map(lambda k: data["duration_index"][str(k)] / 1e9, range(max_index + 1))),
        c="k", linewidth=0.5)
    plt.xlabel("Iteration", loc="right")
    plt.ylabel("Execution time (s)", loc="top")
    plt.tight_layout()
    plt.savefig("../plots/execution.pdf", format="pdf")
    plt.savefig("../plots/execution.png", format="png")
    plt.show()
