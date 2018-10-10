# -*- coding: utf-8 -*-
"""
Created on Tue Oct  9 10:53:07 2018

@author: iakov
"""

from create_maze_graph import create_maze_graph
import graph_movement
import numpy
from numpy.random import randint as randint
import matplotlib.pyplot as plt
from random import choice

import networkx as nx

def print_maze(maze,coordinates):
    plt.figure()
    color_map = []
    for node in maze.nodes():
        if maze.nodes()[node]['position'] == True:
            color_map.append('blue')
        elif maze.nodes()[node]['goal'] == True:
            color_map.append('green')
        else:
            color_map.append('red')


    nx.draw(maze,coordinates, node_color=color_map)



maze, coord_dict, coordinates = create_maze_graph()

starting_node = randint(0,maze.size()+1)
goal_node = randint(0,maze.size()+1)

maze.nodes()[starting_node]['position'] = True
maze.nodes()[goal_node]['goal'] = True


agent = graph_movement.Agent(starting_node,maze.nodes()[starting_node]['coordinates'],coord_dict,goal_node)
print_maze(maze,coordinates)
print(agent.coordinates)
plan =["right","up","right","right","down","right","down"]
agent.execute_plan(plan,maze)
print(agent.coordinates)

print_maze(maze,coordinates)

print(agent.invalid_counter)


#print maze.edges
