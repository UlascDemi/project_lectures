import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

hillclimb1 = pd.read_csv("output/random.csv", names=["index", "vals"])
hillclimb2 = pd.read_csv("output/random.csv", names=["index", "vals"])
anneal1 = pd.read_csv("output/random.csv", names=["index", "vals"])
anneal2 = pd.read_csv("output/random.csv", names=["index", "vals"])
random = pd.read_csv("output/random.csv", names=["index", "vals"])

plots = [
    # pd.read_csv("output/random.csv", names=["index", "vals"]),
    pd.read_csv("output/random_1000.csv", names=["index", "vals"]),
    pd.read_csv("output/greedy_1000.csv", names=["index", "vals"]),
    pd.read_csv("output/hillclimb_700_2.csv", names=["index", "vals"]),
    pd.read_csv("output/sim_anneal_500_2.csv", names=["index", "vals"]),
    # pd.read_csv("output/random.csv", names=["index", "vals"]),
]


for data in plots:
    mu, sigma = np.mean(data.vals), np.std(data.vals)
    s = np.random.normal(mu, sigma, 1000)

    count, bins, ignored = plt.hist(s, 30, density=True)
    # plt.plot(
    #     bins,
    #     1
    #     / (sigma * np.sqrt(2 * np.pi))
    #     * np.exp(-((bins - mu) ** 2) / (2 * sigma**2)),
    #     linewidth=2,
    #     color="r",
    # )

plt.legend(["random", "Greedy", "hillclimb", "simulated annealing"])
plt.xlabel("Malus Points")
plt.ylabel("Probability")
plt.grid(which="both")
plt.savefig("aaaa.png")
