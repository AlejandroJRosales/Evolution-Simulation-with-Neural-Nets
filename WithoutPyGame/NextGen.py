import sys
import random
import matplotlib.pyplot as plt
import numpy as np

species = [
    "Charlen",
    "Gritis",
    "Drakonian"
]
trait_list = [
    'Height',
    'Weight',
    'Speed',
    'Power',
    'Neural Net W1',
    'Neural Net W2'
]
prob_crossover = 0.001
prob_mutation = 0.35
mutation_rate = 0.001
max_num_kids = 5
kids_after_start_prob = 0.5
num_of_traits = len(trait_list)
prob_change_fighters = 0.2
damage_damper = .8
nn_weights1_len = 6
nn_weights2_len = 6


class Stats:
    def weights_summary(self, weights, pause=True):
        print(f"Weights rounded to four decimal places: ", end="")
        for i in range(len(weights)):
            if i == len(trait_list) - 1:
                print(f"{trait_list[i]}: {weights[i]:.2f}")
            else:
                print(f"{trait_list[i]}: {weights[i]:.2f} : ", end="")
        if pause:
            input("\nPress ENTER to continue...")

    def creatures_summary(self, population, weights, generation=0, print_every=1):
        if generation % print_every == 0:
            utils = Utils()
            charlen_median_traits, gritis_median_traits, drakonian_median_traits = utils.get_medians(population)

            fitness1 = 0
            for index in range(len(weights)):
                fitness1 += charlen_median_traits[index] * weights[index]

            fitness2 = 0
            for index in range(len(weights)):
                fitness2 += gritis_median_traits[index] * weights[index]

            fitness3 = 0
            for index in range(len(weights)):
                fitness3 += drakonian_median_traits[index] * weights[index]

            # Combine species into on array
            # print(fitness1)
            final = [["Charlen"] + [fitness1] + charlen_median_traits]
            final.append(["Gritis"] + [fitness2] + gritis_median_traits)
            final.append(["Drakonian"] + [fitness3] + drakonian_median_traits)

            updated_trait_list = [
                'Species',
                'Fitness',  # Fitness Added
                'Feet',
                'lbs',
                'Speed',
                'Power',
                'Neural Net W1',
                'Neural Net W2'
            ]

            # Find largest string length
            max_str_len = max(len(max(species, key=len)), len(max(final, key=len))) - 2
            max_trait_name_len = len(max(updated_trait_list, key=len))

            # Print out medians traits for all species
            print(" " * 22 + "Medians")
            for trait in range(len(updated_trait_list) - 2):
                if trait != 0:
                    print()
                print(updated_trait_list[trait] + " " * (max_trait_name_len - len(updated_trait_list[trait])), end=" ")
                for creature in final:
                    if updated_trait_list[trait] == "Species":
                        print(creature[trait], end=" " * (max_str_len - len(creature[trait])))
                    elif updated_trait_list[trait] == "Fitness":
                        if np.isnan(creature[trait]):
                            print("Extinct", end=" " * (max_str_len - len(str("Extinct"))))
                        else:
                            rounded_score = round(creature[trait], 2)
                            print(rounded_score, end=" " * (max_str_len - len(str(rounded_score))))
                    elif np.isnan(creature[trait]):
                        if updated_trait_list[trait] == "Feet":
                            print("Nan", end=" " * (max_str_len - len(str("Nan"))))
                        else:
                            print("Nan", end=" " * (max_str_len - len(str("Nan"))))
                    else:
                        if updated_trait_list[trait] == "Feet":
                            feet = int(creature[trait] / 12)
                            inches = int(creature[trait]) % 12
                            height = f"{feet}'{inches}\""
                            print(height, end=" " * (max_str_len - len(str(height))))
                        else:
                            trait_rounded = round(creature[trait], 2)
                            print(trait_rounded, end=" " * (max_str_len - len(str(trait_rounded))))

            nn_input = ["c1 fitness",
                        "c2 fitness",
                        "c1 health",
                        "c2 health",
                        "resource reward",
                        "c2 resources"]

            # Use spaces because of difference in use from pycharm to pythonista
            print("\n\n", " " * 9, "Neural Network Medians")
            # print("  Input Names", " " * 11, "Weights")
            print(" " * 19, "C.      G.      D.")
            print(" " * 16, "W1")
            for col in range(nn_weights1_len):
                input_name = nn_input[col]
                print(input_name, end=" " * ((len("resource reward") + 2) - len(input_name)))
                for row in range(len(species)):
                    try:
                        weight = round(float(final[row][6][col]), 4)
                    except:
                        weight = np.nan
                    print(weight, end=" " * (8 - len(str(weight))))
                print()
            print(" " * 16, "W2")
            for col in range(nn_weights2_len):
                print(" " * (len("resource reward") + 2), end="")
                for row in range(len(species)):
                    try:
                        weight = round(float(final[row][7][col]), 4)
                    except:
                        weight = np.nan
                    print(weight, end=" " * (8 - len(str(weight))))
                print()
            print()

    def counting(self, population, generation, print_every=1):
        if generation % print_every == 0:
            print()
            utils = Utils()
            charlen_count, gritis_count, drakonian_count = utils.count_creatures(population)

            if charlen_count == 0:
                charlen_count = "Extinct"
            if gritis_count == 0:
                gritis_count = "Extinct"
            if drakonian_count == 0:
                drakonian_count = "Extinct"
            print(f"Gen {generation} |")
            print("Counts:")
            print(f"\t{charlen_count:,} Charlen") if isinstance(charlen_count, int) else print(f"\tCharlen"
                                                                                               f"{charlen_count}")
            print(f"\t{gritis_count:,} Gritis") if isinstance(gritis_count, int) else print(f"\tGritis {gritis_count}")
            print(f"\t{drakonian_count:,} Drakonian") if isinstance(drakonian_count, int) else print(
                f"\tDrakonian {drakonian_count}")
            print(f"\t{len(population):,} total creatures")

    def show_nn_bar_graph(self, nn_medians, generation, save_plot=True, print_plots_every=500, pause_for_plot=True):
        if generation % print_plots_every == 0 and generation != 0:
            nn_input = ["c1 fitness",
                        "c2 fitness",
                        "c1 health",
                        "c2 health",
                        "resource reward",
                        "c2 resources"]
            fig, ax = plt.subplots()
            y = np.arange(len(nn_input)) * 4
            charlen_weights = nn_medians[0]
            gritis_medians = nn_medians[1]
            drakonian_medians = nn_medians[2]
            ax.barh(y - 1, charlen_weights, align='center', color='black', label="Charlen")
            ax.barh(y, gritis_medians, align='center', color='red', label="Gritis")
            ax.barh(y + 1, drakonian_medians, align='center', color='blue', label="Drakonian")
            ax.set_yticks(y)
            ax.set_yticklabels(nn_input)
            ax.invert_yaxis()
            plt.legend(loc='best')
            plt.show()
            if save_plot:
                plt.savefig('median_nn_weights.png')
            if pause_for_plot:
                input("\nPress ENTER to continue...")


