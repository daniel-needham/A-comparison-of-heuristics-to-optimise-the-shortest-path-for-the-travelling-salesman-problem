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

    def get_cities(self):
        """Returns the list of cities"""
        return self.cities

    def get_city_list(self):
        """Returns a list of city indices"""
        return list(range(len(self.cities)))

    def distance(self, city1, city2):
        """Returns the distance between two cities"""
        return np.linalg.norm(self.cities[city1] - self.cities[city2])

    def total_distance(self, city_list):
        """Returns the total distance between a list of cities"""
        dist = sum([self.distance(city_list[i], city_list[i + 1]) for i in range(len(city_list) - 1)])
        dist += self.distance(city_list[0], city_list[-1]) # home journey
        return dist
    def plot_cities(self, city_list, distance=None):
        """Plots the cities in the order they appear in city_list"""
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



