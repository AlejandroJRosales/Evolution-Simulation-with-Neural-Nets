import random
import NextGen as ng
from NextGen import Stats

pop_n = [3333, 3333, 3333]  # Number of: Humans, Drackonians, Gritiss
weights = [random.random() for i in range(5)]
stats = Stats()
stats.weights_summary(weights)
population = ng.generate_population(pop_n)
for generation in range(4000):
    if generation % 10 == 0:
        print()
    stats.counting(population, generation, print_at=10)
    stats.creatures_summary(population, weights, generation, print_at=10)
    population = ng.evolve(population, weights)