class MassEffect:
    def infect(self, population, prob_illness, prob_infected_individuals, pause=True):
        if random.random() <= prob_illness:
            safe_population = []
            for creature in population:
                if prob_infected_individuals <= random.random():
                    safe_population.append(creature)

            if pause:
                print(f"\nINFECTED: {1 - len(safe_population) / len(population)}% died")
                input("\nPress ENTER to continue...")

            # So population safe population doesn't need to be defined outside condition
            population = safe_population

        return population

    def war(self, population, prob_war, weights, to_fight, pause=True):
        if random.random() <= prob_war:
            initial_pop_size = len(population)
            creature1 = random.randint(0, len(population) - 1)
            creature2 = random.randint(0, len(population) - 1)
            for a in range(int((len(population) - 1) * to_fight), 0, -1):
                if creature1 >= len(population):
                    creature1 = random.randint(0, len(population) - 1)
                if creature2 >= len(population):
                    creature2 = random.randint(0, len(population) - 1)

                creature1_fitness = calc_fitness([population[creature1]], weights)[0]
                creature2_fitness = calc_fitness([population[creature2]], weights)[0]
                boost1 = random.randint(1, 5) * .1
                boost2 = random.randint(1, 5) * .1
                creature1_fitness = creature1_fitness + (
                            creature1_fitness * boost1) if random.random() <= .5 else creature1_fitness - (
                            creature1_fitness * boost1)
                creature2_fitness = creature2_fitness + (
                            creature2_fitness * boost2) if random.random() <= .5 else creature2_fitness - (
                            creature2_fitness * boost2)

                if creature1_fitness < creature2_fitness:
                    del population[creature1]
                    creature1 = random.randint(0, len(population) - 1)
                elif creature1_fitness >= creature2_fitness:
                    del population[creature2]
                    creature2 = random.randint(0, len(population) - 1)

                if random.random() <= prob_change_fighters:
                    creature1 = random.randint(0, len(population) - 1)
                    creature2 = random.randint(0, len(population) - 1)

            print(f"\nWORLD WAR: {(1 - len(population) / initial_pop_size) * 100:.2f}% died")
            if pause:
                input("\nPress ENTER to continue...")

        return population

    def species_war(self, population, prob_species_war, weights, to_fight, pause=True):
        if random.random() <= prob_species_war:
            # Method to get specie index that is not similar to the other creature fighting and its creature index
            def select_creature(other_specie_index):
                specie_index = random.randint(0, len(species_fighting) - 1)
                while specie_index == other_specie_index:
                    specie_index = random.randint(0, len(species_fighting) - 1)
                index = random.randint(0, len(species_war[specie_index]) - 1)

                return specie_index, index,

            # Select names of species that will fight
            r = random.randint(2, len(species))
            possible_fighting = []
            for specie in species:
                possible_fighting.append(specie)
            species_fighting = [possible_fighting.pop(random.randint(0, len(possible_fighting) - 1)) for i in range(r)]

            # Collect initial counts for each species and categorize species from population
            initial_counts = []
            species_war = []
            for specie_fighting in species_fighting:
                fighting = []
                for i in range(len(population) - 1, 0, -1):
                    if population[i][0][1] == specie_fighting:
                        fighting.append(population.pop(i))
                initial_counts.append(len(fighting))
                species_war.append(fighting)

            # Check to see of their are enough creatures in each species fighting, to fight
            if initial_counts.count(0) > 0:
                if initial_counts.count(0) > len(species_fighting) - 2:
                    species_war = []
                    for specie_fighting in species_war:
                        species_war += specie_fighting
                    np.random.shuffle(species_war)

                    return species_war + population
                else:
                    for index in range(len(initial_counts) - 1, 0, -1):
                        if initial_counts[index] == 0:
                            del species_war[index]
                            del initial_counts[index]
                            del species_fighting[index]

            # The actual fight
            specie1 = random.randint(0, len(species_fighting) - 1)
            index1 = random.randint(0, len(species_war[specie1]) - 1)
            specie2, index2 = select_creature(specie1)
            # smallest_specie_size = min([len(specie) for specie in species_war])
            smallest_specie_size = len(min(species_war, key=len))
            for a in range(int((smallest_specie_size - 1) * to_fight), 0, -1):
                if len(min(species_war, key=len)) == 0:
                    break
                if index1 >= len(species_war[specie1]):
                    specie1, index1 = select_creature(specie2)
                if index2 >= len(species_war[specie2]):
                    specie2, index2 = select_creature(specie1)

                # Calculate fitness. Here we +- 10-50% power of creature to make it intereseting
                creature1_fitness = calc_fitness([species_war[specie1][index1]], weights)[0]
                creature2_fitness = calc_fitness([species_war[specie2][index2]], weights)[0]
                boost1 = random.randint(1, 5) * .1
                boost2 = random.randint(1, 5) * .1
                creature1_fitness = creature1_fitness + (
                            creature1_fitness * boost1) if random.random() <= .5 else creature1_fitness - (
                            creature1_fitness * boost1)
                creature2_fitness = creature2_fitness + (
                            creature2_fitness * boost2) if random.random() <= .5 else creature2_fitness - (
                            creature2_fitness * boost2)

                # The actual actual fight
                if creature1_fitness < creature2_fitness:
                    del species_war[specie1][index1]
                    specie1, creature1 = select_creature(specie2)
                elif creature1_fitness > creature2_fitness:
                    del species_war[specie2][index2]
                    specie2, creature2 = select_creature(specie1)

                if random.random() <= prob_change_fighters:
                    specie1, creature1 = select_creature(specie2)
                    specie2, creature2 = select_creature(specie1)

            # Combine the separated species
            whos_fighting = []
            for specie_fighting in species_war:
                whos_fighting += specie_fighting
            np.random.shuffle(whos_fighting)

            # Final creature count for each species that found to count for casualties
            final_counts = []
            for specie_fighting in species_fighting:
                count = 0
                for i in range(len(whos_fighting) - 1):
                    if whos_fighting[i][0][1] == specie_fighting:
                        count += 1
                final_counts.append(count)

            print(f"\nSPECIES WAR BETWEEN {species_fighting}: ", end="")
            for specie in range(len(species_war)):
                print(
                    f"{(1 - final_counts[specie] / initial_counts[specie]) * 100:.2f}% of {species_fighting[specie]} died",
                    end="   ")
            if pause:
                input("\n\nPress ENTER to continue...")

            # So population safe population doesn't need to be defined outside condition
            population += whos_fighting

        return population

    def civil_war(self, population, prob_civil_war, weights, to_fight, pause=True):
        if random.random() <= prob_civil_war:
            # Select names of species that will fight
            specie_fighting = species[random.randint(0, len(species) - 1)]

            # Collect initial counts for each species and categorize specie from population
            fighting = []
            for i in range(len(population) - 1, 0, -1):
                if population[i][0][1] == specie_fighting:
                    fighting.append(population.pop(i))
            initial_count = len(fighting)

            # Check to see of their are enough creatures in the species to fight
            if initial_count < 2:
                population += fighting

                return population

            creature1 = random.randint(0, len(fighting) - 1)
            creature2 = random.randint(0, len(fighting) - 1)
            for a in range(int((len(fighting) - 1) * to_fight), 0, -1):
                if creature1 >= len(fighting):
                    creature1 = random.randint(0, len(fighting) - 1)
                if creature2 >= len(fighting):
                    creature2 = random.randint(0, len(fighting) - 1)

                creature1_fitness = calc_fitness([fighting[creature1]], weights)[0]
                creature2_fitness = calc_fitness([fighting[creature2]], weights)[0]
                boost1 = random.randint(1, 5) * .1
                boost2 = random.randint(1, 5) * .1
                creature1_fitness = creature1_fitness + (
                            creature1_fitness * boost1) if random.random() <= .5 else creature1_fitness - (
                            creature1_fitness * boost1)
                creature2_fitness = creature2_fitness + (
                            creature2_fitness * boost2) if random.random() <= .5 else creature2_fitness - (
                            creature2_fitness * boost2)

                if creature1_fitness < creature2_fitness:
                    del fighting[creature1]
                    creature1 = random.randint(0, len(fighting) - 1)
                elif creature1_fitness >= creature2_fitness:
                    del fighting[creature2]
                    creature2 = random.randint(0, len(fighting) - 1)

                if random.random() <= prob_change_fighters:
                    creature1 = random.randint(0, len(fighting) - 1)
                    creature2 = random.randint(0, len(fighting) - 1)

            population += fighting
            np.random.shuffle(population)

            print(f"\n{specie_fighting} CIVIL WAR: ", end="")
            print(f"{(1 - len(fighting) / initial_count) * 100:.2f}% of {specie_fighting} died", end="   ")
            if pause:
                input("\n\nPress ENTER to continue...")

        return population


