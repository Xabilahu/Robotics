#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math, time, random
import numpy as np

delta_signs = ['→','←', '↓', '↑', '↘', '↙', '↗', '↖']
# [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)] left, right, up, down, upleft, upright, downleft, downright 
#delta_signs = ['↓', '←','→','↑',  '↖', '↗', '↙', '↘']

#Code from: https://code.activestate.com/recipes/578356-random-maze-generator/
def gen_maze(mx, my):
    maze = [[0 for x in range(mx)] for y in range(my)]
    dx = [0, 1, 0, -1]; dy = [-1, 0, 1, 0] # 4 directions to move in the maze
    # start the maze from a random cell
    start = (random.randint(0, mx - 1), random.randint(0, my - 1))
    stack = [start]

    while len(stack) > 0:
        (cx, cy) = stack[-1]
        maze[cy][cx] = 1
        # find a new cell to add
        nlst = [] # list of available neighbors
        for i in range(4):
            nx = cx + dx[i]; ny = cy + dy[i]
            if nx >= 0 and nx < mx and ny >= 0 and ny < my:
                if maze[ny][nx] == 0:
                    # of occupied neighbors must be 1
                    ctr = 0
                    for j in range(4):
                        ex = nx + dx[j]; ey = ny + dy[j]
                        if ex >= 0 and ex < mx and ey >= 0 and ey < my:
                            if maze[ey][ex] == 1: ctr += 1
                    if ctr == 1: nlst.append(i)
        # if 1 or more neighbors available then randomly select one and move
        if len(nlst) > 0:
            ir = nlst[random.randint(0, len(nlst) - 1)]
            cx += dx[ir]; cy += dy[ir]
            stack.append((cx, cy))
        else: stack.pop()

    return np.abs(np.array(maze) - 1).tolist()

# Tries to find start and end positions as opposed as possible in the maze
def find_valid_positions(maze):
    start = None
    end = None

    for i in range(len(maze)):
        for j in range(len(maze)):
            if maze[i][j] == 0:
                start = (i, j)
                break
        if start is not None:
            break
    
    for i in reversed(range(len(maze))):
        for j in reversed(range(len(maze))):
            if maze[i][j] == 0:
                end = (i, j)
                break
        if end is not None:
            break

    return start, end

class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0
        # sign of the pointer for drawing purposes
        self.delta = "o"
        
    def __eq__(self, other):
        return self.position == other.position

    # def __repr__(self):
    #     return self.position
    
    def printNode(self):
        print("({:d}, {:d})[g={:f} + h={:f} = {:f}], delta: {}".format(self.position[0], self.position[1], self.g, self.h, self.f, self.delta, end=''))

        
class MazePath():
    """ A class for recovering the path after astar stops"""
    def __init__(self, mazex, mazey, verbose=1):
        print("Initializing pointer 2d array of size {:d}x{:d}".format(mazex, mazey))
        self.rows = mazey
        self.cols = mazex
        # Pointers are None (o) until assigned
        self.maze = [['o' for j in range(mazey)] for j in range(mazex)]
        self.verbose = verbose
        
        if self.verbose == 1:
            print(self.maze)

    def fill(self, node):
        if self.verbose == 1:
            print("Filling node")
        self.maze[node.position[0]][node.position[1]] = node.delta
        
    def draw(self, start=None, end=None):
        for i in range(self.cols):
            for j in range(self.rows):  
                if start is not None and start[0] == i and start[1] == j:
                    print("s".format(self.maze[i][j]), end= " ")
                elif end is not None and end[0] == i and end[1] == j:
                    print("e".format(self.maze[i][j]), end= " ")
                else:
                    print("{:1}".format(self.maze[i][j]), end= " ")
            print("")    

def printNodeList(node_list):
    for node in node_list:
        node.printNode()
    #print("----  List length: ", len(node_list))
    
