import random
import numpy as np
from random import shuffle

species = [
    "Human",
    "Gritis",
    "Drakonian"
]
trait_list = [
    'Height',
    'Weight',
    'IQ',
    'Speed',
    'Power'
]
tournament_size = 3
prob_crossover = 0.8
prob_mutation = 0.5
num_of_traits = len(trait_list)


class Creatures:
    def generate_human(self):
        human = [('Species', 'Human')]
        mu, sigma = 67, 3  # height
        human.append(('Height', round(np.random.normal(mu, sigma), 3)))
        mu, sigma = 150, 15  # weight
        human.append(('Weight', round(np.random.normal(mu, sigma), 3)))
        mu, sigma = 100, 15  # IQ
        human.append(('IQ', round(np.random.normal(mu, sigma), 3)))
        mu, sigma = 40, 15  # Speed
        human.append(('Speed', round(np.random.normal(mu, sigma), 3)))
        mu, sigma = 40, 15  # Power
        human.append(('Power', round(np.random.normal(mu, sigma), 3)))
        return human

    def generate_gritis(self):
        gritis = [('Species', 'Gritis')]
        mu, sigma = 96, 5  # height
        gritis.append(('Height', round(np.random.normal(mu, sigma), 3)))
        mu, sigma = 200, 20  # weight
        gritis.append(('Weight', round(np.random.normal(mu, sigma), 3)))
        mu, sigma = 40, 12  # IQ
        gritis.append(('IQ', round(np.random.normal(mu, sigma), 3)))
        mu, sigma = 40, 15  # Speed
        gritis.append(('Speed', round(np.random.normal(mu, sigma), 3)))
        mu, sigma = 20, 11  # Power
        gritis.append(('Power', round(np.random.normal(mu, sigma), 3)))
        return gritis

    def generate_drakonian(self):
        drakonian = [('Species', 'Drakonian')]
        mu, sigma = 52, 5  # height
        drakonian.append(('Height', round(np.random.normal(mu, sigma), 3)))
        mu, sigma = 120, 12  # weight
        drakonian.append(('Weight', round(np.random.normal(mu, sigma), 3)))
        mu, sigma = 60, 12  # IQ
        drakonian.append(('IQ', round(np.random.normal(mu, sigma), 3)))
        mu, sigma = 80, 15  # Speed
        drakonian.append(('Speed', round(np.random.normal(mu, sigma), 3)))
        mu, sigma = 50, 10  # Power
        drakonian.append(('Power', round(np.random.normal(mu, sigma), 3)))
        return drakonian


class Stats:
    def weights_summary(self, weights):
        print(trait_list[weights.index(max(weights))], "is key")
        print(f"Weights rounded to four decimal places: ", end="")
        for i in range(len(trait_list)):
            if i == len(trait_list) - 1:
                print(f"{trait_list[i]}: {weights[i]:.2f}")
            else:
                print(f"{trait_list[i]}: {weights[i]:.2f} - ", end="")

    def creatures_summary(self, population, weights, generation, print_every):
        if generation % print_every == 0:
            humans = []
            human_count = 0
            gritiss = []
            gritis_count = 0
            drakonians = []
            drakonian_count = 0
            for creature in population:
                if creature[0][1] == species[0]:
                    humans.append(creature)
                    human_count += 1
                elif creature[0][1] == species[1]:
                    gritiss.append(creature)
                    gritis_count += 1
                else:
                    drakonians.append(creature)
                    drakonian_count += 1

            creature1 = []
            for i in range(len(trait_list)):
                trait = []
                for human in humans:
                    trait.append(human[i + 1][1])
                creature1.append(np.median(trait))
            fitness1 = 0
            for index in range(num_of_traits):
                fitness1 += creature1[index] * weights[index]

            creature2 = []
            for i in range(len(trait_list)):
                trait = []
                for gritis in gritiss:
                    trait.append(gritis[i + 1][1])
                creature2.append(np.median(trait))
            fitness2 = 0
            for index in range(num_of_traits):
                fitness2 += creature2[index] * weights[index]

            creature3 = []
            for i in range(len(trait_list)):
                trait = []
                for drakonian in drakonians:
                    trait.append(drakonian[i + 1][1])
                creature3.append(np.median(trait))
            fitness3 = 0
            for index in range(num_of_traits):
                fitness3 += creature3[index] * weights[index]

            print(" " * 16 + "Medians")
            final = [["Human"] + [fitness1] + creature1]
            final.append(["Gritis"] + [fitness2] + creature2)
            final.append(["Drakonian"] + [fitness3] + creature3)

            traits = [
                'Specie',
                'in"',
                'lbs',
                'IQ',
                'Speed',
                'Power'
            ]

            species_name_len = 0
            for species_name in ["Human", "Gritis", "Drakonian"]:
                if species_name_len < len(species_name):
                    species_name_len = len(species_name)

            trait_max_len = species_name_len
            for trait1 in final:
                if trait_max_len < len(trait1):
                    trait_max_len = len(trait1)

            max_len = 0
            for trait2 in traits:
                if max_len < len(trait2):
                    max_len = len(trait2)

            for i in range(len(final[0])):
                current_len = len(str(traits[i - 1]))
                if i == 0:
                    print(" " * len(traits[i - 1]), " " * (max_len - current_len), end=" ")
                    if human_count == 0:
                        final[0][1] = "Extinct"
                    if gritis_count == 0:
                        final[1][1] = "Extinct"
                    if drakonian_count == 0:
                        final[2][1] = "Extinct"
                elif i == 1:
                    print("Score", " " * ((max_len - current_len) + 1), end=" ")
                else:
                    print(f"{traits[i - 1]}", " " * (max_len - current_len), end=" ")
                for a in range(len(final)):
                    if i == 0:
                        current_len = len(str(final[a][i]))
                        print(f"{final[a][i]}", " " * (trait_max_len - current_len), end=" ")
                    else:
                        if type(final[a][i]) is not str:
                            current_len = len(f"{final[a][i]:.1f}")
                            print(f"{final[a][i]:.1f}", " " * (trait_max_len - current_len), end=" ")
                        else:
                            print(f"{final[a][i]}", " " * (trait_max_len - current_len), end=" ")
                print()

    def counting(self, population, generation, print_every=10):
        human_count = 0
        gritis_count = 0
        drakonian_count = 0
        for creature in population:
            if creature[0][1] == species[0]:
                human_count += 1
            elif creature[0][1] == species[1]:
                gritis_count += 1
            else:
                drakonian_count += 1

        dom_proportion = max(drakonian_count, max(human_count, gritis_count)) / len(population)
        dom_species = species[
            [human_count, gritis_count, drakonian_count].index(max(drakonian_count, max(human_count, gritis_count)))]
        if human_count == 0:
            human_count = "Extinct"
        if gritis_count == 0:
            gritis_count = "Extinct"
        if drakonian_count == 0:
            drakonian_count = "Extinct"
        if generation % print_every == 0:
            print(f"Gen {generation} |")
            print(f"DOMINATING SPECIES: {dom_species}\nProportion of {dom_species}s: {dom_proportion * 100:.2f}%")
            print(
                f"{human_count} Human\n{gritis_count} Gritis\n{drakonian_count} Drakonian\n{len(population)} total creatures")


