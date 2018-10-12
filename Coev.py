import random
import array
import numpy
import math

from deap import base
from deap import creator
from deap import tools
from deap import algorithms

import create_maze_graph as cm

def mazePrint(maze,goal,start):
    for i in range(len(maze)):
        line = "■ "
        for j in range(len(maze[0])):
            if([i,j] == goal):
                line = line + "X "
            elif([i,j] == start):
                line = line + "O "
            elif (maze[i][j] == True):
                line = line + "  "
            else:
                line = line + "■ "
        line = line + "■ "
        print(line)

MAX_MOVES = 20
NUM_AGENTS = 2
maze_test = cm.create_maze(4,4,0.75,0.75)
maze_easy = cm.create_maze(5,5,0.8,0.8)
maze_medium = cm.create_maze(8,8,0.25,0.25)
maze_hard = cm.create_maze(10,10,0.40,0.2)
maze_extreme = cm.create_maze(30,30,0.6,0.75)
maze = maze_medium

#TODO:: THIS IS COMPLETELY ARBITRARY!!
start = [0,0]
end = [4,4]

mazePrint(maze,end,start)
#Heuristic/fitness function. Input is individual (can treat like a list)
#output is score, Note: the comma is important
def evalOneMax(individual):
    print(individual)
    return sum(individual),

def evalMaze(ind, verbose = False):
    for thing in ind:
        print(thing)
    print("-----")
    return 1,
    # seen = set()
    # penalty = 0
    # c_c=[0,0]
    # c_c[0] = start[0]
    # c_c[1] = start[1]
    # n_c = [-1,-1]
    # move_counter = 1
    # early_stop = 0
    #
    # for i in range(len(ind)):
    #     n_c[0] = c_c[0]
    #     n_c[1] = c_c[1]
    #     seen.add((c_c[0],c_c[1]))
    #     if ind[i] == 1:
    #         n_c[0] = c_c[0] - 1
    #         if verbose:
    #             print("moving up " + str(c_c) + " to " + str(n_c))
    #     elif (ind[i] == 2):
    #         n_c[1] = c_c[1] + 1
    #         if verbose:
    #             print("moving right " + str(c_c) + " to " + str(n_c))
    #     elif (ind[i] == 3):
    #         n_c[0] = c_c[0] + 1
    #         if verbose:
    #             print("moving down " + str(c_c) + " to " + str(n_c))
    #     elif (ind[i] == 4):
    #         n_c[1] = c_c[1] - 1
    #         if verbose:
    #             print("moving left " + str(c_c) + " to " + str(n_c))
    #         if verbose:
    #         else:
    #             print("waiting at " + str(c_c))
    #     nx = n_c[0]
    #     ny = n_c[1]
    #
    #     if (nx >= len(maze) or ny >= len(maze[0]) or nx < 0 or ny < 0):
    #         if verbose:
    #             print("OUT OF BOUNDS")
    #         penalty+=2
    #
    #     elif(maze[nx][ny] == False):
    #         if verbose:
    #             print("INVALID MOVE")
    #         penalty+=2
    #     else:
    #         c_c[0] = n_c[0]
    #         c_c[1] = n_c[1]
    #         if((n_c[0],n_c[1]) in seen and ind[i] != 0):
    #             if verbose: print("seen")
    #             penalty+=1
    #         if(c_c == end):
    #             early_stop = i+1
    #             if verbose:
    #                 print("Reached Goal!!")
    #             break
    #
    # #calculate distance from goal
    # distance = math.sqrt((end[0]-c_c[0])**2 + (end[1]-c_c[1])**2)
    # path_length = (MAX_MOVES-early_stop)
    # if verbose:
    #     print("distance to goal:" + str(distance))
    #     print("penalty:" + str(penalty))
    #     print("path length:"+ str(path_length))
    #
    # return distance + penalty,


creator.create("FitnessMax", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
toolbox.register("attr_dir", random.randint, 1, 4)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_dir, MAX_MOVES)
toolbox.register("species", tools.initRepeat, list, toolbox.individual, 20)

toolbox.register("mate", tools.cxOnePoint)
toolbox.register("mutate", tools.mutUniformInt, indpb=0.05,low = 1, up = 4)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("get_best", tools.selBest, k=1)
toolbox.register("evaluate", evalMaze)

# pop = toolbox.population(n = 1000)
# hof = tools.HallOfFame(1)
#
# pop, log = algorithms.eaSimple(pop, toolbox, cxpb=0.50, mutpb=0.25, ngen=70,
#                                halloffame=hof, verbose=True)
#
# print(hof[0])
#
# print(evalMaze(hof[0],verbose = True))

species = [toolbox.species() for _ in range(NUM_AGENTS)]
representatives = [random.choice(species[i]) for i in range(NUM_AGENTS)]
species_index = list(range(NUM_AGENTS))
g = 1
ngen = 2
while g < ngen:
        # Initialize a container for the next generation representatives
    print(species)
    next_repr = [None] * len(species)
    for (i, s), j in zip(enumerate(species), species_index):
        # Vary the species individuals
        s = algorithms.varAnd(s, toolbox, 0.6, 1.0)

        # Get the representatives excluding the current species
        r = representatives[:i] + representatives[i+1:]
        for ind in s:
            # Evaluate and set the individual fitness
            ind.fitness.values = toolbox.evaluate([ind] + r)

        # Select the individuals
        species[i] = toolbox.select(s, len(s))  # Tournament selection
        next_repr[i] = toolbox.get_best(s)[0]   # Best selection

    representatives = next_repr
    print(next_repr)
    g+=1
