from cities import Cities
import numpy as np
import random


class MicrobialGA:
    def __init__(self, population_size=100, local_neighbourhood=2, mutation_rate=0.5, pmx_slice_length=3,
                 selection_type='tournament'):
        """Initializes the hill climber"""
        self.population = None
        self.pop_fitnesses = None
        self.cities = Cities()
        self.city_list = self.cities.get_city_list()
        self.set_up_population(population_size)
        self.local_neighbourhood = local_neighbourhood
        self.mutation_rate = mutation_rate
        self.pmx_slice_length = pmx_slice_length
        if selection_type == 'tournament':
            self.selection_type = self.tournament_selection
        elif selection_type == 'roulette':
            self.selection_type = self.roulette_selection
        elif selection_type == 'rank':
            self.selection_type = self.rank_selection
        else:
            raise ValueError('Invalid selection type')

    def set_up_population(self, population_size):
        """Sets up a population of a given size and their fitnesses"""
        self.population = np.array([np.random.permutation(self.city_list) for _ in range(population_size)])
        self.pop_fitnesses = np.array([self.cities.total_distance(genotype) for genotype in self.population])

    def iterate(self, iterations):
        """Performs tournament selection, crossover and mutation for a given number of iterations"""
        best_fitness_epoch = []
        for i in range(iterations):
            if i % 100 == 0: print(f'Iteration {i}/{iterations}')
            for _ in range(len(self.population)):
                comb1, comb2 = self.selection_type(self.population)
                w, l = self.combat(comb1, comb2)
                l_geno = self.pmx_crossover(w[0], l[0], slice_length=self.pmx_slice_length)
                _, l_index = l
                l_geno = self.mutate_genotype(l_geno)
                self.population[l_index] = l_geno
                self.pop_fitnesses[l_index] = self.cities.total_distance(l_geno)
            best_fitness_epoch.append(self.get_best_fitness())
        self.population = self.population[
            np.argsort([self.cities.total_distance(genotype) for genotype in self.population])]
        return self.population[0], self.cities.total_distance(self.population[0]), best_fitness_epoch

    def tournament_selection(self, population):
        """Performs tournament selection on the population"""
        rand_index = np.random.randint(0, len(population))
        lower = rand_index - self.local_neighbourhood
        upper = rand_index + self.local_neighbourhood
        rand_index2 = rand_index
        while rand_index2 == rand_index:  # Make sure we don't pick the same individual twice
            rand_index2 = np.random.randint(lower, upper)
        rand_index2 = rand_index2 % len(population)
        return (population[rand_index], rand_index), (population[rand_index2], rand_index2)

# todo fix roulette and rank selection
    # def roulette_selection(self, population):
    #     """Performs roulette selection on the population"""
    #     fitnesses = self.pop_fitnesses / np.sum(self.pop_fitnesses)
    #     roul_i = random.choices(range(len(population)), weights=fitnesses, k=1)
    #     roul_i2 = roul_i # Make sure we don't pick the same individual twice
    #     fitnesses = fitnesses[(roul_i - self.local_neighbourhood) : (roul_i2 + self.local_neighbourhood)]
    #     print(fitnesses)
    #     while roul_i2 == roul_i:
    #         random.choices(range(roul_i - self.local_neighbourhood, roul_i2 + self.local_neighbourhood), weights=fitnesses, k=1)
    #
    # def rank_selection(self, population):
    #     """Performs rank selection on the population"""
    #     fitnesses = np.argsort(self.pop_fitnesses)
    #     rank_i, rank_i2 = random.choice(range(len(population)), 2, p=fitnesses)
    #     return (population[rank_i], rank_i), (population[rank_i2], rank_i2)


    def combat(self, comb1, comb2):
        """Performs combat between two individuals"""
        if self.cities.total_distance(comb1[0]) < self.cities.total_distance(comb2[0]):
            return comb1, comb2
        else:
            return comb2, comb1

    def mutate_genotype(self, geno):
        new_geno = geno.copy()
        i, j = np.random.choice(self.city_list, 2, replace=False)
        new_geno[i], new_geno[j] = new_geno[j], new_geno[i]
        return new_geno

    def get_best_fitness(self):
        """Returns the best fitness in the population"""
        return np.min(self.pop_fitnesses)

    def pmx_crossover(self, winner, loser, slice_length=3):
        """Performs PMX crossover between two individuals"""
        # Choose two random crossover points
        i = np.random.randint(0, len(winner))
        j = np.random.choice([i + slice_length, i - slice_length])
        j = j % (len(winner) + 1)  # wrap around if j is out of bounds
        if j < i:  # swap if j less than i
            i, j = j, i

        # copy winner slice to the child
        child = np.full(len(winner), None)
        child[i:j] = winner[i:j]
        # map the slice of loser to the child using indices from winner
        for ind, gene in enumerate(loser[i:j]):
            ind += i
            if gene not in child:
                while child[ind] is not None:
                    ind = np.nonzero(loser == winner[ind])[0][0]
                child[ind] = gene

        # copy over the rest of the genes from loser
        for ind, gene in enumerate(child):
            if gene is None:
                child[ind] = loser[ind]

        return child

# ga = MicrobialGA()
#
# w = np.array([1, 2, 3, 4, 5])
# l = np.array([5, 4, 3, 2, 1])
#
# child = ga.pmx_crossover(w, l)
# print(child)