def generate_population(num_of_creatures):
    creatures = Creatures()
    pop_creatures = []
    for i in range(num_of_creatures[0]):
        pop_creatures.append(creatures.generate_human())
    for i in range(num_of_creatures[1]):
        pop_creatures.append(creatures.generate_gritis())
    for i in range(num_of_creatures[2]):
        pop_creatures.append(creatures.generate_drakonian())
    shuffle(pop_creatures)
    return pop_creatures


def count_species(population):
    human_count = 0
    gritis_count = 0
    drakonian_count = 0
    for creature in population:
        if creature[0][1] == species[0]:
            human_count += 1
        elif creature[0][1] == species[1]:
            gritis_count += 1
        else:
            drakonian_count += 1

    return human_count, gritis_count, drakonian_count


def new_blood(weights, humans_medians, gritiss_medians, drakonians_medians, human_count, gritis_count, drakonian_count):
    dom_species = species[
        [human_count, gritis_count, drakonian_count].index(max(drakonian_count, max(human_count, gritis_count)))]

    contending_species = []
    mutator = .005
    if human_count != 0 and dom_species != "Human":
        human = [('Species', 'Human')]
        mu, sigma = humans_medians[0], humans_medians[0] * mutator  # height
        human.append(('Height', round(np.random.normal(mu, sigma), 3)))
        mu, sigma = humans_medians[1], humans_medians[1] * mutator  # weight
        human.append(('Weight', round(np.random.normal(mu, sigma), 3)))
        mu, sigma = humans_medians[2], humans_medians[2] * mutator  # IQ
        human.append(('IQ', round(np.random.normal(mu, sigma), 3)))
        mu, sigma = humans_medians[3], humans_medians[3] * mutator  # Speed
        human.append(('Speed', round(np.random.normal(mu, sigma), 3)))
        mu, sigma = humans_medians[4], humans_medians[4] * mutator  # Power
        human.append(('Power', round(np.random.normal(mu, sigma), 3)))
        contending_species.append(human)

    elif gritis_count != 0 and dom_species != "Gritis":
        gritis = [('Species', 'Gritis')]
        mu, sigma = gritiss_medians[0], gritiss_medians[0] * mutator  # height
        gritis.append(('Height', round(np.random.normal(mu, sigma), 3)))
        mu, sigma = gritiss_medians[1], gritiss_medians[1] * mutator  # weight
        gritis.append(('Weight', round(np.random.normal(mu, sigma), 3)))
        mu, sigma = gritiss_medians[2], gritiss_medians[2] * mutator  # IQ
        gritis.append(('IQ', round(np.random.normal(mu, sigma), 3)))
        mu, sigma = gritiss_medians[3], gritiss_medians[3] * mutator  # Speed
        gritis.append(('Speed', round(np.random.normal(mu, sigma), 3)))
        mu, sigma = gritiss_medians[4], gritiss_medians[4] * mutator  # Power
        gritis.append(('Power', round(np.random.normal(mu, sigma), 3)))
        contending_species.append(gritis)

    elif drakonian_count != 0 and dom_species != "Drakonian":
        drakonian = [('Species', 'Drakonian')]
        mu, sigma = drakonians_medians[0], drakonians_medians[0] * mutator  # height
        drakonian.append(('Height', round(np.random.normal(mu, sigma), 3)))
        mu, sigma = drakonians_medians[1], drakonians_medians[1] * mutator  # weight
        drakonian.append(('Weight', round(np.random.normal(mu, sigma), 3)))
        mu, sigma = drakonians_medians[2], drakonians_medians[2] * mutator  # IQ
        drakonian.append(('IQ', round(np.random.normal(mu, sigma), 3)))
        mu, sigma = drakonians_medians[3], drakonians_medians[3] * mutator  # Speed
        drakonian.append(('Speed', round(np.random.normal(mu, sigma), 3)))
        mu, sigma = drakonians_medians[4], drakonians_medians[4] * mutator  # Power
        drakonian.append(('Power', round(np.random.normal(mu, sigma), 3)))
        contending_species.append(drakonian)

    fitness_scores = calc_fitness(contending_species, weights)
    winner = contending_species[fitness_scores.index(max(fitness_scores))]
    return winner


