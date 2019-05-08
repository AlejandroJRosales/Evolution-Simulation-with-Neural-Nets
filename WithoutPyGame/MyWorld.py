import random
import NextGen as ng
from NextGen import Stats, MassExtinction

pop_n = [33333, 33333, 33333]  # Number of: Humans, Gritiss, Drackonians
weights = [random.random() for i in range(5)]
stats = Stats()
stats.weights_summary(weights)
print_every = 3
population = ng.generate_population(pop_n)
mass_extinction = MassExtinction()
generation = 0
while True:
    if generation % print_every == 0:
        print()
    stats.counting(population, generation, print_every=print_every)
    stats.creatures_summary(population, weights, generation, print_every=print_every)
    population = ng.evolve(population, weights)
    
    population = mass_extinction.infect(population) if random.random() > .99 else population
    generation += 1
