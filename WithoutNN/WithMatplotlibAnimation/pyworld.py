import numpy as np
import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# import console


# setting up the values for the grid
OFF = 0
DRAKONIAN_ON = 60
GRITIS_ON = 255
FOOD_ON = 200
vals = [DRAKONIAN_ON, GRITIS_ON, OFF]
species_color_dict = {"Drakonian": DRAKONIAN_ON, "Gritis": GRITIS_ON}
population = dict()
food_pot = dict()
species_list = ["Gritis", "Drakonian"]
new_grid = np.array([])
death_count = 0
drakonian_pop_size = 0
gritis_pop_size = 0
max_fitness = 0
max_energy = 0
# 0.05
drakonian_p = 0.05
gritis_p = 0.05
p_off = 1 - drakonian_p - gritis_p
# 0.0005
prob_rand_food_gen = 0.005
parent_num = 2
movement_energy_perc_loss = 0.001
# energy needed proportionate to fitness
energy_perc_for_child = 0.8
perc_of_char_given = 0.7
mouse_side = "None"
pause = False
bomb_set = False
thanos_on = False
mass_food_on = False

# set day
year = 0
day = 0
hour = 0
hours_per_day = 24
days_per_year = 356
# set grid size
x = 50
y = 80
ix = -1
iy = -1


class UserActions:
    @staticmethod
    def onclick(event):
        global food_pot
        global ix, iy
        global mouse_side

        if str(event.button) == "MouseButton.LEFT":
            mouse_side = "Left"
            ix, iy = int(event.xdata), int(event.ydata)
            # print('x = %d, y = %d' % (ix, iy))

            food_pot[(iy, ix)] = random.randint(10, 20)

        elif str(event.button) == "MouseButton.RIGHT":
            mouse_side = "Right"
            ix, iy = int(event.xdata), int(event.ydata)
            # print('x = %d, y = %d' % (ix, iy))

    @staticmethod
    def key_event(event):
        # ctrl+p for something different
        if str(event.key) == "p":
            global pause
            pause = not pause

        elif str(event.key) == "b":
            global bomb_set
            bomb_set = not bomb_set

        elif str(event.key) == "t":
            global thanos_on
            thanos_on = True

        elif str(event.key) == "m":
            global mass_food_on
            mass_food_on = not mass_food_on

    @staticmethod
    def update_user_actions():
        global mouse_side
        global thanos_on
        global food_pot
        global ix, iy
        global death_count

        if mouse_side == "Left":
            if bomb_set:
                for row in range(-8, 9):
                    for col in range(-8, 9):
                        pos = (iy + col, ix + row)
                        if pos in population:
                            del population[pos]
                            new_grid[pos] = OFF
                            death_count += 1
                        if pos in food_pot:
                            del food_pot[pos]
                            new_grid[pos] = OFF

            if mass_food_on:
                for row in range(-4, 5):
                    for col in range(-4, 5):
                        pos = (iy + col, ix + row)
                        food_pot[pos] = random.randint(2, 10)
                        new_grid[pos] = FOOD_ON

            # if we did not just start the program, hence ix and iy would be -1 if we did
            # then add the food_pot to the new grid
            if not mass_food_on and not bomb_set:
                new_grid[(iy, ix)] = FOOD_ON

            ix, iy = -1, -1

        elif mouse_side == "Right":
            if (iy, ix) in population:
                fitness_number = population[(iy, ix)]
                selected_creature_id = (iy, ix)
                display_fitness = True

            # ix, iy = -1, -1

        if thanos_on:
            keys = []
            for key in population:
                keys.append(key)

            for pos in keys:
                if random.random() <= 0.5:
                    del population[pos]
                    new_grid[pos] = OFF
                    death_count += 1

            thanos_on = False

        mouse_side = "None"


