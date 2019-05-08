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
prob_crossover = 0.8
prob_mutation = 0.5
required_pack_size = 3
prob_infected = .7
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

    def creatures_summary(self, population, weights, generation=0, print_every=1):
        check_pulse(population)

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
                'Species',
                'Score',
                'Feet',
                'lbs',
                'IQ',
                'Speed',
                'Power'
            ]

            max_str_len = 0
            for species_name in species:
                if max_str_len < len(species_name):
                    max_str_len = len(species_name)

            for trait in final:
                if max_str_len < len(trait):
                    max_str_len = len(trait)

            max_trait_name_len = 0
            for trait in traits:
                if max_trait_name_len < len(trait):
                    max_trait_name_len = len(trait)

            #   Species  Score               Height   Weight   IQ      Speed   Strength
            # [['Human', 150.49075649967057, 67.002, 149.455, 100.022, 39.695, 39.763],
            for trait in range(len(traits)):
                print()
                print(traits[trait] + " " * (max_trait_name_len - len(traits[trait])), end=" ")
                for creature in final:
                    if traits[trait] == "Species":
                        print(creature[trait], end=" " * (max_str_len - len(creature[trait])))
                    elif traits[trait] == "Score":
                        if np.isnan(creature[trait]):
                            print("Extinct", end=" " * (max_str_len - len(str("Extinct"))))
                        else:
                            rounded_score = round(creature[trait], 2)
                            print(rounded_score, end=" " * (max_str_len - len(str(rounded_score))))
                    elif np.isnan(creature[trait]):
                        if traits[trait] == "Feet":
                            print("Nan", end=" " * (max_str_len - len(str("Nan"))))
                        else:
                            print("Nan", end=" " * (max_str_len - len(str("Nan"))))
                    else:
                        if traits[trait] == "Feet":
                            feet = int(creature[trait] / 12)
                            inches = int(creature[trait]) % 12
                            height = f"{feet}'{inches}\""
                            print(height, end=" " * (max_str_len - len(str(height))))
                        else:
                            trait_rounded = round(creature[trait], 2)
                            print(trait_rounded, end=" " * (max_str_len - len(str(trait_rounded))))
            print()

    def counting(self, population, generation, print_every=1):
        check_pulse(population)

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


class MassExtinction:
    def infect(self, population):
        safe_population = []
        count = 0
        for creature in population:
            if prob_infected <= random.random():
                safe_population.append(creature)
            else:
                count += 1
        print(f"INFECTED: {count/len(population)}% died")
        return safe_population


def check_pulse(population):
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

    if [human_count, gritis_count, drakonian_count].count(0) > 1 \
            and human_count + gritis_count + drakonian_count < 2:
        raise Exception("\n\nAll Species Extinct... This is what happens when you play god")


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


