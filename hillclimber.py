from cities import Cities
import numpy as np


class HillClimber:
    def __init__(self, population_size=100):
        """Initializes the hill climber"""
        self.population = None
        self.cities = Cities()
        self.city_list = self.cities.get_city_list()
        self.set_up_population(population_size)

    def set_up_population(self, population_size):
        """Sets up a population of a given size"""
        self.population = np.array([np.random.permutation(self.city_list) for _ in range(population_size)])

    def iterate(self, iterations):
        """Climbs the hill for a given number of iterations"""
        best_fitness_epoch = []
        for i in range(iterations):
            if i % 100 == 0: print(f'Iteration {i}/{iterations}')
            self.population = self.mutate(self.population)
            best_fitness_epoch.append(self.get_best_fitness())
        self.population = self.population[np.argsort([self.cities.total_distance(genotype) for genotype in self.population])]
        return self.population[0], self.cities.total_distance(self.population[0]), best_fitness_epoch

    def mutate(self, population):
        """Mutates the population"""
        mutated_population = []
        for genotype in population:
            mutated_population.append(self.mutate_genotype(genotype))
        return np.array(mutated_population)

    def mutate_genotype(self, geno):
        """Mutates a given genotype"""
        old_fit = self.cities.total_distance(geno)
        new_geno = geno.copy()
        i, j = np.random.choice(self.city_list, 2, replace=False)
        new_geno[i], new_geno[j] = new_geno[j], new_geno[i]

        if self.cities.total_distance(new_geno) < old_fit:
            return new_geno
        else:
            return geno

    def get_best_fitness(self):
        """Returns the best fitness in the population"""
        best_fitness = np.inf
        for geno in self.population:
            fitness = self.cities.total_distance(geno)
            if fitness < best_fitness:
                best_fitness = fitness
        return best_fitness

