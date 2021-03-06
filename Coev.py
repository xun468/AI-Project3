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

MAX_MOVES = 16
NUM_AGENTS = 2
maze_test = cm.create_maze(4,4,0.75,0.75)
maze_easy = cm.create_maze(5,5,0.8,0.8)
maze_medium = cm.create_maze(8,8,0.25,0.25)
maze_hard = cm.create_maze(10,10,0.40,0.2)
maze_extreme = cm.create_maze(30,30,0.6,0.75)
maze = maze_easy

#TODO:: THIS IS COMPLETELY ARBITRARY!!
start = [0,0]
start2 = [4,0]
end = [2,2]

class MultiAgent:
    def __init__(self,starting):
        self.c_c = starting
        self.seen = set()
        self.move_counter = 1
        self.early_stop = 0
        self.stopped = False
    def update(self,n_c):
        self.c_c[0] = n_c[0]
        self.c_c[1] = n_c[1]

mazePrint(maze,end,start2)
#Heuristic/fitness function. Input is individual (can treat like a list)
#output is score, Note: the comma is important
def evalOneMax(individual):
    print(individual)
    return sum(individual),

def evalMaze(inds, verbose = False):
    penalty = 0
    agents = []
    test = MultiAgent([0,0])
    test1= MultiAgent([0,4])
    agents.append(test)
    agents.append(test1)
    path_len = 0

    for i in range(MAX_MOVES):
        path_len+=1
        for x in range(NUM_AGENTS):
            ind = inds[x]
            a = agents[x]
            n_c = [0,0]
            n_c[0] = a.c_c[0]
            n_c[1] = a.c_c[1]
            a.seen.add((a.c_c[0],a.c_c[1]))
            if(a.stopped == False):
                if ind[i] == 1:
                    n_c[0] = n_c[0] - 1
                    if verbose:
                        print(str(x) + " moving up " + str(a.c_c) + " to " + str(n_c))
                elif (ind[i] == 2):
                    n_c[1] = n_c[1] + 1
                    if verbose:
                        print(str(x) + " moving right " + str(a.c_c) + " to " + str(n_c))
                elif (ind[i] == 3):
                    n_c[0] = n_c[0] + 1
                    if verbose:
                        print(str(x) + " moving down " + str(a.c_c) + " to " + str(n_c))
                elif (ind[i] == 4):
                    n_c[1] = n_c[1] - 1
                    if verbose:
                        print(str(x) + " moving left " + str(a.c_c) + " to " + str(n_c))
                else:
                    if verbose:
                        print(str(x) + " waiting at " + str(a.c_c))
                a.move_counter += 1
                if (n_c[0] >= len(maze) or n_c[1] >= len(maze[0]) or n_c[0] < 0 or n_c[1] < 0):
                    if verbose:
                        print("OUT OF BOUNDS")
                    penalty+=2

                elif(maze[n_c[0]][n_c[1]] == False):
                    if verbose:
                        print("INVALID MOVE")
                    penalty+=2
                else:
                    a.update(n_c)
                    if((n_c[0],n_c[1]) in a.seen and ind[i] != 0):
                        if verbose: print("seen")
                        penalty+=1
                    if(n_c == end):
                        a.early_stop = i+1
                        a.stopped = True
                        if verbose:
                            print(str(x) + " Reached Goal!!")
                        break
        #ONlY TWO FOR NOW
        if(agents[0].c_c == agents[1].c_c and agents[0].c_c != [0,0] and agents[0].c_c != end):
            if verbose:
                print("COLLISSION")
            distance = math.sqrt((end[0]-agents[0].c_c[0])**2 + (end[1]-agents[0].c_c[1])**2) + math.sqrt((end[0]-agents[1].c_c[0])**2 + (end[1]-agents[1].c_c[1])**2)
            path_length = agents[0].move_counter + agents[1].move_counter
            return distance + penalty - path_length/2 + 50,


    #calculate distance from goal
    distance1 = math.sqrt((end[0]-agents[0].c_c[0])**2 + (end[1]-agents[0].c_c[1])**2)
    distance2 = math.sqrt((end[0]-agents[1].c_c[0])**2 + (end[1]-agents[1].c_c[1])**2)
    distance = distance1 + distance2
    bonus = 0
    if distance1 == 0:
        bonus = MAX_MOVES-agents[0].early_stop + 100
    if distance2 == 0:
        bonus = MAX_MOVES-agents[1].early_stop + 100
    if distance1 == 0 and distance2 == 0:
        bonus = MAX_MOVES-agents[0].early_stop +  MAX_MOVES-agents[1].early_stop + 1000
    if verbose:
        print("distance to goal:" + str(distance))
        print("penalty:" + str(penalty))
        print(path_len)
    return distance + penalty - bonus,


creator.create("FitnessMax", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
toolbox.register("attr_dir", random.randint, 1, 4)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_dir, MAX_MOVES)
toolbox.register("species", tools.initRepeat, list, toolbox.individual, 100)

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
best = [random.choice(species[i]) for i in range(NUM_AGENTS)]
species_index = list(range(NUM_AGENTS))
g = 1
ngen = 200

while g < ngen:
    print(str(g) + ": " + str(len(species[0])))
        # Initialize a container for the next generation representatives
    next_repr = [None] * len(species)
    for (i, s), j in zip(enumerate(species), species_index):
        # Vary the species individuals
        s = algorithms.varAnd(s, toolbox, 0.5,0.25)

        # Get the representatives excluding the current species
        r = representatives[:i] + representatives[i+1:]
        for ind in s:
            # Evaluate and set the individual fitness
            ind.fitness.values = toolbox.evaluate([ind] + r)
        # Select the individuals
        species[i] = toolbox.select(s, len(s))  # Tournament selection
        next_repr[i] = toolbox.get_best(s)[0]   # Best selection

    representatives = next_repr

    g+=1

print(next_repr)
print(next_repr[0].fitness.values)
print(next_repr[1].fitness.values)
print (evalMaze(best, verbose = True))