def calc_fitness(population, weights):
    fitness_scores = []
    for creature in population:
        fitness = 0
        for index in range(num_of_traits):
            fitness += creature[index + 1][1] * weights[index]
        fitness_scores.append(fitness)
    return fitness_scores


def select_fittest(population, fitness_scores, weights):
    fitter_population = [population[fitness_scores.index(min(fitness_scores))]]
    pop_keep = random.randint(4, 8) * .1
    for i in range(int(len(population) * pop_keep)):
        r = random.randint(0, len(fitness_scores) - 1)
        best = fitness_scores[r]
        best_creature = population[r]
        for member in range(tournament_size):
            competitor_index = random.randint(0, len(fitness_scores) - 1)
            if fitness_scores[competitor_index] > best:
                best = fitness_scores[competitor_index]
                best_creature = population[competitor_index]
        fitter_population.append(best_creature)

    humans = []
    human_count = 0
    gritiss = []
    gritis_count = 0
    drakonians = []
    drakonian_count = 0
    for creature in population:
        if creature[0][1] == species[0]:
            humans.append(creature)
            human_count += 1
        elif creature[0][1] == species[1]:
            gritiss.append(creature)
            gritis_count += 1
        else:
            drakonians.append(creature)
            drakonian_count += 1

    humans_medians = []
    for i in range(len(trait_list)):
        trait = []
        for human in humans:
            trait.append(human[i + 1][1])
        humans_medians.append(np.median(trait))

    gritiss_medians = []
    for i in range(len(trait_list)):
        trait = []
        for gritis in gritiss:
            trait.append(gritis[i + 1][1])
        gritiss_medians.append(np.median(trait))

    drakonians_medians = []
    for i in range(len(trait_list)):
        trait = []
        for drakonian in drakonians:
            trait.append(drakonian[i + 1][1])
        drakonians_medians.append(np.median(trait))

    for i in range(len(population) - len(fitter_population)):
        winner = new_blood(weights, humans_medians, gritiss_medians, drakonians_medians, human_count, gritis_count,
                           drakonian_count)
        fitter_population.append(winner)
    return fitter_population


def crossover(population):
    def make_child():
        parent1 = population[creature]
        parent2 = population[to_breed_with]
        r = random.randint(1, num_of_traits)
        population[creature] = parent1[:r] + parent2[r:]
        population[to_breed_with] = parent2[:r] + parent1[r:]

    for creature in range((len(population))):
        to_breed_with = random.randint(0, len(population) - 1)
        if prob_crossover <= random.random() and population[creature][0][1] == population[to_breed_with][0][1]:
            for i in range(1, 6):
                prob_of_next_child = 0.4 / i
                if prob_of_next_child <= random.random() or i == 1:
                    make_child()
                else:
                    break
    return population


def mutation(population):
    for i in range(int((len(population) - 1))):
        if prob_mutation <= random.random():
            creature = population[i]
            for a in range(random.randint(0, num_of_traits - 2)):  # -1 species -1 IndexOutOfBounds
                index = random.randint(1, num_of_traits)
                trait = old_trait = creature[index][1]
                if random.randint(0, 1) == 0:
                    trait = round(trait + (trait * .1), 2)
                else:
                    trait = round(trait - (trait * .1), 2)
                creature[index] = (creature[index][0], trait) if trait > 1 else (creature[index][0], old_trait)
            population.append(creature)
        return population


def breed(population):
    return mutation(crossover(population))


def evolve(population, weights):
    fitness_scores = calc_fitness(population, weights)
    return breed(select_fittest(population, fitness_scores, weights))
