import random
import NextGen as ng
from NextGen import Stats, MassExtinction

pop_n = [33, 33, 33]  # Number of: Humans, Gritiss, Drackonians
weights = [random.random() for i in range(5)]

mass_extinction = MassExtinction()
stats = Stats()

print_every = 3
prob_illness = .001
prob_war = .0001
prob_species_war = 1
to_fight = .8
to_fight_species_war = .8
pause = True
stats.weights_summary(weights)

generation = 0
population = ng.generate_population(pop_n)
while True:
    if generation % print_every == 0:
        print()
    stats.counting(population, generation, print_every=print_every)
    stats.creatures_summary(population, weights, generation, print_every=print_every)

    population = ng.evolve(population, weights)

    population = mass_extinction.infect(population, pause) if prob_illness >= random.random() else population
    population = mass_extinction.war(population, weights, to_fight, pause) if prob_war >= random.random() else population
    population = mass_extinction.species_war(population, weights, to_fight_species_war, pause) if prob_species_war >= random.random() else population

    generation += 1
