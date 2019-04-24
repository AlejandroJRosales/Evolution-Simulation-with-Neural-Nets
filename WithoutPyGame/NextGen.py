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
    'Strength'
]
tournament_size = 3
pop_keep = .6
prob_crossover = 0.8
prob_mutation = 0.5
num_of_traits = len(trait_list)


class Creatures:
    def generate_human(self):
        human = [('Species', 'Human')]
        human.append(('Height', random.randint(4, 6) + round(random.random(), 2)))
        human.append(('Weight', round(human[1][1] * random.randint(25, 35) + random.random(), 2)))
        human.append(('IQ', random.randint(70, 170)))
        speed = round(random.randint(20, 70) - (human[2][1] * 0.1))
        human.append(('Speed', speed if speed > 1 else 5))
        human.append(('Strength', round(random.randint(10, 60) + (human[2][1] * 0.2))))
        return human

    def generate_gritis(self):
        gritis = [('Species', 'Gritis')]
        gritis.append(('Height', random.randint(7, 9) + round(random.random(), 2)))
        gritis.append(('Weight', round(gritis[1][1] * random.randint(25, 35) + random.random(), 2)))
        gritis.append(('IQ', random.randint(50, 80)))
        speed = round(random.randint(10, 40) - (gritis[2][1] * 0.1))
        gritis.append(('Speed', speed if speed > 1 else 5))
        gritis.append(('Strength', round(random.randint(60, 100) + (gritis[2][1] * 0.2))))
        return gritis

    def generate_drakonian(self):
        drakonian = [('Species', 'Drakonian')]
        drakonian.append(('Height', random.randint(8, 10) + round(random.random(), 2)))
        drakonian.append(('Weight', round(drakonian[1][1] * random.randint(25, 35) + random.random(), 2)))
        drakonian.append(('IQ', random.randint(10, 30)))
        speed = round(random.randint(60, 100) - (drakonian[2][1] * 0.1))
        drakonian.append(('Speed', speed if speed > 1 else 20))
        drakonian.append(('Strength', round(random.randint(10, 40) + (drakonian[2][1] * 0.2))))
        return drakonian


