import sys
import random
import matplotlib.pyplot as plt
import numpy as np
if sys.platform != "ios":
    import psutil

species = [
    "Charlen",
    "Gritis",
    "Drakonian"
]
trait_list = [
    'Age',
    'Gen.',
    'Health',
    'Resources',
    'Height',
    'Weight',
    'Speed',
    'Power',
    'Neural Net W1',
    'Neural Net W2'
]
nn_input = [
    "my fitness",
    "c2 fitness",
    "my health",
    "c2 health",
    "resource reward",
    "my resources",
    "c2 resources"
]

world_resources = 1000
prob_crossover = .5
prob_mutation = .75
mutation_rate = .001
num_of_traits = len(trait_list)
nn_weights1_len = len(nn_input)
nn_weights2_len = 3
resource_reward_min, resource_reward_max = 20, 50
resource_health_boost_min, resource_health_boost_max = 1, 3
resource_fitness_boost_min, resource_fitness_boost_max = 1, 3
per_lost_resources = .8
damage_multiplier = .9
health_multiplier = .5
age_penalty_multiplier = .2
energy_retention = .9
prob_change_fighters = 0.2
charlen_maturity_age = 18
gritis_maturity_age = 25
drakonian_maturity_age = 13


class Stats:
    def weights_summary(self, weights, pause=True):
        print(f"Environmental Factors: ", end="")
        for i in range(len(weights)):
            if i == len(trait_list) - 1:
                print(f"{trait_list[i + 3]}: {weights[i]:.2f}")
            else:
                print(f"{trait_list[i + 3]}: {weights[i]:.2f} : ", end="")
        if pause:
            input("\nPress ENTER to continue...\n")

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
                'Age',
                'Gen.',
                'Health',
                'Resources',
                'Feet',
                'lbs',
                'Speed',
                'Power',
            ]

            # Find largest string length between extinct, trait length, and species name length
            max_trait_str_len = max(len("Extinct"), len(max(species, key=len)))
            for creature in final:
                for trait in range(3, len(creature) - 2):
                    competitor = len(str(round(creature[trait], 2)))
                    if competitor > max_trait_str_len:
                        max_trait_str_len = competitor

            # Find max trait name length
            max_trait_name_len = len(max(updated_trait_list, key=len))

            # Print out medians traits for all species
            print(" " * (8 + max_trait_str_len) + "Medians")
            for trait in range(len(updated_trait_list)):
                if trait != 0:
                    print()
                print(updated_trait_list[trait] + " " * (max_trait_name_len - len(updated_trait_list[trait])), end=" ")
                for creature in final:
                    if updated_trait_list[trait] == "Species":
                        print(creature[trait], end=" " * (max_trait_str_len - len(creature[trait])))
                    elif updated_trait_list[trait] == "Fitness":
                        if np.isnan(creature[trait]):
                            print("Extinct", end=" " * (max_trait_str_len - len(str("Extinct"))))
                        else:
                            rounded_score = round(creature[trait], 2)
                            print(rounded_score, end=" " * (max_trait_str_len - len(str(rounded_score))))
                    elif np.isnan(creature[trait]):
                        if updated_trait_list[trait] == "Feet":
                            print("Nan", end=" " * (max_trait_str_len - len(str("Nan"))))
                        else:
                            print("Nan", end=" " * (max_trait_str_len - len(str("Nan"))))
                    else:
                        if updated_trait_list[trait] == "Feet":
                            feet = int(creature[trait] / 12)
                            inches = int(creature[trait]) % 12
                            height = f"{feet}'{inches}\""
                            print(height, end=" " * (max_trait_str_len - len(str(height))))
                        else:
                            trait_rounded = round(creature[trait], 2)
                            print(trait_rounded, end=" " * (max_trait_str_len - len(str(trait_rounded))))

            # Use spaces because of difference in use from pycharm to pythonista IDEs
            print("\n\n", " " * 9, "Neural Network Medians")
            # print("  Input Names", " " * 11, "Weights")
            print(" " * 19, "C.      G.      D.")
            print(" " * 16, "W1")
            for col in range(nn_weights1_len):
                input_name = nn_input[col]
                print(input_name, end=" " * ((len("resource reward") + 2) - len(input_name)))
                for row in range(len(species)):
                    try:
                        weight = round(float(final[row][len(final[row]) - 2][col]), 4)
                    except:
                        weight = np.nan
                    print(weight, end=" " * (8 - len(str(weight))))
                print()
            print(" " * 16, "W2")
            for col in range(nn_weights2_len):
                print(" " * (len("resource reward") + 2), end="")
                for row in range(len(species)):
                    try:
                        weight = round(float(final[row][len(final[row]) - 1][col]), 4)
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
            print(f"Year {generation} |")
            print(f"\t{charlen_count:,} Charlen") if isinstance(charlen_count, int) else print(f"\tCharlen {charlen_count}")
            print(f"\t{gritis_count:,} Gritis") if isinstance(gritis_count, int) else print(f"\tGritis {gritis_count}")
            print(f"\t{drakonian_count:,} Drakonian") if isinstance(drakonian_count, int) else print(
                f"\tDrakonian {drakonian_count}")
            print(f"\t{len(population):,} total creatures")

    def show_nn_bar_graph(self, nn_medians, generation, save_plot=True, print_plots_every=500, pause_for_plot=True):
        if generation % print_plots_every == 0 and generation != 0:
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
            plt.tight_layout()
            plt.show()
            if save_plot:
                plt.savefig('median_nn_weights.png')
            if pause_for_plot:
                input("\nPress ENTER to continue...\n")


