# -*- coding: utf-8 -*-
"""
Created on Tue Oct  9 10:49:16 2018

@author: iakov
"""
import numpy as np
import networkx as nx


class Agent:
    def __init__(self,current_position,coordinates,coord_dict,goal_node):
        self.current_position = current_position
        self.coordinates = coordinates
        self.coord_dict = coord_dict
        self.invalid_counter = 0
        self.goal_node = goal_node
    
    def plan_eval(self):
        return -self.invalid_counter
    
    def move(self,direction,graph):
        next_coords = np.array(self.coordinates)
#        print next_coords
        if(direction=='up'):
            next_coords[1] = next_coords[1] + 1
        elif (direction=='down'):
            next_coords[1] = next_coords[1] - 1
        elif (direction=='right'):
            next_coords[0] = next_coords[0] + 1
        elif (direction=='left'):
            next_coords[0] = next_coords[0] - 1
        new_coords = (next_coords[0],next_coords[1])
#        print self.coordinates
#        print new_coords
        for id, coords in self.coord_dict.items():
            if coords == new_coords:
                next_position = id
                self.coordinates = new_coords
                graph.nodes()[self.current_position]['position'] = False
                graph.nodes()[next_position]['position'] = True
                return                

        print "INVALID MOVE"
        self.invalid_counter += 1
        return

    def execute_plan(self,plan,graph):
        for step in plan:
            print step
            self.move(step,graph)
        return self.plan_eval()




