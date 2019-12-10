# Evolution Simulation with Neural Network
​Basically, it is a glorified genetic algorithm mixed with a neural network... NEAT! (pun intended). There are three species: Charlens, Gritiss, and Drakonians. Each species has a special skill. Each creature comes with a small neural network that tells the creature what to do. When starting a new simulation (as opposed to loading a saved simulation), a normal distribution is implemented for the initiation of all traits for the new population. As time passes, each generation becomes fitter as the weak are weeded out. This occurs when a creature fights or eats another creature, thus removing the weaker creature from the population and improving the chances of survival of the strong creature. This choice to fight or eat the other creature, or remain passive towards is up to them. Each choice offers pros and cons that a creature must figure out how to take advantage of to survive. For when fighting, the creature's fitness, resources, and health come into play. Then, after the weak are weeded out each year, the strong crossover and their offspring mutate. (The neural networks evolve with each new generation) Population sizes vary, both for each species and the total population. Population sizes depend on the health, resources, and how smart each creature is. As well as if an infectious disease wipes out many, and/or a species goes extinct during a war. Having many children is a strategy to ensure the species survival, however, it may not be the best option, as every child the parent has is given health and resources from the parent. Thus, a creature needs both wits and bronze if it wants to not only survive but thrive and pass on its genes.

A simple display of the population gives a summary of how the population is doing. The median creature for each species is shown. The population size of each species and total population size is shown. A bar graph of the median neural network weights for each creature is displayed every so often. You can also save as many simulations as you want and load them later! Also, the CPU and RAM usage is now shown.

On a final note:
  I am looking to continue to improve this game for the rest of my life. Basically, way down the road, adding in morals and better         machine learning and a better, easier-on-the-eyes display. Basically,  to simulate *life* is the goal. A far cry from what I have now,   but it is the goal nonetheless. 

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
  10. Added health and resources for each creature

Display:
  1. Display Generation and Key Trait Along With Weights For Other Traits
  2. Display Counts of Species and Total Population Size
  3. Display Medians for All Species, inclduing weights for neural networks
  4. Display CPU and RAM usage
  5. Display graph of median neural networks for each species

Extra:
  1. Can save simulations and load them later


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
  1. Use Unity to display creatures or program it as a app!!!!