class MassEffect:
    def infect(self, population, prob_illness, prob_infected_individuals, pause=True):
        if random.random() <= prob_illness:
            safe_population = []
            for creature in population:
                if prob_infected_individuals <= random.random():
                    safe_population.append(creature)

            if pause:
                print(f"\nINFECTED: {1 - len(safe_population) / len(population)}% died")
                input("\nPress ENTER to continue...\n")

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
                input("\nPress ENTER to continue...\n")

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
    def generate_charlen(self, weights):
        charlen = [('Species', 'Charlen')]
        charlen.append(('Age', charlen_maturity_age))  # Age
        charlen.append(('Gen.', 0))  # Generation
        charlen.append(('Resources', random.randint(10, 60)))  # Resources
        mu, sigma = 67, 3  # Height
        charlen.append(('Height', round(np.random.normal(mu, sigma), 3)))
        mu, sigma = 150, 15  # Weight
        charlen.append(('Weight', round(np.random.normal(mu, sigma), 3)))
        mu, sigma = 40, 15  # Speed
        charlen.append(('Speed', round(np.random.normal(mu, sigma), 3)))
        mu, sigma = 40, 15  # Power
        charlen.append(('Power', round(np.random.normal(mu, sigma), 3)))
        mu, sigma = calc_fitness([charlen], weights)[0], 20  # Calculate fitness to calculate health
        charlen.insert(3, ('Health', round(np.random.normal(mu, sigma), 3)))
        charlen.append(('Neural Net W1', np.round(2 * np.random.random(nn_weights1_len) - 1, 8)))  # Weights for Neural Network
        charlen.append(('Neural Net W2', np.round(2 * np.random.random(nn_weights2_len) - 1, 8)))  # Weights for Neural Network

        return charlen

    def generate_gritis(self, weights):
        gritis = [('Species', 'Gritis')]
        gritis.append(('Age', gritis_maturity_age))  # Age
        gritis.append(('Gen.', 0))  # Generation
        gritis.append(('Resources', random.randint(10, 60)))  # Resources
        mu, sigma = 96, 5  # Height
        gritis.append(('Height', round(np.random.normal(mu, sigma), 3)))
        mu, sigma = 200, 20  # Weight
        gritis.append(('Weight', round(np.random.normal(mu, sigma), 3)))
        mu, sigma = 40, 15  # Speed
        gritis.append(('Speed', round(np.random.normal(mu, sigma), 3)))
        mu, sigma = 20, 11  # Power
        gritis.append(('Power', round(np.random.normal(mu, sigma), 3)))
        mu, sigma = calc_fitness([gritis], weights)[0], 20  # Calculate fitness to calculate health
        gritis.insert(3, ('Health', round(np.random.normal(mu, sigma), 3)))
        gritis.append(('Neural Net W1', np.round(2 * np.random.random(nn_weights1_len) - 1, 8)))  # Weights for Neural Network
        gritis.append(('Neural Net W2', np.round(2 * np.random.random(nn_weights2_len) - 1, 8)))  # Weights for Neural Network

        return gritis

    def generate_drakonian(self, weights):
        drakonian = [('Species', 'Drakonian')]
        drakonian.append(('Age', drakonian_maturity_age))  # Age
        drakonian.append(('Gen.', 0))  # Generation
        drakonian.append(('Resources', random.randint(10, 60)))  # Resources
        mu, sigma = 52, 5  # Height
        drakonian.append(('Height', round(np.random.normal(mu, sigma), 3)))
        mu, sigma = 120, 12  # Weight
        drakonian.append(('Weight', round(np.random.normal(mu, sigma), 3)))
        mu, sigma = 80, 15  # Speed
        drakonian.append(('Speed', round(np.random.normal(mu, sigma), 3)))
        mu, sigma = 50, 10  # Power
        drakonian.append(('Power', round(np.random.normal(mu, sigma), 3)))
        mu, sigma = calc_fitness([drakonian], weights)[0], 20  # Calculate fitness to calculate health
        drakonian.insert(3, ('Health', round(np.random.normal(mu, sigma), 3)))
        drakonian.append(('Neural Net W1', np.round(2 * np.random.random(nn_weights1_len) - 1, 8)))  # Weights for Neural Network
        drakonian.append(('Neural Net W2', np.round(2 * np.random.random(nn_weights2_len) - 1, 8)))  # Weights for Neural Network

        return drakonian


