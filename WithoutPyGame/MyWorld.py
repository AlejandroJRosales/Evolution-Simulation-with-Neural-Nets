"""
CONVERT TO BLENDER OBJECTS - Change to "CATD" type dna or numbers or number representing "CATD"
"""

import sys
import numpy as np
import NextGen as ng
from NextGen import Stats, MassEffect, Utils

pop_n = [333333333, 333333333, 333333333]  # Number of: Charlens, Gritiss, Drackonians

load_file = False
auto_save = True
pause_for_auto_save = False
save_every = 7
file_in = open(input("File name to load previous simulation from: ") + ".txt", "r") if load_file else None
if load_file:
    file_in = file_in.readlines()
file_out = input("File name to auto save as: ") + ".txt" if auto_save else None

stats = Stats()
mass_effect = MassEffect()
utils = Utils()
print_every = 5
print_plots_every = 1500
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
pause_for_plot = False
save_plot = False
on_win32 = sys.platform == "win32"

if load_file:
    weights = [float(weight) for weight in file_in.pop(0).split(",")]
    generation = original_gen = int(file_in.pop(0))
    trait_list = ['Species', 'Height', 'Weight', 'Speed', 'Power', 'Neural Net W1', 'Neural Net W2']
    population = []
    creature = []
    count = 0
    while file_in:
        if count % (len(trait_list)) == 0 and count != 0:
            population.append(creature)
            creature = []
            count = 0
        if trait_list[count] == 'Species':
            creature.append((trait_list[count], file_in.pop(0).strip("\n")))
        elif trait_list[count] == 'Neural Net W1' or trait_list[count] == 'Neural Net W2':
            trait = ""
            for i in range(2):
                trait += file_in.pop(0).strip("\n").strip(" ")
            creature.append((trait_list[count], np.array([float(t) for t in trait.split(",")])))
        else:
            creature.append((trait_list[count], float(file_in.pop(0).strip("\n"))))
        count += 1
else:
    weights = utils.create_weights()
    generation = original_gen = 0
    population = ng.generate_population(pop_n)

py = 0
if on_win32:
    import os
    import psutil
    pid = os.getpid()
    py = psutil.Process(pid)

stats.weights_summary(weights, pause)
while True:
    # for i in range(10000):
    utils.cpu_gpu_usage(py, generation, print_every=print_every)
    utils.check_pulse(population)
    stats.counting(population, generation, print_every=print_every)
    stats.creatures_summary(population, weights, generation, print_every=print_every)
    stats.show_nn_bar_graph(utils.get_median_nn_stats(population), generation, save_plot=save_plot, print_plots_every=print_plots_every, pause_for_plot=pause_for_plot)

    population = ng.evolve(population, weights)

    population = mass_effect.infect(population, prob_illness, prob_infected_individuals, pause=pause)
    population = mass_effect.war(population, prob_war, weights, to_fight, pause=pause)
    population = mass_effect.species_war(population, prob_species_war, weights, to_fight_species_war, pause=pause)
    population = mass_effect.civil_war(population, prob_civil_war, weights, to_fight_civil_war, pause=pause)

    if auto_save and generation % save_every == 0 and generation != original_gen or (generation == 0 and auto_save):
        def clean_text(text):
            return text.replace("(", "").replace(")", "").replace("'", "").replace("array", "").replace("[", "").replace("]", "")
        print("\nAuto saving...")
        with open(file_out, 'w') as f:
            f.write(clean_text(str(weights)) + "\n")
            f.write(str(generation) + "\n")
            for creature in population:
                for trait in creature:
                    cleaned_trait = clean_text(str(trait))
                    f.write(cleaned_trait[cleaned_trait.index(",") + 2:] + "\n")
        print("Done...")
        if pause_for_auto_save:
            input("\nPress ENTER to continue...")

    generation += 1