class Creatures:
    def generate_charlen(self):
        charlen = [('Species', 'Charlen')]
        mu, sigma = 67, 3  # Height
        charlen.append(('Height', round(np.random.normal(mu, sigma), 3)))
        mu, sigma = 150, 15  # Weight
        charlen.append(('Weight', round(np.random.normal(mu, sigma), 3)))
        mu, sigma = 40, 15  # Speed
        charlen.append(('Speed', round(np.random.normal(mu, sigma), 3)))
        mu, sigma = 40, 15  # Power
        charlen.append(('Power', round(np.random.normal(mu, sigma), 3)))
        charlen.append(('Neural Net W1', 2 * np.random.random(nn_weights1_len) - 1))  # Weights for Neural Network
        charlen.append(('Neural Net W2', 2 * np.random.random(nn_weights2_len) - 1))  # Weights for Neural Network

        return charlen

    def generate_gritis(self):
        gritis = [('Species', 'Gritis')]
        mu, sigma = 96, 5  # Height
        gritis.append(('Height', round(np.random.normal(mu, sigma), 3)))
        mu, sigma = 200, 20  # Weight
        gritis.append(('Weight', round(np.random.normal(mu, sigma), 3)))
        mu, sigma = 40, 15  # Speed
        gritis.append(('Speed', round(np.random.normal(mu, sigma), 3)))
        mu, sigma = 20, 11  # Power
        gritis.append(('Power', round(np.random.normal(mu, sigma), 3)))
        gritis.append(('Neural Net W1', 2 * np.random.random(nn_weights1_len) - 1))  # Weights for Neural Network
        gritis.append(('Neural Net W2', 2 * np.random.random(nn_weights2_len) - 1))  # Weights for Neural Network

        return gritis

    def generate_drakonian(self):
        drakonian = [('Species', 'Drakonian')]
        mu, sigma = 52, 5  # Height
        drakonian.append(('Height', round(np.random.normal(mu, sigma), 3)))
        mu, sigma = 120, 12  # Weight
        drakonian.append(('Weight', round(np.random.normal(mu, sigma), 3)))
        mu, sigma = 80, 15  # Speed
        drakonian.append(('Speed', round(np.random.normal(mu, sigma), 3)))
        mu, sigma = 50, 10  # Power
        drakonian.append(('Power', round(np.random.normal(mu, sigma), 3)))
        drakonian.append(('Neural Net W1', 2 * np.random.random(nn_weights1_len) - 1))  # Weights for Neural Network
        drakonian.append(('Neural Net W2', 2 * np.random.random(nn_weights2_len) - 1))  # Weights for Neural Network

        return drakonian


