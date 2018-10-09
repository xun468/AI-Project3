# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

#import sys
import numpy
from numpy.random import random_integers as randint
import matplotlib.pyplot as pyplot

import networkx as nx



# Code copied from Wikipedia
# Creates a 2d binary array. 1/True is a wall, 0/False is an empty time.
def create_maze(width, height, complexity, density):
    # Only odd shapes
    shape = ((height // 2) * 2 + 1, (width // 2) * 2 + 1)
    # Adjust complexity and density relative to maze size
    complexity = int(complexity * (5 * (shape[0] + shape[1]))) # number of components
    density    = int(density * ((shape[0] // 2) * (shape[1] // 2))) # size of components
    # Build actual maze
    Z = numpy.zeros(shape, dtype=bool)
    # Fill borders
    Z[0, :] = Z[-1, :] = 1
    Z[:, 0] = Z[:, -1] = 1
    # Make aisles
    for i in range(density):
        x, y = randint(0, shape[1] // 2) * 2, randint(0, shape[0] // 2) * 2 # pick a random position
        Z[y, x] = 1
        for j in range(complexity):
            neighbours = []
            if x > 1:             neighbours.append((y, x - 2))
            if x < shape[1] - 2:  neighbours.append((y, x + 2))
            if y > 1:             neighbours.append((y - 2, x))
            if y < shape[0] - 2:  neighbours.append((y + 2, x))
            if len(neighbours):
                y_,x_ = neighbours[randint(0, len(neighbours) - 1)]
                if Z[y_, x_] == 0:
                    Z[y_, x_] = 1
                    Z[y_ + (y - y_) // 2, x_ + (x - x_) // 2] = 1
                    x, y = x_, y_
    return Z


## Takes Z from create_maze as input
## Returns the adjacency matrix of the maze (which we use to create the graph)
## as well as the coordinates of each point (for easier printing of the graph)
def maze_to_graph(maze):
    maze_size = 0
    for i in range(1,maze.shape[0]-1):
        for j in range(1,maze.shape[1]-1):
            if maze[i,j] == 0:
                maze_size = maze_size + 1
                
    adjacency_matrix = numpy.zeros([maze_size,maze_size], dtype=int)
    
    i_counter = 0
    coordinates = []
    previous_row = numpy.zeros([maze.shape[1]])

    for i in range(1,maze.shape[0]-1):
        for j in range(1,maze.shape[1]-1):
            if maze[i,j] == 0:
                coordinates.append((j,int(maze.shape[0]-i)))
                if(maze[i,j-1]==0):
                    adjacency_matrix[i_counter,i_counter-1] = 1
                if(maze[i-1,j]==0):
                    adjacency_matrix[i_counter,int(previous_row[j])] = 1                    
                previous_row[j] = i_counter
                i_counter = i_counter + 1

#    print coordinates
    return adjacency_matrix, coordinates
                    

## Use width,height,complexity and density to customize the layout of
## the maze to our liking.

def create_maze_graph():
    width = 21
    height = 21
    complexity = 0.75
    density = 0.75
    maze = create_maze(width,height,complexity,density)
    #pyplot.figure(figsize=(10, 5))
    #pyplot.imshow(maze, cmap=pyplot.cm.binary, interpolation='nearest')
    #pyplot.xticks([]), pyplot.yticks([])
    #pyplot.show()
    
    maze, coordinates = maze_to_graph(maze)
    
    maze_graph = nx.from_numpy_matrix(maze)
    nodes = maze_graph.nodes()
#    coordinates = numpy.array(coordinates)
    coord_dict = dict(zip(nodes,coordinates))
#    print coord_dict
    nx.set_node_attributes(maze_graph,coord_dict,'coordinates')
    nx.set_node_attributes(maze_graph,False,'position')
    nx.set_node_attributes(maze_graph,False,'travelled')
    nx.set_node_attributes(maze_graph,False,'goal')

#    nx.draw(maze_graph,coordinates)
    return maze_graph, coord_dict, coordinates
