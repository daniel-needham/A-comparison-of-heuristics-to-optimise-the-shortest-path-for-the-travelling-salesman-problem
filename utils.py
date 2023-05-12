import numpy as np
import matplotlib.pyplot as plt


def invNormal(low, high, mu=0, sd=1, *, size=1, block_size=1024):
    remain = size
    result = []

    mul = -0.5 * sd ** -2

    while remain:
        # draw next block of uniform variates within interval
        x = np.random.uniform(low, high, size=min((remain + 5) * 2, block_size))

        # reject proportional to normal density
        x = x[np.exp(mul * (x - mu) ** 2) < np.random.rand(*x.shape)]

        # make sure we don't add too much
        if remain < len(x):
            x = x[:remain]

        result.append(x)
        remain -= len(x)

    return np.concatenate(result)


def plot_fitness_by_iter(fitnesses, iter):
    """Plots the fitnesses by iteration"""
    plt.figure(figsize=(10, 10))
    plt.plot(range(1, iter + 1), fitnesses)
    plt.title("Best fitness in the population by iteration")
    plt.xlabel('Iteration')
    plt.ylabel('Fitness(Total Distance for Journey)')
    plt.show()