class Stats:
    def weights_summary(self, weights):
        print(trait_list[weights.index(max(weights))], "is key")
        print(f"Weights rounded to four decimal places: ", end="")
        for i in range(len(trait_list)):
            if i == len(trait_list) - 1:
                print(f"{trait_list[i]}: {weights[i]:.4f}")
            else:
                print(f"{trait_list[i]}: {weights[i]:.4f} - ", end="")

    def creatures_summary(self, population, weights, generation, print_every):
        if generation % print_every == 0:
            humans = []
            gritiss = []
            drakonians = []
            for creature in population:
                if creature[0][1] == species[0]:
                    humans.append(creature)
                elif creature[0][1] == species[1]:
                    gritiss.append(creature)
                else:
                    drakonians.append(creature)

            humans, gritiss, drakonians = sorted(humans), sorted(gritiss), sorted(drakonians)

            fitness_scores = calc_fitness(population, weights)
            best_creature = population[fitness_scores.index(max(fitness_scores))]
            print(f"FITTEST CREATURE: ", end="")
            for i in range(len(best_creature)):
                if i == 0:
                    print(f"{best_creature[i][1]} [Score: {max(fitness_scores):.2f}]", end=": [")
                elif i == len(best_creature) - 1:
                    print(f"{best_creature[i][0]}: {best_creature[i][1]:.2f}]")
                else:
                    print(f"{best_creature[i][0]}: {best_creature[i][1]:.2f}", end=", ")

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

            print("Medians")
            final = [["Human"] + [fitness1] + creature1]
            final.append(["Gritis"] + [fitness2] + creature2)
            final.append(["Drakonian"] + [fitness3] + creature3)

            traits = [
                'Specie',
                'ft',
                'lbs',
                'IQ',
                'Speed',
                'Stngth'
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
                elif i == 1:
                    print("Score", " " * ((max_len - current_len) + 1), end=" ")
                else:
                    print(f"{traits[i - 1]}", " " * (max_len - current_len), end=" ")
                for a in range(len(final)):
                    if i == 0:
                        current_len = len(str(final[a][i]))
                        print(f"{final[a][i]}", " " * (trait_max_len - current_len), end=" ")
                    else:
                        current_len = len(f"{final[a][i]:.2f}")
                        print(f"{final[a][i]:.2f}", " " * (trait_max_len - current_len),  end=" ")
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
        dom_species = species[[human_count, gritis_count, drakonian_count].index(max(drakonian_count, max(human_count, gritis_count)))]
        if human_count == 0:
            human_count = "Extinct"
        if gritis_count == 0:
            gritis_count = "Extinct"
        if drakonian_count == 0:
            drakonian_count = "Extinct"
        if generation % print_every == 0:
            print(f"Gen {generation} |")
            print(f"DOMINATING SPECIES: {dom_species} - Proportion of {dom_species}s: {dom_proportion * 100:.2f}%", end=" - ")
            print(
                f"counts=(Human: {human_count}, Gritis: {gritis_count}, Drakonian: {drakonian_count}) - {len(population)} creatures")


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
    if dom_species != "Human":
        human = [('Species', 'Human')]
        height = humans_medians[0] + random.randint(1, 10) / 100 if random.randint(0, 1) == 0 else humans_medians[
                                                                                                       0] - random.randint(
            1, 10) / 100
        human.append(('Height', height))
        weight = (humans_medians[1] + random.randint(1, 10) / 100 if random.randint(0, 1) == 0 else humans_medians[
                                                                                                        1] - random.randint(
            1, 10) / 100)
        human.append(('Weight', weight))
        iq = humans_medians[2] + random.randint(1, 10) / 100 if random.randint(0, 1) == 0 else humans_medians[
                                                                                                   2] - random.randint(
            1, 10) / 100
        human.append(('IQ', iq))
        speed = humans_medians[3] + random.randint(1, 10) / 100 if random.randint(0, 1) == 0 else humans_medians[
                                                                                                      3] - random.randint(
            1, 10) / 100
        human.append(('Speed', speed))
        strength = humans_medians[4] + random.randint(1, 10) / 100 if random.randint(0, 1) == 0 else humans_medians[
                                                                                                         4] - random.randint(
            1, 10) / 100
        human.append(('Strength', strength))
        contending_species.append(human)

    elif dom_species != "Gritis":
        gritis = [('Species', 'Gritis')]
        height = gritiss_medians[0] + random.randint(1, 10) / 100 if random.randint(0, 1) == 0 else gritiss_medians[
                                                                                                        0] - random.randint(
            1, 10) / 100
        gritis.append(('Height', height))
        weight = (
            gritiss_medians[1] + random.randint(1, 10) / 100 if random.randint(0, 1) == 0 else gritiss_medians[
                                                                                                   1] - random.randint(
                1, 10) / 100)
        gritis.append(('Weight', weight))
        iq = gritiss_medians[2] + random.randint(1, 10) / 100 if random.randint(0, 1) == 0 else gritiss_medians[
                                                                                                    2] - random.randint(
            1, 10) / 100
        gritis.append(('IQ', iq))
        speed = gritiss_medians[3] + random.randint(1, 10) / 100 if random.randint(0, 1) == 0 else gritiss_medians[
                                                                                                       3] - random.randint(
            1, 10) / 100
        gritis.append(('Speed', speed))
        strength = gritiss_medians[4] + random.randint(1, 10) / 100 if random.randint(0, 1) == 0 else gritiss_medians[
                                                                                                          4] - random.randint(
            1, 10) / 100
        gritis.append(('Strength', strength))
        contending_species.append(gritis)

    else:
        drakonian = [('Species', 'Drakonian')]
        height = drakonians_medians[0] + random.randint(1, 10) / 100 if random.randint(0, 1) == 0 else \
        drakonians_medians[
            0] - random.randint(
            1, 10) / 100
        drakonian.append(('Height', height))
        weight = (
            drakonians_medians[1] + random.randint(1, 10) / 100 if random.randint(0, 1) == 0 else drakonians_medians[
                                                                                                      1] - random.randint(
                1, 10) / 100)
        drakonian.append(('Weight', weight))
        iq = drakonians_medians[2] + random.randint(1, 10) / 100 if random.randint(0, 1) == 0 else drakonians_medians[
                                                                                                       2] - random.randint(
            1, 10) / 100
        drakonian.append(('IQ', iq))
        speed = drakonians_medians[3] + random.randint(1, 10) / 100 if random.randint(0, 1) == 0 else \
        drakonians_medians[
            3] - random.randint(
            1, 10) / 100
        drakonian.append(('Speed', speed))
        strength = drakonians_medians[4] + random.randint(1, 10) / 100 if random.randint(0, 1) == 0 else \
        drakonians_medians[
            4] - random.randint(
            1, 10) / 100
        drakonian.append(('Strength', strength))
        contending_species.append(drakonian)

    fitness_scores = calc_fitness(contending_species, weights)
    winner = contending_species[fitness_scores.index(max(fitness_scores))]
    return winner, winner[0][1], 0


def calc_fitness(population, weights):
    fitness_scores = []
    for creature in population:
        fitness = 0
        for index in range(num_of_traits):
            fitness += creature[index + 1][1] * weights[index]
        fitness_scores.append(fitness)
    return fitness_scores


def select_fittest(population, fitness_scores, weights):
    # idk man
    for creature in range(len(population)):
        for trait in range(len(population[creature])):
            if "nan" in population[creature][trait]:
                print(population[creature][trait])
                population.remove(creature)

    fitter_population = [population[fitness_scores.index(min(fitness_scores))]]
    pop_keep = random.randint(1, 8) * .1
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

    humans, gritiss, drakonians = sorted(humans), sorted(gritiss), sorted(drakonians)

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
        winner, species_name, add = new_blood(weights, humans_medians, gritiss_medians, drakonians_medians, human_count, gritis_count, drakonian_count)
        fitter_population.append(winner)

        if i != len(population):
            if species_name == species[0]:
                human_count += 1
            if species_name == species[1]:
                gritis_count += 1
            if species_name == species[2]:
                drakonian_count += 1
    return fitter_population


def crossover(population):
    for creature in range((len(population))):
        to_breed_with = random.randint(0, len(population) - 1)
        if random.random() <= prob_crossover and population[creature][0][1] == population[to_breed_with][0][1]:
            parent1 = population[creature]
            parent2 = population[to_breed_with]
            r = random.randint(1, num_of_traits)
            population[creature] = parent1[:r] + parent2[r:]
            population[to_breed_with] = parent2[:r] + parent1[r:]
    return population


def mutation(population):
    for i in range(int((len(population) - 1))):
        if random.random() <= prob_mutation:
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
