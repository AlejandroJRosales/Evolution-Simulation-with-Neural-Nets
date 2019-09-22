# Evolution Simulation with Neural Network
A simple evolution simulation. Basically, it is a glorified genetic algorithm mixed with neuro evolution. There are three species, Charlens, Gritiss, and Drakonians. Each species has a special skill. Each creature comes with a small neural network that, based of the input and weights, tell the creature what to do. Through evolution, each generation becomes better as the weak are weeded out. Through fighting, resources and health come into play. After the weak are weeded out, the strong crossover and their young mutate. (The neural networks evolve with the creatures) A normal distribution is implemented for all traits for the initiation of the starting population. Population size can grow over time or shrink and so can the population sizes of each species, depeneding on the health of the creatures and how smart they are. Extinction is all too real for each species. As a species can overtake them all, infectious disease can wipe out many, and/or a species could go extinct during war.

A simple display of the population gives a summary of how the population is doing. The median creature for each species is shown. Showing their traits and weights of their neural network. The population size of each species and total population size is shown. I am looking to continue to improve this game for the rest of my life. Basically, way down the road, adding in morals and better machine learning and a better, easier-on-the-eyes display. Basically,  to simulate *life* is the goal. A far cry from what I have now, but it is the goal nonetheless. 

[Run the code here](https://repl.it/@n113/My-Simple-Simjulation-v2)


### Implemented
***

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

Display:
  1. Display Generation and Key Trait Along With Weights For Other Traits
  2. Display Counts of Species and Total Population Size
  3. Display Medians for All Species, inclduing weights for neural networks




### To-Do
***

Simulation:
  1. Small, Fast Depiction of Life
  2. More Species
  3. Depiction of Speices
  4. ~~Shared Resources (Intelligence Required)~~
  5. ~~Wars~~
  6. ~~Mass Extinction From Illness~~
  7. Include Mutating Viruses that Weak Fitness or Kills

Display:
  1. Use Blender to display creatures!!!!
