# My Simple Simulation
A simple world simulation. Basically, it is a glorified genetic algorithm. There are three species, Humans, Gritiss, and Drakonians.
Each species has a special skill. Through evolution, each generation becomes better as the weak are weeded out and the strong crossover and their young mutate. A normal distribution is implemented for all traits for the initiation of the starting population and "new blood" population. Population size grows over time. Extinction is all too real for each species. For a species can overtake them all or infectious disease can wipe out many. 

A simple display or the population gives a summary of how the population is doing. Such as the median creature for each species and the population size of each species. A better format will hopefully be coming later. I am looking to continue to improve this game for the rest of my life. Basically, way down the road, adding in morals and machine learning and a better, easier-on-the-eyes display. Basically,  to simulate *life* is the goal. A far cry from what I have now, but it is the goal nonetheless. 

[Run the code here](https://repl.it/@n113/My-Simple-Simulation)


### Implemented
***

Simulation:
  1. Inititate Population From Normal Distribution (3 Species: Humans, Gritiss, and Drakonians)
  2. Survival of the fittest (Fitness Scores, Tournament Selection)
  3. Fittest Breed (Mutations, Crossover)
  4. "Enviromental" Factors (Simple weights applied to skills)
  5. Drakonians Can Hunt in Packs
  6. Species Can Have Up To N kids. (Let N be number of kids and P be probability of having next kid. P = .4/N)
  7. Species Can Go Extinct (1, 2, or All)
  8. Infectious Disease Can Kill N% of Total Population
  9. There are simple wars (everyone fights everyone) and species wars, where it is one species against another

Display:
  1. Display Generation and Key Trait Along With Weights For Other Traits
  2. Display Counts of Species and Total Population Size
  3. Display Medians for All Species




### To-Do
***

Simulation:
  1. Adjust Pack Hunting
  2. Small, Fast Depiction of Life
  3. More Species
  4. Depiction of Speices
  5. Shared Resources (Intelligence Required)
  6. ~~Wars~~
  7. ~~Mass Extinction From Illness~~
  8. Include Map
  9. Include Mutating, Viruses that Weak Fitness or Kills

Display:
  1. Just Make it Better
