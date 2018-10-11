import random
import array
import numpy
import math

from deap import base
from deap import creator
from deap import tools
from deap import algorithms

import create_maze_graph as cm

MAX_MOVES = 20
maze_easy = cm.create_maze(4,4,0.75,0.75)
maze_test = cm.create_maze(5,5,0.8,0.8)
maze = maze_test

print(maze)
#TODO:: THIS IS COMPLETELY ARBITRARY!!
start = [0,0]
end = [2,2]
#Heuristic/fitness function. Input is individual (can treat like a list)
#output is score, Note: the comma is important
def evalOneMax(individual):
    print(individual)
    return sum(individual),

def evalMaze(ind, verbose = False):
    seen = set()
    penalty = 0
    c_c=[0,0]
    c_c[0] = start[0]
    c_c[1] = start[1]
    n_c = [-1,-1]
    move_counter = 1
    early_stop = 0

    for i in range(len(ind)):
        n_c[0] = c_c[0]
        n_c[1] = c_c[1]
        seen.add((c_c[0],c_c[1]))
        if ind[i] == 1:
            n_c[0] = c_c[0] - 1
            if verbose:
                print("moving up " + str(c_c) + " to " + str(n_c))
        elif (ind[i] == 2):
            n_c[1] = c_c[1] + 1
            if verbose:
                print("moving right " + str(c_c) + " to " + str(n_c))
        elif (ind[i] == 3):
            n_c[0] = c_c[0] + 1
            if verbose:
                print("moving down " + str(c_c) + " to " + str(n_c))
        elif (ind[i] == 4):
            n_c[1] = c_c[1] - 1
            if verbose:
                print("moving left " + str(c_c) + " to " + str(n_c))
        nx = n_c[0]
        ny = n_c[1]

        if (nx >= len(maze) or ny >= len(maze[0]) or nx < 0 or ny < 0):
            if verbose:
                print("OUT OF BOUNDS")
            penalty+=1

        elif(maze[nx][ny] == False):
            if verbose:
                print("INVALID MOVE")
            penalty+=1
        else:
            c_c[0] = n_c[0]
            c_c[1] = n_c[1]
            if((c_c[0],c_c[1]) in seen):
                if verbose: print("seen")
                penalty+=2
            if(c_c == end):
                early_stop = i+1
                if verbose:
                    print("Reached Goal!!")
                break

    #calculate distance from goal
    distance = math.sqrt((end[0]-c_c[0])**2 + (end[1]-c_c[1])**2)
    path_length = (MAX_MOVES-early_stop)
    if verbose:
        print("distance to goal:" + str(distance))
        print("penalty:" + str(penalty))
        print("path length:"+ str(path_length))

    return distance + penalty,
#determins if we are minimizing or maximizing
creator.create("FitnessMax", base.Fitness, weights=(-1.0,))

#what one individual looks like, in thise case it is a list
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

#generation function for an element of the individual
toolbox.register("attr_bool", random.randint, 1, 4)

#structure initializers, int at the end is size of the individual
toolbox.register("individual", tools.initRepeat, creator.Individual,
    toolbox.attr_bool, MAX_MOVES)

#structure initializer, do not touch
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

#specify heuristic here
toolbox.register("evaluate", evalMaze)

#mutation function, don't think we need another one
toolbox.register("mutate", tools.mutUniformInt, indpb=0.05,low = 0, up = 4)

#idk
toolbox.register("mate", tools.cxOnePoint)
toolbox.register("select", tools.selTournament, tournsize=3)

pop = toolbox.population(n = 2000)
hof = tools.HallOfFame(1)

pop, log = algorithms.eaSimple(pop, toolbox, cxpb=0.50, mutpb=0.25, ngen=60,
                               halloffame=hof, verbose=True)

print(hof[0])

print(evalMaze(hof[0],verbose = True))