class CreatureActions:
    @staticmethod
    def update_time(hour, day, year):
        hour += 1
        if hour % hours_per_day == 0:
            day += 1
            hour = 0
        if day != 0 and day % days_per_year == 0:
            year += 1
            day = 0

        return hour, day, year

    @staticmethod
    def keys_and_stats():
        # copy keys and get stats to minimize number of loops
        keys = []
        # max_fitness = 0
        # max_energy = 0
        drakonian_pop_size = 0
        gritis_pop_size = 0
        for key in population:
            creature = population[key]
            if creature["species"] == "Drakonian":
                drakonian_pop_size += 1
            if creature["species"] == "Gritis":
                gritis_pop_size += 1
            # if creature["fitness"] > max_fitness:
            #     max_fitness = creature["fitness"]
            # if creature["energy"] > max_energy:
            #     max_energy = creature["energy"]
            keys.append(key)

        return keys, max_fitness, max_energy, drakonian_pop_size, gritis_pop_size

    @staticmethod
    def generate_population(x, y):
        """returns a grid of NxN random values"""
        random_grid = np.random.choice(vals, x * y, p=[drakonian_p, gritis_p, p_off]).reshape(x, y)
        for i in range(y):
            for j in range(x):
                key = (j, i)
                characteristics = dict()
                if random_grid[j, i] == DRAKONIAN_ON:
                    # species
                    characteristics["species"] = "Drakonian"
                    # add fitness
                    characteristics["fitness"] = random.randint(10, 100)
                    # add energy
                    characteristics["energy"] = random.randint(20, 50)
                    population[key] = characteristics
                elif random_grid[j, i] == GRITIS_ON:
                    # species
                    characteristics["species"] = "Gritis"
                    # add fitness
                    characteristics["fitness"] = random.randint(10, 100)
                    # add energy
                    characteristics["energy"] = random.randint(20, 50)
                    population[key] = characteristics

        return random_grid

    def rand_generate_food(self):
        for i in range(y):
            for j in range(x):
                if random.random() <= prob_rand_food_gen:
                    food_pot[(j, i)] = random.randint(2, 10)
                    new_grid[(j, i)] = FOOD_ON

    @staticmethod
    def creature_consume_food():
        # copy food keys so we can edit the dictionary
        keys = []
        for key in food_pot:
            keys.append(key)

        # check all of the creatures to see if they reached food
        for food_loc in keys:
            for creature_loc in population:
                if food_loc == creature_loc:
                    creature = population[creature_loc]
                    creature["fitness"] += food_pot[food_loc]
                    creature["energy"] += food_pot[food_loc]
                    del food_pot[food_loc]
                    # since the creature is at the food location, simply turn it from food on to just on for the
                    # creature to now be displayed instead of the food
                    if creature["species"] == "Drakonian":
                        new_grid[food_loc] = DRAKONIAN_ON
                    elif creature["species"] == "Gritis":
                        new_grid[food_loc] = GRITIS_ON

    @staticmethod
    def reproduce(grid, keys, death_count):
        for key in keys:
            creature = population[key]
            # this grabs the color for the species that the creature is
            ON = species_color_dict[creature["species"]]

            # we use i and j specifically for moving the creature to a new grid location/create new id
            j = key[0]
            i = key[1]

            # compute 8-neighbor sum
            # using toroidal boundary conditions - x and y wrap around
            # so that the simulation takes place on a toroidal surface.
            total = 0
            if grid[j, (i - 1) % y] == ON:
                total += 1
            if grid[j, (i + 1) % y] == ON:
                total += 1
            if grid[(j - 1) % x, i] == ON:
                total += 1
            if grid[(j + 1) % x, i] == ON:
                total += 1
            if grid[(j - 1) % x, (i - 1) % y] == ON:
                total += 1
            if grid[(j - 1) % x, (i + 1) % y] == ON:
                total += 1
            if grid[(j + 1) % x, (i - 1) % y] == ON:
                total += 1
            if grid[(j + 1) % x, (i + 1) % y] == ON:
                total += 1

            # create new creatures randomly next to the parent if there is the needed number of parents and
            # the energy is higher proportionally compared to the fitness of the creature at j, i
            # if the world is filling up to fast change the total == to a higher number so there must be a greater
            # of other creatures next to the creature for it to procreate
            if grid[key] == ON and total == parent_num and creature["energy"] > creature["fitness"] * energy_perc_for_child:
                new_key = 0
                r = random.randint(0, 7)
                if r == 0:
                    new_key = (j, (i - 1) % y)
                if r == 1:
                    new_key = (j, (i + 1) % y)
                if r == 2:
                    new_key = ((j - 1) % x, i)
                if r == 3:
                    new_key = ((j + 1) % x, i)
                if r == 4:
                    new_key = ((j - 1) % x, (i - 1) % y)
                if r == 5:
                    new_key = ((j - 1) % x, (i + 1) % y)
                if r == 6:
                    new_key = ((j + 1) % x, (i - 1) % y)
                if r == 7:
                    new_key = ((j + 1) % x, (i + 1) % y)

                parent = creature
                fitness_given = int(parent["fitness"] * perc_of_char_given)
                energy_given = int(parent["energy"] * perc_of_char_given)

                # create the child first and add some of the parent fitness/energy
                child = dict()
                child["species"] = parent["species"]
                child["fitness"] = parent["fitness"] + random.randint(-fitness_given, fitness_given)
                child["energy"] = parent["energy"] + random.randint(-energy_given, energy_given)

                # remove fitness from parent even if child does not make it
                parent["fitness"] -= fitness_given
                parent["energy"] -= energy_given
                population[key] = parent
                if new_key in population:
                    # get creature at new_key as that's the position the child will go to
                    other = population[new_key]
                    if child["fitness"] > other["fitness"]:
                        # keep the key as the key does not change, but change the creature as that does
                        population[new_key] = child
                    # else, if other fitness is greater than child fitness than do nothing as other stays there and
                    # child dies, hence not added to board but is added to death cout
                    death_count += 1
                else:
                    # if there is not another creature there add the child to the population and to the new grid
                    population[new_key] = child
                    new_grid[new_key] = ON

        return death_count

    @staticmethod
    def creature_movement(keys, hour, death_count):
        for key in keys:
            original_creature = population[key]
            # since we start with an even time and end with an even time, and since the time loops, we may run into a
            # a problem here, so fix this bug

            # nevertheless, we are checking if the hour is even, if so every creature gets to move, if not
            # then check if the creature is drakonian, if they are then they always get to move, regardless of the time
            # aka, they drakonians move every hour, while the rest move every other hour
            if hour % 2 == 0 or original_creature["species"] == "Drakonian":
                # Subtract the energy loss from movment once the creature moves. If they are Drakonian, this happen more
                # often, but they also get to move more often
                original_creature["energy"] -= original_creature["energy"] * movement_energy_perc_loss

                r = random.randint(0, 7)
                new_key = 0
                j = key[0]
                i = key[1]
                if r == 0:
                    new_key = (j, (i - 1) % y)
                elif r == 1:
                    new_key = (j, (i + 1) % y)
                elif r == 2:
                    new_key = ((j - 1) % x, i)
                elif r == 3:
                    new_key = ((j + 1) % x, i)
                elif r == 4:
                    new_key = ((j - 1) % x, (i - 1) % y)
                elif r == 5:
                    new_key = ((j - 1) % x, (i + 1) % y)
                elif r == 6:
                    new_key = ((j + 1) % x, (i - 1) % y)
                elif r == 7:
                    new_key = ((j + 1) % x, (i + 1) % y)

                final_alive_creature = []
                if new_key in population:
                    challenger_creature = population[new_key]
                    if original_creature["fitness"] < challenger_creature["fitness"]:
                        # if the challenger is fitter than the creature currently at the position
                        # then set the final alive creature to the challenger
                        final_alive_creature = challenger_creature
                    # add to the death count as regardless one creature will die if there are two
                    # creatures fighting for a
                    # position
                    else:
                        final_alive_creature = original_creature
                    death_count += 1

                else:
                    # if the new creature does not meet another creature when moving then del old
                    # and replace creature at new position
                    del population[key]
                    final_alive_creature = original_creature
                    new_grid[key] = OFF

                # take the final alive creature and check if its energy is at or below 0, if so, kill it
                if final_alive_creature["energy"] > 0:
                    population[new_key] = final_alive_creature
                    # set the new grid at the new key on if the creature lives, because if it does not then its
                    # old position will be deleted and turned off, and the new position will not be added to population
                    # of the new grid
                    # this grabs the color for the species that the creature is
                    ON = species_color_dict[final_alive_creature["species"]]
                    new_grid[new_key] = ON
                else:
                    death_count += 1

        return death_count

    def update(self, grid):
        global hour
        global day
        global year
        global new_grid
        # global max_fitness
        # global max_energy
        global death_count
        global drakonian_pop_size
        global gritis_pop_size

        # I traverse the dictionaries inside the functions instead of traverse the dictionaries and call different
        # functions each time because it saves processing time

        # copy the keys so we can edit the population dictionaries. We do it this way so that we can also find the
        # max fitness and energy
        population_keys, max_fitness, max_energy, drakonian_pop_size, gritis_pop_size = self.keys_and_stats()

        self.rand_generate_food()

        self.creature_consume_food()

        # this first loop is for the creatures to have children first
        death_count = self.reproduce(grid, population_keys, death_count)

        # then this second loop is to have the creatures and the kids to move about the world
        death_count = self.creature_movement(population_keys, hour, death_count)

        # hour completed, so add to hour count
        hour, day, year = self.update_time(hour, day, year)