def astar(maze, start, end, verbose=1):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []
    mp = MazePath(len(maze), len(maze[0]), verbose=verbose)
    mp.maze[start[0]][start[1]] = 's'
    mp.maze[end[0]][end[1]] = 'g'

    # Add the start node
    open_list.append(start_node)
    # Loop until you find the end
    while len(open_list) > 0:
        if verbose == 1:
            print("--- Find the best node ----------")
        current_node = open_list[0]
        current_index = 0
        index = 0
        for item in open_list:            
            if item.f < current_node.f:
                current_node = item
                current_index = index            
            index += 1
        if verbose == 1:
            current_node.printNode()
            print("Node index: ", current_index)
            print("------------------------------")
        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)
        # print("Open List after best node pop:")
        # printNodeList(open_list)

        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            current_node.delta = 'g'
            total_cost = current.g
            if verbose == 1:
                print("Goal reached. Calculating path...")
            while current is not None:
                if verbose == 1:
                    print("Node ({:d}, {:d})".format(current.position[0], current.position[1]), end=' ')
                    print("g: {:f} h: {:f} f: {:f}".format(current.g, current.h, current.f))
                path.append(current.position)
                current = current.parent
            if verbose == 1:
                print("Total cost: {:f}".format(total_cost))
                mp.draw()
            return path[::-1] # Return reversed path
           
        # Generate children
        children = []
        delta_index = -1
        # Adjacent squares
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: 

            delta_index += 1
            # Get node position
            node_position = (current_node.position[0] + new_position[0],current_node.position[1] + new_position[1])
            
            # Make sure position is within maze range
            if (node_position[0] < 0 or node_position[0] >= len(maze) or node_position[1] < 0 or node_position[1] >= len(maze[0])):
                continue
            
            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] == 1:
                continue

            # Create new node and append it to children list
            new_node = Node(current_node, node_position)
            new_node.delta = delta_signs[delta_index]
            new_node.g = current_node.g
            new_node.g += 1.4 if new_node.delta in delta_signs[4:] else 1
            new_node.h = math.sqrt((end_node.position[0] - new_node.position[0]) ** 2 + (end_node.position[1] - new_node.position[1]) ** 2)
            new_node.f = new_node.g + new_node.h
            children.append(new_node)
            
        # Loop through children
        if verbose == 1:
            print("         Children list:")
            printNodeList(children)
            print("         ------------------------------")
        for child in children:
            found_in_closed = False

            # Child is on the closed list?
            if verbose == 1:
                print("          child ({:d},{:d}) in closed_list?".format(child.position[0], child.position[1]))
            # TODO
            found_in_closed = child in closed_list
            if found_in_closed: 
                continue

            # TODO
            # calculate new cost
            # Create the f, g, and h values

            current_step = 1.4 if child.delta in delta_signs[4:] else 1
            c_g = current_node.g + current_step

            # Child is already in the open list
            if verbose == 1:
                print("          child ({:d},{:d}) in open_list?".format(child.position[0], child.position[1]))
            found_in_open = False

            for open_node in open_list:
                if child == open_node:
                    found_in_open = True
                    if verbose == 1:
                        print("          Yes!--> analyze g function: {:f} >{:f}".format(child.g, open_node.g))
                    if open_node.g > child.g:
                        open_node.g = c_g
                        open_node.h = math.sqrt((end_node.position[0] - child.position[0]) ** 2 + (end_node.position[1] - child.position[1]) ** 2)
                        open_node.f = open_node.g + open_node.h
                        open_node.delta = child.delta
                        break
                        
                
            # Add the child to the open list
            if not found_in_open:
                if verbose == 1:
                    print("          No!--> append child to open_list")
                    mp.fill(child)
                open_list.append(child)
        if verbose == 1:
            print("Open List:")
            printNodeList(open_list)
            print("Closed List:")
            printNodeList(closed_list)
            mp.draw()
            print("------------------------------")
    if len(open_list) == 0:
        if verbose == 1:
            print("Failed!")

def main():

    # maze = [[0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 1, 0, 0, 0, 0, 0]]

    # start = (0, 0)
    # end = (7, 6)

    
    # maze = [[0, 0, 1, 0, 0, 0],
    #         [0, 0, 0, 0, 0, 0],
    #         [0, 1, 1, 0, 0, 0],
    #         [0, 0, 1, 1, 0, 0],
    #         [0, 0, 0, 0, 0, 0]]

    # start = (0, 5)
    # end = (3, 1)

    # maze = [[0, 0, 0, 0, 0],
    #         [0, 0, 1, 0, 0],
    #         [1, 0, 1, 1, 0],
    #         [0, 0, 0, 1, 0],
    #         [0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 0]]

    # start = (0, 0)
    # end = (5,3)

    maze = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0],
            [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

    start = (12, 11)
    end = (1, 24)

    # maze = [[1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0],
    #         [1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0],
    #         [1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #         [1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #         [1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #         [1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #         [0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0]]

    # start = (0, 13)
    # end = (9, 13)

    path = astar(maze, start, end)
    print(path)
    print()

    MazePath(len(maze), len(maze[0])).draw(start=start, end=end)

    # maze = gen_maze(175, 175)
    # start, end = find_valid_positions(maze)

    # total = 0
    # for i in range(20):
    #     st = time.time()
    #     path = astar(maze, start, end, verbose=0)
    #     nd = time.time()
    #     total += nd-st
    # print(path)
    # print("Elapsed time: {} seconds.".format(total / 20.))


if __name__ == '__main__':
    main()
