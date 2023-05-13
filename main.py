from ant_colony_optimisation import ACO
from hillclimber import HillClimber
from genetic_algorithm import MicrobialGA
from utils import *
import numpy as np

# hyperparameters
pop_size = 10
iterations = 1000

hill_climber = HillClimber(pop_size)
geno, distance, fitness_by_iter = hill_climber.iterate(iterations)
print(geno)
print(distance)
hill_climber.cities.plot_cities(geno, distance)
plot_fitness_by_iter(fitness_by_iter, iterations)


microbial_ga = MicrobialGA(pop_size, pmx_slice_length=5, selection_type='tournament')
geno, distance, fitness_by_iter = microbial_ga.iterate(iterations)
print(geno)
print(distance)
microbial_ga.cities.plot_cities(geno, distance)
plot_fitness_by_iter(fitness_by_iter, iterations)

ant_colony = ACO(5, 0.9, 0.9, 0.5, 0.1)
geno, distance, fitness_by_iter = ant_colony.iterate(iterations)
print(geno)
print(distance)
ant_colony.cities.plot_cities(geno, distance)
plot_fitness_by_iter(fitness_by_iter, iterations)