class Utils:
    def create_weights(self):
        return [random.random() * .5 for i in range(4)]

    def check_pulse(self, population):
        if len(population) <= 1:
            print("\n\nAll Species Extinct... This is what \nhappens when you play god")
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
        np.sort(input_list)
        if input_list:
            middle = float(len(input_list)) / 2
            return input_list[int(middle - .5)]
            # if middle % 2 != 0:
            #     return input_list[int(middle - .5)]
            # else:
            #     try:
            #         return (input_list[int(middle)] + input_list[int(middle - 1)]) / 2
            #     except:
            #         return input_list[int(middle - .5)]

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

        # Calculate medians for all traits and do it separately to account for different size arrays
        charlen_median_traits = []
        for i in range(1, len(trait_list) + 1):
            trait = []
            for charlen in charlens:
                trait.append(charlen[i][1])
            charlen_median_traits.append(self.get_middle(trait))

        gritis_median_traits = []
        for i in range(1, len(trait_list) + 1):
            trait = []
            for gritis in gritiss:
                trait.append(gritis[i][1])
            gritis_median_traits.append(self.get_middle(trait))

        drakonian_median_traits = []
        for i in range(1, len(trait_list) + 1):
            trait = []
            for drakonian in drakonians:
                trait.append(drakonian[i][1])
            drakonian_median_traits.append(self.get_middle(trait))

        return [charlen_median_traits, gritis_median_traits, drakonian_median_traits]

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def softmax(self, x):
        e_x = np.exp(x - np.max(x))
        out = e_x / e_x.sum()
        return out

    def sigmoid_dot(self, inp, weights):
        return [self.sigmoid(sum([num * weight for num in inp])) for weight in weights]

    def softmax_dot(self, inp, weights):
        return [self.softmax(sum([num * weight for num in inp])) for weight in weights]

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
                # print(final[row])
                # print(final[row][len(final[row]) - 2])
                # print(final[row][len(final[row]) - 1])
                try:
                    # Change - 2 when adding more traits for some reason
                    weight = round(float(final[row][len(final[row]) - 2][col]), 4)
                except:
                    weight = np.nan
                if row == 0:
                    charlen_median_nn_stats.append(weight)
                if row == 1:
                    gritis_median_nn_stats.append(weight)
                if row == 2:
                    drakonian_median_nn_stats.append(weight)

        return charlen_median_nn_stats, gritis_median_nn_stats, drakonian_median_nn_stats

    def cpu_ram_usage(self, on_pc, py, year, print_every=1):
        if on_pc and year % print_every == 0:
            print(f"CPU USAGE: {psutil.cpu_percent()}% RAM USAGE: {round(py.memory_info()[0] / 2. ** 30, 3)}GB", end="")


