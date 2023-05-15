import numpy as np
import random
import matplotlib.pyplot as plt
from utils import *


# randomly generate 100 cities and save them to a file for the first time
# x = invNormal(0, 200, 100,size=50)
# y = invNormal(0, 200, 100,size=50)
#
# cities = np.array([x,y]).T
# np.save('cities.npy', cities)


class Cities:
    """Class to create a list of cities with their coordinates and provide related methods"""

    def __init__(self):
        """Initializes the list of cities"""
        self.cities = np.load('cities.npy')
        self.distance_matrix = self.create_distance_matrix()

    def create_distance_matrix(self):
        """Creates a distance matrix for the cities"""
        """:return: a distance matrix for the cities"""
        distance_matrix = np.zeros((len(self.cities), len(self.cities)))
        for i in range(len(self.cities)):
            for j in range(len(self.cities)):
                distance_matrix[i, j] = self.distance(i, j)
        return distance_matrix

    def get_cities(self):
        """Returns the list of cities"""
        """:return: the list of cities"""
        return self.cities

    def get_city_list(self):
        """Returns a list of city indices"""
        return list(range(len(self.cities)))

    def distance(self, city1, city2):
        """Returns the distance between two cities"""
        """:param city1: the index of the first city"""
        """:param city2: the index of the second city"""
        return np.linalg.norm(self.cities[city1] - self.cities[city2])

    def total_distance(self, city_list):
        """Returns the total distance between a list of cities"""
        """:param city_list: a list of city indices"""
        """Returns the total distance between a list of cities"""
        dist = sum([self.distance(city_list[i], city_list[i + 1]) for i in range(len(city_list) - 1)])
        dist += self.distance(city_list[0], city_list[-1])  # home journey
        return dist

    def plot_cities(self, city_list, distance=None):
        """Plots the cities in the order they appear in city_list"""
        """:param city_list: a list of city indices"""
        """:param distance: the total distance of the journey"""
        """:return: None"""
        plt.figure(figsize=(10, 10))
        plt.plot(self.cities[city_list][:, 0], self.cities[city_list][:, 1], '--', color='grey', marker='o')
        start_end = [city_list[0]] + [city_list[-1]]
        plt.plot(self.cities[city_list[0]][0], self.cities[city_list[0]][1], 'ro')
        plt.plot(self.cities[start_end][:, 0], self.cities[start_end][:, 1], '--', color='grey', marker='o')
        plt.plot(self.cities[city_list[0]][0], self.cities[city_list[0]][1], 'ro')
        title = "The Salesman's journey with a total distance of: " + str(
            round(distance, 2)) if distance else "The Salesman's journey"
        plt.title(title)
        plt.legend(['Journey', 'Starting point'])
        plt.xlabel('X dimension')
        plt.ylabel('Y dimension')
        plt.show()

    def plot_map(self):
        plt.figure(figsize=(10, 10))
        plt.scatter(self.cities[:, 0], self.cities[:, 1], color='red', marker='.', s=100)
        plt.title('Map of the cities')
        plt.xlabel('X dimension')
        plt.ylabel('Y dimension')
        plt.show()
