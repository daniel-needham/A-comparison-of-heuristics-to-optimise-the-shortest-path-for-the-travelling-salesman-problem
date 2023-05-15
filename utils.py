import numpy as np
import matplotlib.pyplot as plt


def invNormal(low, high, mu=0, sd=1, *, size=1, block_size=1024):
    """Draws samples from a truncated normal distribution"""
    """:param low: lower bound of the interval"""
    """:param high: upper bound of the interval"""
    """:param mu: mean of the normal distribution"""
    """:param sd: standard deviation of the normal distribution"""
    """:param size: number of samples to draw"""
    """:param block_size: number of samples to draw at a time"""
    """:return: samples from the truncated normal distribution"""
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
    """:param fitnesses: list of fitnesses by iteration"""
    """:param iter: number of iterations"""
    """:return: None"""
    plt.figure(figsize=(10, 10))
    plt.plot(range(1, iter + 1), fitnesses)
    plt.title("Best fitness in the population by iteration")
    plt.xlabel('Iteration')
    plt.ylabel('Fitness (Total Distance for Journey)')
    plt.show()


def plot_mean_fitness_by_iter(fitnesses, iter, std):
    """Plots the mean fitnesses by iteration"""
    """:param fitnesses: list of fitnesses by iteration"""
    """:param iter: number of iterations"""
    """:param std: list of standard deviation of fitness"""
    """:return: None"""
    plt.figure(figsize=(10, 10))
    plt.plot(range(1, iter + 1), fitnesses)
    plt.fill_between(range(1, iter + 1), fitnesses - std, fitnesses + std, alpha=0.2)
    plt.title("Fitness in the population by iteration averaged over 5 runs")
    plt.xlabel('Iteration')
    plt.ylabel('Fitness (Total Distance for Journey)')
    plt.legend(['Mean fitness', 'Standard deviation'])
    plt.show()

def plot_all_mean_fitness_by_iter(fitnesses, iterations):
    """Plots the mean fitnesses of multiple SSO by iteration"""
    """:param fitnesses: np array of fitnesses of multiple SSOs"""
    """:param iterations: number of iterations"""
    """:return: None"""
    plt.figure(figsize=(10, 10))
    for i in range(fitnesses.shape[0]):
        plt.plot(range(1, iterations + 1), fitnesses[i])
    plt.title("Fitness in the population by iteration averaged over 5 runs")
    plt.xlabel('Iteration')
    plt.ylabel('Fitness (Total Distance for Journey)')
    plt.legend(['Hill Climber', 'Genetic Algorithm', 'Ant Colony Optimisation'])
    plt.show()