class Display:
    def __init__(self):
        self.creature_action = CreatureActions()
        self.user_action = UserActions()

    @staticmethod
    def display_info(img, fitness_number, selected_creature_id, display_fitness):
        # update data
        # print(f"Alive: {len(population)}\tDeath Count: {death_count}")
        plt.suptitle(f"Y:D:H: {year}:{day}:{hour} - Alive: {drakonian_pop_size + gritis_pop_size:,} - Death Count: {death_count:,}", fontsize=11)
        plt.xlabel(f"Drakonian's: {drakonian_pop_size:,} Gritis's': {gritis_pop_size:,}", fontsize=11)
        # if display_fitness:
        #     plt.xlabel(f"CreatureActions {selected_creature_id} Fitness: {fitness_number}", fontsize=11)
        # else:
        #     plt.xlabel(f"Max Fitness: {max_fitness} - Max Energy: {round(max_energy, 1)}", fontsize=10)
        img.set_data(new_grid)

    def update(self, frameNum, fig, img, grid):
        global new_grid

        fitness_number = 0
        selected_creature_id = (-1, -1)
        display_fitness = False

        # copy grid since we require 8 neighbors
        # for calculation and we go line by line
        new_grid = grid.copy()
        self.creature_action.update(grid) if not pause else None

        fig.canvas.mpl_connect('button_press_event', self.user_action.onclick)
        fig.canvas.mpl_connect('key_press_event', self.user_action.key_event)
        self.user_action.update_user_actions()

        self.display_info(img, fitness_number, selected_creature_id, display_fitness)
        grid[:] = new_grid[:]

        return img,


def main():
    creature = CreatureActions()
    display = Display()

    # set animation update interval
    updateInterval = 1

    # declare grid
    grid = creature.generate_population(x, y)

    # set up animation
    # count = 0
    fig, ax = plt.subplots()
    img = ax.imshow(grid)
    # show animation
    count = 0
    while True:
        # show animation
        ani = animation.FuncAnimation(fig, display.update, fargs=(fig, img, grid,), frames=10, interval=updateInterval,
                                      save_count=50)

        plt.show()

        if count == 100:
            # console.clear()
            count = 0

        count += 1


# call main
if __name__ == '__main__':
    main()
