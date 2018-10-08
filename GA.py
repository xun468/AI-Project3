import random
import array
import numpy

from deap import base
from deap import creator
from deap import tools
from deap import algorithms


#Heuristic/fitness function. Input is individual (can treat like a list)
#output is score, Note: the comma is important
def evalOneMax(individual):
    print(individual)
    return sum(individual),

#determins if we are minimizing or maximizing
creator.create("FitnessMax", base.Fitness, weights=(-1.0,))

#what one individual looks like, in thise case it is a list
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

#generation function for an element of the individual
toolbox.register("attr_bool", random.randint, 0, 4)

#structure initializers, int at the end is size of the individual
toolbox.register("individual", tools.initRepeat, creator.Individual,
    toolbox.attr_bool, 3)

#structure initializer, do not touch
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

#specify heuristic here
toolbox.register("evaluate", evalOneMax)

#mutation function, don't think we need another one
toolbox.register("mutate", tools.mutUniformInt, indpb=0.05,low = 0, up = 4)

#idk
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("select", tools.selTournament, tournsize=3)

pop = toolbox.population(n = 200)
hof = tools.HallOfFame(1)

pop, log = algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=40,
                               halloffame=hof, verbose=True)

print(hof[0])