def generate_population(num_of_creatures, weights):
    creatures = Creatures()
    pop_creatures = []
    for i in range(num_of_creatures[0]):
        pop_creatures.append(creatures.generate_charlen(weights))
    for i in range(num_of_creatures[1]):
        pop_creatures.append(creatures.generate_gritis(weights))
    for i in range(num_of_creatures[2]):
        pop_creatures.append(creatures.generate_drakonian(weights))
    np.random.shuffle(pop_creatures)

    return pop_creatures


def calc_fitness(population, weights):
    fitness_scores = []
    for creature in population:
        fitness = 0
        for index in range(len(weights)):
            # Change 4 when adjusting trait list
            fitness += creature[index + 4][1] * weights[index]
        fitness_scores.append(round(fitness, 3))

    # [round(sum([creature[index + 1][1] * weights[index] for index in range(len(weights))]), 3) for creature in population]
    return fitness_scores


def select_fittest(population, fitness_scores):
    # This is so the parameter can be controlled at the top
    wrld_resources = world_resources

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

    fighting_count = 0
    eat_count = 0
    for count in range(len(population)):
        # it is ok if not every creature participates so do not worry about it
        creature_index = random.randint(0, len(population) - 1)
        creature = population[creature_index]
        # creature_specie = creature[0][1]
        creature_fitness = fitness_scores[creature_index] if fitness_scores[creature_index] > 5 else 5
        creature_health = creature[3][1]
        creature_resources = creature[4][1]
        # Change these when adjusting traits for some reasons
        creature_nn_weights1 = creature[len(creature) - 2][1]
        creature_nn_weights2 = creature[len(creature) - 1][1]

        # Make sure creature is not fighting itself
        competitor_index = creature_index
        while competitor_index == creature_index:
            competitor_index = random.randint(0, len(population) - 1)
        assert competitor_index != creature_index
        competitor = population[competitor_index]
        # competitor_specie = competitor[0][1]
        competitor_fitness = fitness_scores[competitor_index] if fitness_scores[competitor_index] > 10 else 10
        competitor_health = competitor[3][1]
        competitor_resources = competitor[4][1]
        # Change these when adjusting traits for some reasons
        competitor_nn_weights1 = competitor[len(competitor) - 2][1]
        competitor_nn_weights2 = competitor[len(competitor) - 1][1]

        resource_reward = random.randint(resource_reward_min, resource_reward_max) if wrld_resources > 0 else 0
        wrld_resources -= resource_reward

        fight_categories = ["Passivity", "Fight", "Eat"]

        # Think, i.e. applying their neural network
        utils = Utils()
        hidden_layer_output = utils.sigmoid_dot([creature_fitness,
                                competitor_fitness,
                                creature_health,
                                competitor_health,
                                resource_reward,
                                creature_resources,
                                competitor_resources], creature_nn_weights1)
        output = utils.sigmoid_dot(hidden_layer_output, creature_nn_weights2)
        # Index 1 is yes to fight, index 0 is no to fight
        creature_wants = fight_categories[output.index(max(output))]

        hidden_layer_output = utils.sigmoid_dot([competitor_fitness,
                                creature_fitness,
                                competitor_health,
                                creature_health,
                                resource_reward,
                                competitor_resources,
                                creature_resources], competitor_nn_weights1)
        output = utils.sigmoid_dot(hidden_layer_output, competitor_nn_weights2)
        # Index 1 is yes to fight, index 0 is no to fight
        competitor_wants = fight_categories[output.index(max(output))]

        # print(creature_wants, competitor_wants)

        if creature_wants == "Eat" or competitor_wants == "Eat":
            eat_count += 1
            # Resources help give health a boost and fitness a boost as well
            creature_health += creature_resources * (
                    random.randint(resource_health_boost_min, resource_health_boost_max) * .01)
            creature_fitness += creature_resources * (
                    random.randint(resource_fitness_boost_min, resource_fitness_boost_max) * .01)
            competitor_health += competitor_resources * (
                    random.randint(resource_health_boost_min, resource_health_boost_max) * .01)
            competitor_fitness += competitor_resources * (
                    random.randint(resource_fitness_boost_min, resource_fitness_boost_max) * .01)

            if creature_fitness > competitor_fitness:
                # Since the competitor lost we remove health from the creature remove resources from them
                competitor_lost_resources = competitor_resources
                competitor_resources -= competitor_lost_resources

                creature_health -= abs(competitor_fitness * .1)
                creature_lost_resources = creature_resources * .1
                creature_resources -= creature_lost_resources

                # Now onto the original creature
                # They get the boost of both resources they were fighting for and the resources of the competitor
                # they vanquished to their resources
                creature_health += (resource_reward + competitor_lost_resources) * energy_retention
                creature[3] = ('Health', round(creature_health, 3))
                creature_resources += (resource_reward + competitor_lost_resources) * energy_retention
                creature[4] = ('Resources', round(creature_resources, 3))
                population[creature_index] = creature

                # Competitor eaten
                del population[competitor_index]

            elif creature_fitness < competitor_fitness:
                # Since the original creature lost we remove health from the creature remove resources from them
                creature_lost_resources = creature_resources
                creature_resources -= creature_lost_resources

                competitor_health -= abs(creature_fitness * .1)
                competitor_lost_resources = competitor_resources * .1
                competitor_resources -= competitor_lost_resources

                # Now onto the original creature
                # They get the boost of both resources they were fighting for and the resources of the competitor
                # they vanquished to their resources
                competitor_health += (resource_reward + creature_lost_resources) * energy_retention
                competitor[3] = ('Health', round(competitor_health, 3))
                competitor_resources += (resource_reward + creature_lost_resources) * energy_retention
                competitor[4] = ('Resources', round(competitor_resources, 3))
                population[competitor_index] = competitor

                # Creature eaten
                del population[creature_index]

            else:
                # If they tied then they both lose health and resources and both may die
                creature_health -= abs(competitor_fitness * damage_multiplier)
                creature_lost_resources = creature_resources * per_lost_resources
                creature_resources -= creature_lost_resources
                if creature_health <= 0:
                    del population[creature_index]
                else:
                    creature[3] = ('Health', round(creature_health, 3))
                    creature[4] = ('Resources', round(creature_resources, 3))
                    population[creature_index] = creature

                competitor_health -= abs(creature_fitness * damage_multiplier)
                competitor_lost_resources = competitor_resources * per_lost_resources
                competitor_resources -= competitor_lost_resources
                if competitor_health <= 0:
                    del population[competitor_index]
                else:
                    competitor[3] = ('Health', round(competitor_health, 3))
                    competitor[4] = ('Resources', round(competitor_resources, 3))
                    population[competitor_index] = competitor

        elif creature_wants == "Fight" and competitor_wants == "Fight":
            fighting_count += 1
            # Resources help give health a boost and fitness a boost as well
            creature_health += creature_resources * (
                        random.randint(resource_health_boost_min, resource_health_boost_max) * .01)
            creature_fitness += creature_resources * (
                        random.randint(resource_fitness_boost_min, resource_fitness_boost_max) * .01)
            competitor_health += competitor_resources * (
                        random.randint(resource_health_boost_min, resource_health_boost_max) * .01)
            competitor_fitness += competitor_resources * (
                        random.randint(resource_fitness_boost_min, resource_fitness_boost_max) * .01)

            if creature_fitness > competitor_fitness:
                # Since the competitor lost we remove health from the creature remove resources from them
                competitor_health -= abs(creature_fitness * damage_multiplier)
                competitor_lost_resources = competitor_resources * per_lost_resources
                competitor_resources -= competitor_lost_resources

                creature_health -= abs(competitor_fitness * .1)
                creature_lost_resources = creature_resources * .1
                creature_resources -= creature_lost_resources

                # Now onto the original creature
                # They get the boost of both resources they were fighting for and the resources of the competitor
                # they vanquished to their resources
                creature_health += (resource_reward + competitor_lost_resources) * health_multiplier
                creature[3] = ('Health', round(creature_health, 3))
                creature_resources += (resource_reward + competitor_lost_resources)
                creature[4] = ('Resources', round(creature_resources, 3))
                population[creature_index] = creature

                if competitor_health <= 0:
                    # If the creatures health falls below zero we remove them, i.e. they die
                    del population[competitor_index]
                else:
                    # Here we finalize the results and return the creatures back to the population
                    competitor[3] = ('Health', round(competitor_health, 3))
                    competitor[4] = ('Resources', round(competitor_resources, 3))
                    population[competitor_index] = competitor

            elif creature_fitness < competitor_fitness:
                # Since the original creature lost we remove health from the creature remove resources from them
                creature_health -= abs(competitor_fitness * damage_multiplier)
                creature_lost_resources = creature_resources * per_lost_resources
                creature_resources -= creature_lost_resources

                competitor_health -= abs(creature_fitness * .1)
                competitor_lost_resources = competitor_resources * .1
                competitor_resources -= competitor_lost_resources

                # Now onto the original creature
                # They get the boost of both resources they were fighting for and the resources of the competitor
                # they vanquished to their resources
                competitor_health += (resource_reward + creature_lost_resources) * health_multiplier
                competitor[3] = ('Health', round(competitor_health, 3))
                competitor_resources += (resource_reward + creature_lost_resources)
                competitor[4] = ('Resources', round(competitor_resources, 3))
                population[competitor_index] = competitor

                if creature_health <= 0:
                    # If the creatures health falls below zero we remove them, i.e. they die
                    del population[creature_index]
                else:
                    # Here we finalize the results and return the creatures back to the population
                    creature[3] = ('Health', round(creature_health, 3))
                    creature[4] = ('Resources', round(creature_resources, 3))
                    population[creature_index] = creature

            else:
                # If they tied then they both lose health and resources and both may die
                creature_health -= abs(competitor_fitness * damage_multiplier)
                creature_lost_resources = creature_resources * per_lost_resources
                creature_resources -= creature_lost_resources
                if creature_health <= 0:
                    del population[creature_index]
                else:
                    creature[3] = ('Health', round(creature_health, 3))
                    creature[4] = ('Resources', round(creature_resources, 3))
                    population[creature_index] = creature

                competitor_health -= abs(creature_fitness * damage_multiplier)
                competitor_lost_resources = competitor_resources * per_lost_resources
                competitor_resources -= competitor_lost_resources
                if competitor_health <= 0:
                    del population[competitor_index]
                else:
                    competitor[3] = ('Health', round(competitor_health, 3))
                    competitor[4] = ('Resources', round(competitor_resources, 3))
                    population[competitor_index] = competitor

        else:
            creature[3] = ('Health', round(((creature_resources + (resource_reward * .5)) * health_multiplier), 3))
            creature[4] = ('Resources', round((creature_resources + (resource_reward * .5)), 3))
            population[creature_index] = creature
            competitor[3] = ('Health', round((competitor_resources + (resource_reward * .5) * health_multiplier), 3))
            competitor[4] = (
            'Resources', round((competitor_resources + (resource_reward * .5)), 3))
            population[competitor_index] = competitor

    print(f"# Fights: ", fighting_count)  # *** <- I'm here to make this eaiser to find with ctrl-f
    print(f"# Eat: ", eat_count)  # *** <- I'm here to make this eaiser to find with ctrl-f

    return population


