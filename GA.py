'''
    Created by Justin Weiss on 2/28/20.
    Copyright © 2020 Justin Weiss. All rights reserved.

    This program using a Genetic Algorithm to find the minmum number of coins
    from a dollar amount inputed by the user

    To Run: GA.py <dollar amount> <population Size>

    Note: I converted the dollar amount into a whole number for simplicity.
    Example: Quarter = 0.25 but in my program a quarter is 25
'''


import random
import sys

# reads in the dollar amount and Population size from input
input = float(sys.argv[1])
populationSize = int(sys.argv[2])

# calculates the min number of coins, the goal
def goalCalc (temp):
    q = int(temp//25)
    d = int(temp - (q*25))//10
    n = int(temp - (q*25) - (d*10))//5
    p = int(temp - (q*25) - (d*10) - (n*5))
    return (q+d+n+p)

# Sets global values
max = int(input*100)
mutation = 10
goal = goalCalc(max)

# Creates the class for the Individual in the population
class Individual (object):
    """docstring for Individual."""

    # The Individual is made up of the number of each type of coin and it's fitness value
    def __init__(self, quarters, dimes, nickels, pennies):
        self.quarters = quarters
        self.dimes = dimes
        self.nickels = nickels
        self.pennies = pennies
        self.fitness = self.fitnessCalc()

    # This function ranodmly generates the first Individual for the population
    @classmethod
    def createIndividual (self):
        global max
        value = 0

        # Loops until the random set of coins equals the correct dollar amount
        while (max != value):
            quarters = random.randint(0, (max//25))
            dimes = random.randint(0, (max//10))
            nickels = random.randint(0, (max//5))
            pennies = random.randint(0, (max))
            #pennies = (max-(quarters*25))

            # Calculates the correct dollar amount
            value = self.calculateValue (quarters, dimes, nickels, pennies)

        if max==value:
            return(quarters, dimes, nickels, pennies)
        else:
            print("ERROR")

    # Calculates fitness by adding the total number of coins and subtracting the goal
    # Therefore if $1 is inputed the goal would be 4 quarters and 4-4=0, fitness
    # would be 0 and that would be the most optimal set of coins
    def fitnessCalc (self):
        global goal
        return ((self.quarters + self.dimes + self.nickels + self.pennies)-goal)

    # Calculates the value of coins not yet in the population, must enter the
    # coin values in the input of the function
    def calculateValue (quarters, dimes, nickels, pennies):
        return ((quarters*25) + (dimes*10) + (nickels*5) + (pennies*1))

    # calculates the individuals value
    def calcIndividualValue (self):
        return ((self.quarters*25) + (self.dimes*10) + (self.nickels*5) + (self.pennies))

    # This function takes 2 parents, parent1 as self and parent2 as parent2,
    # it then mates them based off a random percentage
    def mate (self, parent2):
        global mutation
        probability = random.randint(1,100)

        # 30% of the time
        if probability<=30:
            child = parent2
            child.quarters = self.quarters
            child.dimes = self.dimes

        # 30% of the time
        elif probability<=60:
            child = parent2
            child.quarters = self.quarters
            child.pennies = self.pennies

        # 30% of the time, since mutation = 10%
        elif probability<=(100-mutation):
            child = parent2
            child.pennies = self.pennies
            child.nickels = self.nickels

        # 10% of the time randomly generate a new child, this is user setable
        # at the top just change mutation
        else:
            quarters, dimes, nickels, pennies = Individual.createIndividual()
            child = Individual(quarters, dimes, nickels, pennies)

        # recalculate the child fitness and set it, then return child
        child.fitness = child.fitnessCalc()
        return child

def main():
    global populationSize
    global max
    generation = 1
    found = False
    population = []

    # create initial population
    for _ in range(populationSize):
        ''' creates one person in population '''
        quarters, dimes, nickels, pennies = Individual.createIndividual()
        population.append(Individual(quarters, dimes, nickels, pennies))

    print("Population Created!")

    while not found:
        # sort the population in increasing order of fitness score
        population = sorted(population, key = lambda x:x.fitness)

        # Checks to see if the first Individual in the population is the most fit
        if population[0].fitness == 0:
            if Individual.calcIndividualValue(population[0])==max:
                found = True
                break

        # Creates a new population and puts the 5 most fit into the new population
        new_population = []
        new_population.extend(population[:5])

        # Loops through the rest of the population mating them
        for _ in range(populationSize-5):
            value = 0

            # Loops until the mate is the correct dollar amount
            while (max != value):
                # Randomly selects 2 parents from the top 50% of the population
                parent1 = population[random.randint(0,populationSize//2)]
                parent2 = population[random.randint(0,populationSize//2)]
                child = parent1.mate(parent2)
                value = Individual.calcIndividualValue(child)

            if max==value:
                #print(max)
                #print(value)
                #return(quarters, dimes, nickels, pennies)
                new_population.append(child)
            else:
                print("ERROR")
            #new_population.append(child)

        del population
        population = new_population
        del new_population

        population = sorted(population, key = lambda x:x.fitness)

        print("Fitness: %d" %population[0].fitness,\
            "  Q: %d" %population[0].quarters,\
            "  D: %d" %population[0].dimes,\
            "  N: %d" %population[0].nickels,\
            "  P: %d" %population[0].pennies,\
            "  Generation: %d" %generation,
            "  Value: %d" %value)
        generation += 1

    print("Fitness: %d" %population[0].fitness,\
        "  Q: %d" %population[0].quarters,\
        "  D: %d" %population[0].dimes,\
        "  N: %d" %population[0].nickels,\
        "  P: %d" %population[0].pennies,\
        "  Generation: %d" %generation,
        "  Value: %d" %Individual.calcIndividualValue(population[0]))

main()