class Utils:
    def create_weights(self):
        return [random.random() if random.randint(0, 1) == 0 else -random.random() for i in range(4)]

    def check_pulse(self, population):
        if len(population) <= 1:
            print("\n\nAll Species Extinct... This is what happens when you play god")
            print("\n" + "=" * 42)
            sys.exit()

    def count_creatures(self, population):
        charlen_count = 0
        gritis_count = 0
        drakonian_count = 0
        for creature in population:
            try:
                if creature[0][1] == species[0]:
                    charlen_count += 1
                elif creature[0][1] == species[1]:
                    gritis_count += 1
                else:
                    drakonian_count += 1
            except:
                pass

        return charlen_count, gritis_count, drakonian_count

    def get_middle(self, input_list):
        if input_list:
            middle = float(len(input_list)) / 2
            if middle % 2 != 0:
                return input_list[int(middle - .5)]
            else:
                try:
                    return (input_list[int(middle)] + input_list[int(middle - 1)]) / 2
                except:
                    return input_list[int(middle - .5)]

        else:
            return np.nan

    def get_medians(self, population):
        # Separate creatures by species
        charlens = []
        gritiss = []
        drakonians = []
        for creature in population:
            if creature[0][1] == species[0]:
                charlens.append(creature)
            elif creature[0][1] == species[1]:
                gritiss.append(creature)
            else:
                drakonians.append(creature)

        # Calculate medians for all traits
        charlen_median_traits = []
        for i in range(len(trait_list)):
            trait = []
            for charlen in charlens:
                trait.append(charlen[i + 1][1])
            charlen_median_traits.append(self.get_middle(trait))

        gritis_median_traits = []
        for i in range(len(trait_list)):
            trait = []
            for gritis in gritiss:
                trait.append(gritis[i + 1][1])
            gritis_median_traits.append(self.get_middle(trait))

        drakonian_median_traits = []
        for i in range(len(trait_list)):
            trait = []
            for drakonian in drakonians:
                trait.append(drakonian[i + 1][1])
            drakonian_median_traits.append(self.get_middle(trait))

        return [charlen_median_traits, gritis_median_traits, drakonian_median_traits]

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-round(x, 15)))

    def dot(self, inp, weights):
        nodes = []
        for num in inp:
            node = 0
            for weight in weights:
                node += num * weight
            nodes.append(self.sigmoid(node))

        return nodes

    def get_median_nn_stats(self, population):
        charlen_median_traits, gritis_median_traits, drakonian_median_traits = self.get_medians(population)

        # Combine species into on array
        final = [["Charlen"] + charlen_median_traits]
        final.append(["Gritis"] + gritis_median_traits)
        final.append(["Drakonian"] + drakonian_median_traits)

        charlen_median_nn_stats = []
        gritis_median_nn_stats = []
        drakonian_median_nn_stats = []
        # Use spaces because of difference in use from pycharm to pythonista
        for col in range(nn_weights1_len):
            for row in range(len(species)):
                try:
                    weight = round(float(final[row][5][col]), 4)
                except:
                    weight = np.nan
                if row == 0:
                    charlen_median_nn_stats.append(weight)
                if row == 1:
                    gritis_median_nn_stats.append(weight)
                if row == 2:
                    drakonian_median_nn_stats.append(weight)

        return charlen_median_nn_stats, gritis_median_nn_stats, drakonian_median_nn_stats


