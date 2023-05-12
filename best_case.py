import numpy as np
from python_tsp.exact import solve_tsp_dynamic_programming
from python_tsp.distances import great_circle_distance_matrix
from cities import Cities

cities = Cities()
city_positions = cities.get_cities()
print(city_positions)

# # distance_matrix  = great_circle_distance_matrix(city_positions)
# # permutation, distance = solve_tsp_dynamic_programming(distance_matrix)
# print(permutation)
# print(distance)
