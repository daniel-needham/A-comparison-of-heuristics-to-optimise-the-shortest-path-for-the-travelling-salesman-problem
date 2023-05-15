from ant_colony_optimisation import ACO
from hillclimber import HillClimber
from genetic_algorithm import MicrobialGA
from utils import *
import numpy as np

# hyperparameters
pop_size = 20
iterations = 1000
total_runs = 5

hc_best_fit = 2000
hc_best_geno = None
hc_worst_fit = 0
hc_worst_geno = None
hc_runs = np.zeros((total_runs, iterations))
for i in range(total_runs):
    hill_climber = HillClimber(pop_size)
    geno, distance, fitness_by_iter = hill_climber.iterate(iterations)
    print(distance)
    if distance < hc_best_fit:
        hc_best_fit = distance
        hc_best_geno = geno
    if distance > hc_worst_fit:
        hc_worst_fit = distance
        hc_worst_geno = geno

    hc_runs[i] = fitness_by_iter

    if i == total_runs - 1:
        hill_climber.cities.plot_cities(hc_best_geno, hc_best_fit)
        hill_climber.cities.plot_cities(hc_worst_geno, hc_worst_fit)


hc_mean_by_iter = np.mean(hc_runs, axis=0)
hc_std_by_iter = np.std(hc_runs, axis=0)

plot_mean_fitness_by_iter(hc_mean_by_iter, iterations, hc_std_by_iter)



ga_best_fit = 2000
ga_best_geno = None
ga_worst_fit = 0
ga_worst_geno = None
ga_runs = np.zeros((total_runs, iterations))
for i in range(total_runs):
    microbial_ga = MicrobialGA(pop_size, local_neighbourhood=2, pmx_slice_length=25, mutation_rate=1, selection_type='tournament')
    geno, distance, fitness_by_iter = microbial_ga.iterate(iterations)
    print(distance)
    if distance < ga_best_fit:
        ga_best_fit = distance
        ga_best_geno = geno
    if distance > ga_worst_fit:
        ga_worst_fit = distance
        ga_worst_geno = geno

    ga_runs[i] = fitness_by_iter

    if i == total_runs - 1:
        microbial_ga.cities.plot_cities(ga_best_geno, ga_best_fit)
        microbial_ga.cities.plot_cities(ga_worst_geno, ga_worst_fit)

ga_mean_by_iter = np.mean(ga_runs, axis=0)
ga_std_by_iter = np.std(ga_runs, axis=0)

plot_mean_fitness_by_iter(ga_mean_by_iter, iterations, ga_std_by_iter)


aco_best_fit = 2000
aco_best_geno = None
aco_worst_fit = 0
aco_worst_geno = None

aco_runs = np.zeros((total_runs, iterations))
for i in range(total_runs):
    ant_colony = ACO(pop_size, 1, 5, 0.5, 100)
    geno, distance, fitness_by_iter = ant_colony.iterate(iterations)
    print(distance)

    if distance < aco_best_fit:
        aco_best_fit = distance
        aco_best_geno = geno
    if distance > aco_worst_fit:
        aco_worst_fit = distance
        aco_worst_geno = geno

    aco_runs[i] = fitness_by_iter

    if i == total_runs - 1:
        ant_colony.cities.plot_cities(aco_best_geno, aco_best_fit)
        ant_colony.cities.plot_cities(aco_worst_geno, aco_worst_fit)


aco_mean_by_iter = np.mean(aco_runs, axis=0)
aco_std_by_iter = np.std(aco_runs, axis=0)
plot_mean_fitness_by_iter(aco_mean_by_iter, iterations, aco_std_by_iter)

print(f'Hill climber final mean fitness: {hc_mean_by_iter[-1]} with std: {hc_std_by_iter[-1]}')
print(f'Genetic algorithm final mean fitness: {ga_mean_by_iter[-1]} with std: {ga_std_by_iter[-1]}')
print(f'Ant colony optimisation final mean fitness: {aco_mean_by_iter[-1]} with std: {aco_std_by_iter[-1]}')

fitnesses = np.array([hc_mean_by_iter, ga_mean_by_iter, aco_mean_by_iter])
plot_all_mean_fitness_by_iter(fitnesses, iterations)