def crossover(population):
    # Cycle through each creature so that they all have a CHANCE to breed
    for creature in range(len(population) - 1):
        # Choose a random possible mating partner; random so as not to include bias
        to_breed_with = random.randint(0, len(population) - 1)
        # Initialize our possible parents
        # Again I say possible because later we will find out if they become parents
        parent1 = population[creature]
        parent2 = population[to_breed_with]
        # Figure out the parents species, age, generation, health, resources, and if their the same species respectively
        specie_parent1 = parent1[0][1]
        specie_parent2 = parent2[0][1]
        parent1_age = parent1[1][1]
        parent2_age = parent2[1][1]
        parent1_gen = parent1[2][1]
        parent2_gen = parent2[2][1]
        parent1_health = parent1[3][1]
        parent2_health = parent2[3][1]
        parent1_resources = parent1[4][1]
        parent2_resources = parent2[4][1]

        parent1_sexually_mature, parent2_sexually_mature = False, False
        if specie_parent1 == "Charlen" and parent1_age >= charlen_maturity_age:
            parent1_sexually_mature = True
        if specie_parent2 == "Charlen" and parent2_age >= charlen_maturity_age:
            parent2_sexually_mature = True
        if specie_parent1 == "Gritis" and parent1_age >= gritis_maturity_age:
            parent1_sexually_mature = True
        if specie_parent1 == "Gritis" and parent2_age >= gritis_maturity_age:
            parent2_sexually_mature = True
        if specie_parent1 == "Drakonian" and parent1_age >= drakonian_maturity_age:
            parent1_sexually_mature = True
        if specie_parent1 == "Drakonian" and parent2_age >= drakonian_maturity_age:
            parent2_sexually_mature = True

        both_sexually_mature = parent1_sexually_mature and parent2_sexually_mature
        same_species = specie_parent1 == specie_parent2
        # both_same_gen = parent1_gen == parent2_gen

        # Store children in array so that when you edit the right parents because you first need to edit the parents
        # before placing children in population because it will mess with indexes of creatures in population
        children = []

        # Check if both parents are sexually mature and same species
        if same_species and both_sexually_mature:
            # Breed if parents pass probability of crossover and health is above 20
            while random.random() <= prob_crossover and (parent1_health > 20 and parent2_health > 20):
                # while parent1_health > 20 and parent2_health > 20:
                # print("Child", creature)
                p1_nn_weights1 = parent1[len(parent1) - 2][1]
                p1_nn_weights2 = parent1[len(parent2) - 1][1]
                p2_nn_weights1 = parent2[len(parent2) - 2][1]
                p2_nn_weights2 = parent2[len(parent2) - 1][1]
                r1 = random.randint(0, len(p1_nn_weights1) - 1)
                r2 = random.randint(0, len(p1_nn_weights2) - 1)
                parent1[len(parent1) - 2] = (parent1[len(parent1) - 2][0], np.concatenate((p1_nn_weights1[:r1], p2_nn_weights1[r1:]), axis=0))
                parent1[len(parent1) - 1] = (parent1[len(parent1) - 1][0], np.concatenate((p1_nn_weights2[:r2], p2_nn_weights2[r2:]), axis=0))
                parent2[len(parent2) - 2] = (parent2[len(parent2) - 2][0], np.concatenate((p2_nn_weights1[:r1], p1_nn_weights1[r1:]), axis=0))
                parent2[len(parent2) - 1] = (parent2[len(parent2) - 1][0], np.concatenate((p2_nn_weights2[:r2], p1_nn_weights2[r2:]), axis=0))

                # Change 4 when adjusting traits
                # The parent gives health and resources to children and in return the parents lose those resources
                parent_given_health = round(((parent1_health + parent2_health) / 2) * .5, 3)
                parent_given_resources = round(((parent1_resources + parent2_resources) / 2) * .3, 3)
                parent1_health = round(parent1_health - parent_given_health, 3)
                parent2_health = round(parent2_health - parent_given_health, 3)
                parent1_resources = round(parent1_resources - parent_given_resources, 3)
                parent2_resources = round(parent2_resources - parent_given_resources, 3)

                generation = max(parent1_gen, parent2_gen)
                r3 = random.randint(4, num_of_traits + 2)
                if random.random() <= .5:
                    child = parent1[:r3] + parent2[r3:]
                else:
                    child = parent2[:r3] + parent1[r3:]
                child[1] = ('Age', 0)
                child[2] = ('Gen.', generation + 1)
                child[3] = ('Health', parent_given_health)
                child[4] = ('Resources', parent_given_resources)
                children.append(child)

            parent1[3] = ('Health', parent1_health)
            parent2[3] = ('Health', parent2_health)
            parent1[4] = ('Resources', parent1_resources)
            parent2[4] = ('Resources', parent2_resources)
            population[creature] = parent1
            population[to_breed_with] = parent2

            # Now place children in
            [population.insert(random.randint(0, len(population) - 1), child) for child in children]

    return population