def new_blood(weights, humans_medians, gritiss_medians, drakonians_medians, human_count, gritis_count, drakonian_count):
    dom_species = species[
        [human_count, gritis_count, drakonian_count].index(max(drakonian_count, max(human_count, gritis_count)))]

    contending_species = []
    height_mutator = .25
    weight_mutator = .25
    iq_mutator = .25
    speed_mutator = .25
    power_mutator = .25

    if [human_count, drakonian_count, gritis_count].count(0) == 2:
        if human_count != 0:
            human = [('Species', 'Human')]
            mu, sigma = humans_medians[0], height_mutator  # height
            human.append(('Height', round(np.random.normal(mu, sigma), 3)))
            mu, sigma = humans_medians[1], weight_mutator  # weight
            human.append(('Weight', round(np.random.normal(mu, sigma), 3)))
            mu, sigma = humans_medians[2], iq_mutator  # IQ
            human.append(('IQ', round(np.random.normal(mu, sigma), 3)))
            mu, sigma = humans_medians[3], speed_mutator  # Speed
            human.append(('Speed', round(np.random.normal(mu, sigma), 3)))
            mu, sigma = humans_medians[4], power_mutator  # Power
            human.append(('Power', round(np.random.normal(mu, sigma), 3)))
            return human

        if gritis_count != 0:
            gritis = [('Species', 'Gritis')]
            mu, sigma = gritiss_medians[0], height_mutator  # height
            gritis.append(('Height', round(np.random.normal(mu, sigma), 3)))
            mu, sigma = gritiss_medians[1], weight_mutator  # weight
            gritis.append(('Weight', round(np.random.normal(mu, sigma), 3)))
            mu, sigma = gritiss_medians[2], iq_mutator  # IQ
            gritis.append(('IQ', round(np.random.normal(mu, sigma), 3)))
            mu, sigma = gritiss_medians[3], speed_mutator  # Speed
            gritis.append(('Speed', round(np.random.normal(mu, sigma), 3)))
            mu, sigma = gritiss_medians[4], power_mutator  # Power
            gritis.append(('Power', round(np.random.normal(mu, sigma), 3)))
            return gritis

        if drakonian_count != 0:
            drakonian = [('Species', 'Drakonian')]
            mu, sigma = drakonians_medians[0], height_mutator  # height
            drakonian.append(('Height', round(np.random.normal(mu, sigma), 3)))
            mu, sigma = drakonians_medians[1], weight_mutator  # weight
            drakonian.append(('Weight', round(np.random.normal(mu, sigma), 3)))
            mu, sigma = drakonians_medians[2], iq_mutator  # IQ
            drakonian.append(('IQ', round(np.random.normal(mu, sigma), 3)))
            mu, sigma = drakonians_medians[3], speed_mutator  # Speed
            drakonian.append(('Speed', round(np.random.normal(mu, sigma), 3)))
            mu, sigma = drakonians_medians[4], power_mutator  # Power
            drakonian.append(('Power', round(np.random.normal(mu, sigma), 3)))
            return drakonian

    else:
        if dom_species != "Human" and human_count != 0:
            human = [('Species', 'Human')]
            mu, sigma = humans_medians[0], height_mutator  # height
            human.append(('Height', round(np.random.normal(mu, sigma), 3)))
            mu, sigma = humans_medians[1], weight_mutator  # weight
            human.append(('Weight', round(np.random.normal(mu, sigma), 3)))
            mu, sigma = humans_medians[2], iq_mutator  # IQ
            human.append(('IQ', round(np.random.normal(mu, sigma), 3)))
            mu, sigma = humans_medians[3], speed_mutator  # Speed
            human.append(('Speed', round(np.random.normal(mu, sigma), 3)))
            mu, sigma = humans_medians[4], power_mutator  # Power
            human.append(('Power', round(np.random.normal(mu, sigma), 3)))
            contending_species.append(human)

        if dom_species != "Gritis" and gritis_count != 0:
            gritis = [('Species', 'Gritis')]
            mu, sigma = gritiss_medians[0], height_mutator  # height
            gritis.append(('Height', round(np.random.normal(mu, sigma), 3)))
            mu, sigma = gritiss_medians[1], weight_mutator  # weight
            gritis.append(('Weight', round(np.random.normal(mu, sigma), 3)))
            mu, sigma = gritiss_medians[2], iq_mutator  # IQ
            gritis.append(('IQ', round(np.random.normal(mu, sigma), 3)))
            mu, sigma = gritiss_medians[3], speed_mutator  # Speed
            gritis.append(('Speed', round(np.random.normal(mu, sigma), 3)))
            mu, sigma = gritiss_medians[4], power_mutator  # Power
            gritis.append(('Power', round(np.random.normal(mu, sigma), 3)))
            contending_species.append(gritis)

        if dom_species != "Drakonian" and drakonian_count != 0:
            drakonian = [('Species', 'Drakonian')]
            mu, sigma = drakonians_medians[0], height_mutator  # height
            drakonian.append(('Height', round(np.random.normal(mu, sigma), 3)))
            mu, sigma = drakonians_medians[1], weight_mutator  # weight
            drakonian.append(('Weight', round(np.random.normal(mu, sigma), 3)))
            mu, sigma = drakonians_medians[2], iq_mutator  # IQ
            drakonian.append(('IQ', round(np.random.normal(mu, sigma), 3)))
            mu, sigma = drakonians_medians[3], speed_mutator  # Speed
            drakonian.append(('Speed', round(np.random.normal(mu, sigma), 3)))
            mu, sigma = drakonians_medians[4], power_mutator  # Power
            drakonian.append(('Power', round(np.random.normal(mu, sigma), 3)))
            contending_species.append(drakonian)

        # This is because n_species = 0  so not chosen and dominating species not chosen,
        # thus len of contending_species = 1. Easier than printing out big chunk of code again
        if len(contending_species) != 1:
            fitness_scores = calc_fitness(contending_species, weights)
            probability = .5
            new_blood_child_benefit = random.randint(15, 30) / 100
            if fitness_scores.index(max(fitness_scores)) == 0:
                probability += new_blood_child_benefit
            elif fitness_scores.index(max(fitness_scores)) == 1:
                probability -= new_blood_child_benefit
            if random.random() <= probability:
                winner = contending_species[0]
            else:
                winner = contending_species[1]
            return winner

        else:
            return contending_species[0]


