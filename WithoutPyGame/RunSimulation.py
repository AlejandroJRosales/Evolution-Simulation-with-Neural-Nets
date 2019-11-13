"""
CONVERT TO BLENDER OBJECTS - Change to "CATD" type dna or numbers or number representing "CATD"
"""

import sys
import numpy as np
import NextGen as ng
from NextGen import Stats, MassEffect, Utils

pop_n = [1000, 1000, 1000]  # Number of: Charlens, Gritiss, Drackonians

file_in_name = input("File name to load previous simulation from (enter nothing to skip): ")
file_out_name = input("File name to auto save as (enter nothing to skip): ")

load_file = True if file_in_name != "" else False
auto_save = True if file_out_name != "" else False

stats = Stats()
mass_effect = MassEffect()
utils = Utils()

print_every = 10
print_plots_every = 300
save_every = 20
pause = False
pause_for_plot = False
pause_for_auto_save = False
save_plot = True

prob_illness = .0001
prob_war = .0001
prob_species_war = .001
prob_civil_war = 0.001
prob_infected_individuals = 0.8
to_fight = 0.8
to_fight_species_war = 0.8
to_fight_civil_war = 0.8

on_pc = sys.platform != "ios"

if load_file:
    file_in = open(file_in_name + ".txt", "r").readlines()
    file_in.pop(0)  # Remove creature count, was for display purposes so not needed
    print("Loading parameters of your world...")
    weights = [float(weight) for weight in file_in.pop(0).split(",")]
    year = original_year = int(file_in.pop(0))
    trait_list = ['Species', 'Age', 'Gen.', 'Health', 'Resources', 'Height', 'Weight', 'Speed', 'Power', 'Neural Net W1', 'Neural Net W2']
    population = []
    creature = []
    print("Parameters loaded")
    print("Loading creatures into your world...")
    count = 0
    while file_in:
        if count % (len(trait_list)) == 0 and count != 0:
            population.append(creature)
            creature = []
            count = 0
        if trait_list[count] == 'Species':
            creature.append((trait_list[count], file_in.pop(0).strip("\n")))
        elif trait_list[count] == 'Neural Net W1' or trait_list[count] == 'Neural Net W2':
            trait = file_in.pop(0)
            creature.append((trait_list[count], np.array([float(t) for t in trait.split(",")])))

        else:
            creature.append((trait_list[count], float(file_in.pop(0).strip("\n"))))
        count += 1
    print("Creatures Loaded")
    print("All set!")
else:
    weights = utils.create_weights()
    year = original_year = 0
    population = ng.generate_population(pop_n, weights)

py = 0
if on_pc:
    import os
    import psutil
    pid = os.getpid()
    py = psutil.Process(pid)

print(f"Starting with {len(population):,} creatures in your world")
input("\nPress ENTER to continue...\n")

stats.weights_summary(weights, pause)
while True:
    # for i in range(10000):
    utils.cpu_ram_usage(on_pc, py, year, print_every=print_every)
    utils.check_pulse(population)
    stats.counting(population, year, print_every=print_every)
    stats.creatures_summary(population, weights, year, print_every=print_every)
    stats.show_nn_bar_graph(utils.get_median_nn_stats(population), year, save_plot=save_plot, print_plots_every=print_plots_every, pause_for_plot=pause_for_plot)

    population = ng.evolve(population, weights)

    population = mass_effect.infect(population, prob_illness, prob_infected_individuals, pause=pause)
    population = mass_effect.war(population, prob_war, weights, to_fight, pause=pause)
    population = mass_effect.species_war(population, prob_species_war, weights, to_fight_species_war, pause=pause)
    population = mass_effect.civil_war(population, prob_civil_war, weights, to_fight_civil_war, pause=pause)

    if auto_save and year % save_every == 0 and year != original_year or (year == 0 and auto_save):
        def clean_text(text):
            return text.replace("(", "").replace(")", "").replace("'", "").replace("array", "").replace("[", "").replace("]", "")
        print("\nAuto saving...")
        with open(file_out_name + ".txt", 'w') as f:
            f.write(f"{len(population):,}\n")
            f.write(clean_text(str(weights)) + "\n")
            f.write(str(year) + "\n")
            for creature in population:
                # if len(creature) <
                for trait in creature:
                    if isinstance(trait[1], np.ndarray):
                        new_weights = []
                        for weight in range(len(trait[1])):
                            new_weights.append('{0:f}'.format(trait[1][weight]))
                        trait = ("Dummy", new_weights)
                    cleaned_trait = clean_text(str(trait))
                    f.write(cleaned_trait[cleaned_trait.index(",") + 2:] + "\n")
        print("Saved...\n")
        if pause_for_auto_save:
            input("\nPress ENTER to continue...\n")

    year += 1
