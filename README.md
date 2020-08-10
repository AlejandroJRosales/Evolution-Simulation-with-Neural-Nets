# Evolution Simulation 
### With Neural Network and Without Animation:
Basically, it is a glorified genetic algorithm mixed with a neural network... NEAT! (pun intended). The population contains three species: Charlens, Gritiss, and Drakonians. Each species has a special skill. Within each species, the creatures come with a small neural network that tells the creature what to do. The population is formed by the creatures within each species. When starting a new simulation (as opposed to loading a saved simulation), a normal distribution is implemented. This is for the initiation of all traits for the new population. Being an evolution simulation, each generation becomes fitter as the weak are weeded out (survival of the fittest). The stressor occurs as a creature fights or eats another creature, thus removing the weaker creature from the population and improving the chances of survival of the strong creature. Based on the creature's neural network, the choice to fight or to eat the other creature, or to remain passive, is up to them (wits). Each choice offers the pros and cons that a creature must wage in order to survive or to perish. 

This dilemma (to survive or to perish) depends on the creature's fitness, resources, and health status (infections, war, and injuries). Then, after the weak are weeded out each year. The strong mate and their offspring mutate. The mutations occur based on the probability of mutation and mutation rate. In this manner, the creature's neural networks evolve with each new generation. In tandem, the population will vary in size depending on the survival of the fittest.

Population size depends on the health status, resources, and how intelligent each creature is. Health status is affected by an infectious disease that can wipe out many creatures, or the species can go extinct. War can act in the same manner as an infectious disease regarding population size. At this time, infection or war is randomly determined. (I will likely change that later) Resources are a measure of what is available from parents to children. Resources can be a limitation when the offspring number increases in a population, although this can be a strategy of survival. Resource allocation is done probabilistically at the beginning, however, resource allocation will depend on the survival of the fittest. A creature can have access to more resources if it wins a fight or if it is not sick. Thus, a creature needs both wits and bronze if it wants to not only survive but thrive and pass on its genes.

A simple display of the population gives a summary of how the population is doing. The median creature for each species is shown. The population size of each species and total population size is shown. A bar graph of the median neural network weights for each creature is displayed every so often. You can also save as many simulations as you want and load them later! Also, the CPU and RAM usage is now shown.


[Run the code here using repl.it](https://repl.it/@n113/My-Simple-Simjulation-v2)


***
Implemented:
Simulation:
  1. Inititate Population From Normal Distribution (3 Species: Humans, Gritiss, and Drakonians)
  2. Survival of the fittest (Fitness Scores, Tournament Selection)
  3. Fittest Breed (Mutations, Crossover)
  4. "Enviromental" Factors (Simple weights applied to skills)
  5. Species Can Have Up To N kids. (Let N be number of kids and P be probability of having next kid. P = .4/N)
  6. Species Can Go Extinct (1, 2, or All)
  7. Infectious Disease Can Kill N% of Total Population
  8. There are wars, one where everyone fights everyone, species wars, where it is one species against another
  9. Neural Networks are now in every creature 
  10. Added health and resources for each creature
  11. Shared Resources
  12. Wars
  13. Mass extinction from illness

Display:
  1. Display Generation and Key Trait Along With Weights For Other Traits
  2. Display Counts of Species and Total Population Size
  3. Display Medians for All Species, inclduing weights for neural networks
  4. Display CPU and RAM usage
  5. Display graph of median neural networks for each species

Extra:
  1. Can save simulations and load them later


***
To-Do:
1. Small, Fast Depiction of Life
2. More Species
3. Depiction of Speices
4. ~~Shared Resources (Intelligence Required)~~
5. ~~Wars~~
6. ~~Mass Extinction From Illness~~
7. Include Mutating Viruses that Weak Fitness or Kills

### With Matplotlib Animation and Without Neural Network:
Basically, the creatures as displayed on a grid using matplotlib animation function. The creatures are yellow, and the empty spots are purple. The creatures, currently, move around randomly. That being said, I would like to add eyesight to them so that they can see food and go to it, or even chase prey. Adding a neural network, even a small one, might be too computationally expensive, but we'll see. The creatures have fitness and energy. The energy levels deplete as each hour passes. If the energy goes below 0, then the creature dies. A creature needs energy level proportionally higher to their fitness to procreate. This proporiton can be edited. Next, if a creature, a child or not, runs into, another creature, then each creatures fitness will decide who lives and who dies. 
There are also things the user can do to interact with the creatures. The user can press pause to pause the simulation. This is to drop single pieces of food on the grid for a creature to eat. Or the user can drop mass amounts of food on the grid. Each piece of food is randomly set to a number. This number, when the piece of food is eaten, increases their fitness and energy of the creature that ate the food by the amount the food number was set to. In addition, the user can set off an explosion that blows up a ceratain area of the grid. The user can also press "t" to activate the thanos feature. The thanos feature, as guessed, kills about 50% of all the creatures on the grid.
For the strings displayed on the plot, year:days:hours are displayed. So is the number of creatures alive, and how many have died. In addition, the max fitness and energy is displayed. Note, not neccesarily of the same creature.

*** 
Implemented:
  1. Food in simulation
  2. pause game
  3. Thanos (kill 50% of pop randomly)
  4. Bomb
  5. energy and can reproduce at a certain level
  6. year:day:hour
  7. Food randomly generated at random times

***
To-Do:
  1. 1 block 360 eyesight
  2. select character move around
  3. different species (some fast, some slower, some stronger, etc.)
  4. food and prey
  5. serial killer prey cant see them (red prey)
  6. green plants that only oragne can eat
  7. 0 energy decreses health slowly

### On a final note:
 I am looking to continue to improve this game for the rest of my life. Basically, way down the road, adding in morals and better         machine learning and a better, easier-on-the-eyes display. Basically,  to simulate *life* is the goal. A far cry from what I have now,   but it is the goal nonetheless. 