def calc_fitness(population, weights):
    fitness_scores = []
    for creature in population:
        fitness = 0
        for index in range(num_of_traits):
            fitness += creature[index + 1][1] * weights[index]
        fitness_scores.append(fitness)
    return fitness_scores


def select_fittest(population, fitness_scores, weights):
    tournament_size = random.randint(3, 6)

    humans = []
    human_count = 0
    gritiss = []
    gritis_count = 0
    drakonians = []
    drakonian_count = 0
    index = 0
    human_index = 0
    gritis_index = 0
    drakonian_index = 0
    for creature in population:
        if creature[0][1] == species[0]:
            humans.append(creature)
            human_count += 1
            if human_count == 1:
                human_index = index
        elif creature[0][1] == species[1]:
            gritiss.append(creature)
            gritis_count += 1
            if gritis_count == 1:
                gritis_index = index
        else:
            drakonians.append(creature)
            drakonian_count += 1
            if drakonian_count == 1:
                drakonian_index = index

        index += 1

    if human_count == 1:
        population.pop(human_index)
        fitness_scores.pop(human_index)
    if gritis_count == 1:
        population.pop(gritis_index)
        fitness_scores.pop(gritis_index)
    if drakonian_count == 1:
        population.pop(drakonian_index)
        fitness_scores.pop(drakonian_index)

    fitter_population = [population[fitness_scores.index(max(fitness_scores))]]
    pop_keep = random.randint(4, 8) * .1
    for i in range(int(len(population) * pop_keep)):
        competitors = []
        for member in range(tournament_size - 1):
            competitor_index = random.randint(0, len(fitness_scores) - 1)
            competitor_fitness = fitness_scores[competitor_index]
            competitors.append((competitor_index, competitor_fitness))

        competitors_names = []
        for competitor in competitors:
            competitors_names.append(population[competitor[0]][0][1])

        if competitors_names.count("Drakonian") >= required_pack_size:
            drakonians_competitors = []
            for competitor in range(len(competitors)):
                if competitors_names[competitor] == "Drakonian":
                    drakonians_competitors.append(competitors[competitor])

            for a in range(random.randint(1, 2)):
                best_fitness_score = 0
                best_creature = []
                best_creature_index = 0
                index = 0
                for drakonian in drakonians_competitors:
                    if drakonian[1] > best_fitness_score:
                        best_fitness_score = drakonian[1]
                        best_creature = population[drakonian[0]]
                        best_creature_index = index
                    index += 1
                drakonians_competitors.pop(best_creature_index)
                fitter_population.append(best_creature)
        else:
            r = random.randint(0, len(fitness_scores) - 1)
            best_fitness_score = fitness_scores[r]
            best_creature = population[r]
            for competitor in competitors:
                if competitor[1] > best_fitness_score:
                    best_fitness_score = competitor[1]
                    best_creature = population[competitor[0]]
            fitter_population.append(best_creature)

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
    check_pulse(population)
    try:
        fitness_scores = calc_fitness(population, weights)
        return breed(select_fittest(population, fitness_scores, weights))
    except Exception:
        raise Exception("\n\nSimulation Broken... This is what happens when you play god")