def generate_population(num_of_creatures):
    creatures = Creatures()
    pop_creatures = []
    for i in range(num_of_creatures[0]):
        pop_creatures.append(creatures.generate_charlen())
    for i in range(num_of_creatures[1]):
        pop_creatures.append(creatures.generate_gritis())
    for i in range(num_of_creatures[2]):
        pop_creatures.append(creatures.generate_drakonian())
    np.random.shuffle(pop_creatures)

    return pop_creatures


def calc_fitness(population, weights):
    fitness_scores = []
    for creature in population:
        fitness = 0
        for index in range(len(weights)):
            fitness += creature[index + 1][1] * weights[index]
        fitness_scores.append(round(fitness, 3))

    return fitness_scores


def select_fittest(population, fitness_scores):
    charlens = []
    charlen_count = 0
    gritiss = []
    gritis_count = 0
    drakonians = []
    drakonian_count = 0
    index = 0
    charlen_index = 0
    gritis_index = 0
    drakonian_index = 0
    for creature in population:
        if creature[0][1] == species[0]:
            charlens.append(creature)
            charlen_count += 1
            if charlen_count == 1:
                charlen_index = index
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

    if charlen_count == 1:
        del population[charlen_index]
        del fitness_scores[charlen_index]
    if gritis_count == 1:
        del population[gritis_index]
        del fitness_scores[gritis_index]
    if drakonian_count == 1:
        del population[drakonian_index]
        del fitness_scores[drakonian_index]

    # Momentarily give each creature health and resources
    for creature, creature_fitness in zip(population, fitness_scores):
        creature.append(abs(creature_fitness * .5))  # Health
        creature.append(random.randint(0, 100))  # Resources

    fighting_count = 0
    want_2_fight_avg = 0
    n = len(population)
    for count in range(len(population)):
        creature_index = random.randint(0, len(population) - 1)
        creature = population[creature_index]
        creature_specie = creature[0][1]
        creature_fitness = fitness_scores[creature_index] if fitness_scores[creature_index] > 10 else 10
        creature_resources = creature[len(creature) - 1]
        creature_health = creature[len(creature) - 2]
        creature_nn_weights1 = creature[5][1]
        creature_nn_weights2 = creature[6][1]

        # Make sure creature is not fighting itself
        competitor_index = creature_index
        while competitor_index == creature_index:
            competitor_index = random.randint(0, len(population) - 1)
        assert competitor_index != creature_index

        competitor = population[competitor_index]
        competitor_specie = competitor[0][1]
        competitor_fitness = fitness_scores[competitor_index] if fitness_scores[competitor_index] > 10 else 10
        competitor_resources = competitor[len(competitor) - 1]
        competitor_health = competitor[len(competitor) - 2]
        competitor_nn_weights1 = competitor[5][1]
        competitor_nn_weights2 = competitor[6][1]

        resource_reward = random.randint(10, 40)

        # Think
        utils = Utils()
        creature_want = utils.dot([creature_fitness,
                                competitor_fitness,
                                creature_health,
                                competitor_health,
                                resource_reward,
                                competitor_resources], creature_nn_weights1)
        creature_want = utils.sigmoid(np.dot(creature_want, creature_nn_weights2))

        competitor_want = utils.dot([competitor_fitness,
                                creature_fitness,
                                competitor_health,
                                creature_health,
                                resource_reward,
                                creature_resources], competitor_nn_weights1)
        competitor_want = utils.sigmoid(np.dot(competitor_want, competitor_nn_weights2))

        want_2_fight_avg += (creature_want + competitor_want)/2
        if creature_want >= .5 and competitor_want >= .5:
            fighting_count += 1
            # Resources help give health a boost and fitness a boost as well
            creature_health += creature_resources * random.randint(1, 4) * .1
            creature_fitness += creature_resources * random.randint(1, 4) * .1
            competitor_health += competitor_resources * random.randint(1, 4) * .1
            competitor_fitness += competitor_resources * random.randint(1, 4) * .1

            if creature_fitness > competitor_fitness:
                competitor_health -= abs(creature_fitness * damage_damper)
                competitor_lost_resources = competitor_resources * .75
                competitor_resources -= competitor_lost_resources

                creature_resources += resource_reward + competitor_lost_resources
                creature[len(creature) - 1] = creature_resources
                population[creature_index] = creature

                if competitor_health <= 0:
                    del population[competitor_index]
                else:
                    competitor[len(competitor) - 1] = competitor_resources
                    competitor[len(competitor) - 2] = competitor_health
                    population[competitor_index] = competitor

            elif creature_fitness < competitor_fitness:
                creature_health -= abs(competitor_fitness * damage_damper)
                creature_lost_resources = creature_resources * .75
                creature_resources -= creature_lost_resources

                competitor_resources += resource_reward + creature_lost_resources
                competitor[len(competitor) - 1] = competitor_resources
                population[competitor_index] = competitor

                if creature_health <= 0:
                    del population[creature_index]
                else:
                    creature[len(creature) - 1] = creature_resources
                    creature[len(creature) - 2] = creature_health
                    population[creature_index] = creature

            else:
                competitor_health -= abs(creature_fitness * damage_damper)
                if competitor_health <= 0:
                    del population[competitor_index]
                else:
                    competitor[len(competitor) - 2] = competitor_health
                    population[competitor_index] = competitor

                creature_health -= abs(competitor_fitness * damage_damper)
                if creature_health <= 0:
                    del population[creature_index]
                else:
                    creature[len(creature) - 2] = creature_health
                    population[creature_index] = creature

        elif creature_specie == competitor_specie:
            creature[len(creature) - 1] = creature_resources + (resource_reward * .5)
            population[creature_index] = creature
            competitor[len(competitor) - 1] = competitor_resources + (resource_reward * .5)
            population[competitor_index] = competitor

    print(f"Number of Fights:", fighting_count)
    print("Creatures want to fight avg: ", want_2_fight_avg/n)

    # Remove temporary health and resources
    for creature in population:
        creature.pop(len(creature) - 1)
        creature.pop(len(creature) - 1)
    return population


