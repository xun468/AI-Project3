import random
import array
import numpy
import math

from deap import base
from deap import creator
from deap import tools
from deap import algorithms

import create_maze_graph as cm

def mazePrint(maze,goal,start,start2):
    wall = "■ ■ "
    for i in range(len(maze)):
        wall+= "■ "
    print(wall)
    for i in range(len(maze)):
        line = "■ "
        for j in range(len(maze[0])):
            if([i,j] == goal):
                line = line + "G "
            elif([i,j] == start):
                line = line + "O "
            elif([i,j] == start2):
                line = line + "X "
            elif (maze[i][j] == True):
                line = line + "  "
            else:
                line = line + "■ "
        line = line + "■ "
        print(line)
    print(wall)

MAX_MOVES = 20
maze_test = cm.create_maze(4,4,0.75,0.75)
maze_easy = cm.create_maze(5,5,0.8,0.8)
maze_medium = cm.create_maze(8,8,0.25,0.25)
maze_hard = cm.create_maze(10,10,0.40,0.2)

maze = maze_test

#Test
#[0,0],[0,1],[4,4]
#Easy
#[0,0],[4,0],[2,2]
#Medium
#[0,0],[0,8],[4,4]
#hard
#[0,0],[0,10],[2,8]

start = [0,0]
start2 = [0,4]
end = [4,4]

mazePrint(maze,end,start,start2)
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
    path_length = 0

    for i in range(len(ind)):
        n_c[0] = c_c[0]
        n_c[1] = c_c[1]
        path_length += 1
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
        else:
            if verbose:
                print("waiting at " + str(c_c))
        nx = n_c[0]
        ny = n_c[1]

        if (nx >= len(maze) or ny >= len(maze[0]) or nx < 0 or ny < 0):
            if verbose:
                print("OUT OF BOUNDS")
            penalty+=2

        elif(maze[nx][ny] == False):
            if verbose:
                print("INVALID MOVE")
            penalty+=2
        else:
            c_c[0] = n_c[0]
            c_c[1] = n_c[1]
            if((n_c[0],n_c[1]) in seen and ind[i] != 0):
                if verbose: print("seen")
                penalty+=1
            if(c_c == end):
                if verbose:
                    print("Reached Goal!!")
                break

    #calculate distance from goal
    distance = math.sqrt((end[0]-c_c[0])**2 + (end[1]-c_c[1])**2)
    bonus = 0
    if distance == 0:
        bonus = MAX_MOVES-path_length + 100
    if verbose:
        print("distance to goal:" + str(distance))
        print("penalty:" + str(penalty))
        print("path length:"+ str(path_length))

    return distance + penalty - bonus,
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
toolbox.register("mutate", tools.mutUniformInt, indpb=0.05,low = 1, up = 4)

#idk
toolbox.register("mate", tools.cxOnePoint)
toolbox.register("select", tools.selTournament, tournsize=3)

# pop = toolbox.population(n = 1000)
# hof = tools.HallOfFame(1)
#
# pop, log = algorithms.eaSimple(pop, toolbox, cxpb=0.50, mutpb=0.25, ngen=70,
#                                halloffame=hof, verbose=True)
#
# print(hof[0])
#
# print(evalMaze(hof[0],verbose = True))
