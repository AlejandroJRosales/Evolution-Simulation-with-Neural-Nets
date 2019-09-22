"""
CONVERT TO BLENDER OBJECTS - Change to "CATD" type dna or numbers or number representing "CATD"
"""

import NextGen as ng
from NextGen import Stats, MassEffect, Utils

pop_n = [200, 200, 200]  # Number of: Charlens, Gritiss, Drackonians

stats = Stats()
mass_effect = MassEffect()
utils = Utils()
print_every = 2
print_plots_every = 50
num_data_points = 5
prob_illness = .0001
prob_war = .0001
prob_species_war = .001
prob_civil_war = 0.001
prob_infected_individuals = 0.8
to_fight = 0.8
to_fight_species_war = 0.8
to_fight_civil_war = 0.8
pause = False
pause_for_plot = True
save_plot = True

weights = utils.create_weights()
stats.weights_summary(weights, pause)

generation = 0
population = ng.generate_population(pop_n)
while True:
    # for i in range(10000):
    utils.check_pulse(population)
    stats.counting(population, generation, print_every=print_every)
    stats.creatures_summary(population, weights, generation, print_every=print_every)
    stats.show_nn_bar_graph(utils.get_median_nn_stats(population), generation, save_plot=save_plot, print_plots_every=print_plots_every, pause_for_plot=pause_for_plot)

    population = ng.evolve(population, weights)

    population = mass_effect.infect(population, prob_illness, prob_infected_individuals, pause=pause)
    population = mass_effect.war(population, prob_war, weights, to_fight, pause=pause)
    population = mass_effect.species_war(population, prob_species_war, weights, to_fight_species_war, pause=pause)
    population = mass_effect.civil_war(population, prob_civil_war, weights, to_fight_civil_war, pause=pause)

    generation += 1
