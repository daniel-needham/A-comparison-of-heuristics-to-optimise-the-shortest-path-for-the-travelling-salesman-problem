import numpy as np
import random
from cities import Cities


class ACO:

    def __init__(self, ants, alpha, beta, rho, q):
        self.ants = ants
        self.alpha = alpha
        self.beta = beta
        self.rho = rho
        self.q = q
        self.cities = Cities()
        self.number_of_cities = len(self.cities.get_city_list())
        self.distance_matrix = self.cities.distance_matrix
        self.pheromone_matrix = np.ones((self.number_of_cities, self.number_of_cities)) * 0.1
        self.best_path = None
        self.best_distance = np.inf
        self.best_distance_by_iter = []

    def next_city(self, current_city, unvisited_cities):
        """Returns the next city for an ant based on pheromone and heuristic information"""
        """:param current_city: The current city of the ant"""
        """:param unvisited_cities: list of cities that the ant has not visited yet"""
        """:return: the next city for the ant to visit"""
        # Calculate the probabilities for the ant to go to the next city
        denom = sum((self.pheromone_matrix[current_city][j] ** self.alpha) * (
                (1 / self.distance_matrix[current_city][j]) ** self.beta) for j in unvisited_cities)
        if denom == 0.0:
            print("denom is zero")
            next_city = np.random.choice(unvisited_cities, 1)[0]
        else:
            probabilities = [(self.pheromone_matrix[current_city][j] ** self.alpha) * (
                    (1 / self.distance_matrix[current_city][j]) ** self.beta) / denom for j in unvisited_cities]
            # Randomly select the next city based on the probabilities
            next_city = np.random.choice(unvisited_cities, 1, p=probabilities)[0]

        return next_city

    def ant_tour(self):
        """Sends an ant on a tour"""
        """:return: the tour of the ant"""
        start_city = random.randint(0, self.number_of_cities - 1)
        unvisited_cities = [i for i in range(self.number_of_cities) if i != start_city]
        current_city = start_city
        ant_tour = [start_city]

        while unvisited_cities:
            next_city = self.next_city(current_city, unvisited_cities)
            ant_tour.append(next_city)
            unvisited_cities.remove(next_city)
            current_city = next_city

        return ant_tour

    def tour_length(self, tour):
        """Calculates the length of a tour"""
        """:param tour: the tour to calculate the length of"""
        """:return: the length of the tour"""
        return self.cities.total_distance(tour)

    def update_pheromones(self, tours):
        """Updates the pheromone matrix based on the tours"""
        """:param tours: the tours to update the pheromone matrix with"""
        """:return: None"""
        self.pheromone_matrix *= (1 - self.rho)
        for tour in tours:
            distance = self.tour_length(tour)
            for i in range(len(tour) - 1):
                self.pheromone_matrix[tour[i]][tour[i + 1]] += self.q / distance
            self.pheromone_matrix[tour[-1]][tour[0]] += self.q / distance

    def iterate(self, iterations):
        """Runs the ant colony optimisation algorithm for a given number of iterations"""
        """:param iterations: the number of iterations to run the algorithm for"""
        """:return: the best path, the distance of the best path, and the best distance by iteration"""
        for iteration in range(iterations):
            tours = [self.ant_tour() for _ in range(self.ants)]
            self.update_pheromones(tours)

            for tour in tours:
                distance = self.tour_length(tour)
                if distance < self.best_distance:
                    self.best_distance = distance
                    self.best_path = tour

            self.best_distance_by_iter.append(self.best_distance)
            if iteration % 100 == 0:
                print("Iteration: {}/{}, Best Distance: {}".format(iteration, iterations, self.best_distance))

        return self.best_path, self.best_distance, self.best_distance_by_iter