def mutation(population):
    for count in range(len(population) - 1):
        creature = population[count]
        for index in range(5, len(creature)):
            if random.random() <= prob_mutation:
                if creature[index][0] == "Neural Net W1" or creature[index][0] == "Neural Net W2":
                    nn = creature[index][1]
                    for weight in range(len(nn)):
                        if random.random() <= prob_mutation:
                            nn[weight] = round(nn[weight] * random.randint(5000, 15000)/10000, 8)
                    creature[index] = (creature[index][0], nn)
                else:
                    trait = old_trait = creature[index][1]
                    if random.random() <= .5:
                        trait = round(trait + (trait * mutation_rate), 3)
                    else:
                        trait = round(trait - (trait * mutation_rate), 3)
                    creature[index] = (creature[index][0], trait) if trait > 1 else (creature[index][0], old_trait)
        population[count] = creature

    return population


def update_age_health(population):
    creature = 0
    max_age = 0
    max_gen = 0
    while creature < len(population):
        # Make sure all creatures are not missing a trait or more
        assert not len(population[creature]) < num_of_traits
        # Trait is age which is at position 2
        current_age = population[creature][1][1]
        current_health = population[creature][3][1]
        updated_age = current_age + 1
        updated_health = round(current_health - (updated_age * age_penalty_multiplier), 3)
        # check if health at or below 0
        if updated_health <= 0:
            del population[creature]
            creature -= 1
        else:
            max_age = updated_age if updated_age > max_age else max_age
            max_gen = population[creature][2][1] if population[creature][2][1] > max_gen else max_gen
            population[creature][1] = ('Age', updated_age)
            population[creature][3] = ('Health', updated_health)

        creature += 1
    print(f"Max Age: {max_age}")
    print(f"Max Gen: {max_gen}")

    return population


def breed(population):
    return mutation(crossover(population))


def evolve(population, weights):
    fitness_scores = calc_fitness(population, weights)
    return update_age_health(breed(select_fittest(population, fitness_scores)))