def crossover(population):
    for creature in range(len(population) - 1):
        to_breed_with = random.randint(0, len(population) - 1)
        if random.random() <= prob_crossover and population[creature][0][1] == population[to_breed_with][0][1]:
            for i in range(1, max_num_kids + 1):
                prob_of_next_child = kids_after_start_prob / i
                if prob_of_next_child <= random.random() or i == 1:
                    parent1 = population[creature]
                    parent2 = population[to_breed_with]
                    p1_nn_weights1 = parent1[5][1]
                    p1_nn_weights2 = parent1[6][1]
                    p2_nn_weights1 = parent2[5][1]
                    p2_nn_weights2 = parent2[6][1]
                    r1 = random.randint(0, len(p1_nn_weights1))
                    r2 = random.randint(0, len(p1_nn_weights2))
                    parent1[5] = (parent1[5][0], np.concatenate((p1_nn_weights1[:r1], p2_nn_weights1[r1:]), axis=0))
                    parent1[6] = (parent1[6][0], np.concatenate((p1_nn_weights2[:r2], p2_nn_weights2[r2:]), axis=0))
                    parent2[5] = (parent2[5][0], np.concatenate((p2_nn_weights1[:r1], p1_nn_weights1[r1:]), axis=0))
                    parent2[6] = (parent2[6][0], np.concatenate((p2_nn_weights2[:r2], p1_nn_weights2[r2:]), axis=0))
                    r3 = random.randint(1, num_of_traits)
                    if random.random() <= .5:
                        population.insert(random.randint(0, len(population) - 1), parent1[:r3] + parent2[r3:])
                    else:
                        population.insert(random.randint(0, len(population) - 1), parent2[:r3] + parent1[r3:])
                else:
                    break
    return population


def mutation(population):
    for i in range(int((len(population) - 1))):
        if random.random() <= prob_mutation:
            creature = population[i]
            for a in range(random.randint(0, num_of_traits - 2)):  # -1 species -1 IndexOutOfBounds
                index = random.randint(1, num_of_traits)
                if creature[index][0] == "Neural Net W1" or creature[index][0] == "Neural Net W2":
                    trait = creature[index][1]
                    for weight in range(len(trait)):
                        if random.random() <= .7:
                            trait[weight] *= random.randint(5000, 15000)/10000
                    creature[index] = (creature[index][0], trait)
                else:
                    trait = old_trait = creature[index][1]
                    if random.random() <= .5:
                        trait = round(trait + (trait * mutation_rate), 3)
                    else:
                        trait = round(trait - (trait * mutation_rate), 3)
                    creature[index] = (creature[index][0], trait) if trait > 1 else (creature[index][0], old_trait)
            population[i] = creature

    return population


def breed(population):
    return mutation(crossover(population))


def evolve(population, weights):
    fitness_scores = calc_fitness(population, weights)
    return breed(select_fittest(population, fitness_scores))
