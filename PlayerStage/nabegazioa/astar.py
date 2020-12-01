#!/usr/bin/env python3
# -*- coding: utf-8 -*-
delta_signs = ['→','←',  '↓', '↑',  '↘', '↙', '↗', '↖']
# [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)] left, right, up, down, upleft, upright, downleft, downright 
#delta_signs = ['↓', '←','→','↑',  '↖', '↗', '↙', '↘']

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
    def __init__(self, mazex, mazey):
        print("Initializing pointer 2d array of size {:d}x{:d}".format(mazex, mazey))
        self.rows = mazey
        self.cols = mazex
        # Pointers are None (o) until assigned
        self.maze = [['o' for j in range(mazey)] for j in range(mazex)]
        print(self.maze)

    def fill(self, node):
        print("Filling node")
        self.maze[node.position[0]][node.position[1]] = node.delta
        
    def draw(self):
        for i in range(self.cols):
            for j in range(self.rows):            
                print("{:1}".format(self.maze[i][j]), end= " ")
            print("")
            


        

def printNodeList(node_list):
    for node in node_list:
        node.printNode()
    #print("----  List length: ", len(node_list))
    
def astar(maze, start, end):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []
    mp = MazePath(len(maze), len(maze[0]))
    mp.maze[start[0]][start[1]] = 's'
    mp.maze[end[0]][end[1]] = 'g'

    # Add the start node
    open_list.append(start_node)
    # Loop until you find the end
    while len(open_list) > 0:
        print("--- Find the best node ----------")
        current_node = open_list[0]
        current_index = 0
        index = 0
        for item in open_list:            
            if item.f < current_node.f:
                current_node = item
                current_index = index            
            index += 1
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
            total_cost = current.g
            print("Goal reached. Calculating path...")
            while current is not None:
                print("Node ({:d}, {:d})".format(current.position[0], current.position[1]), end=' ')
                print("g: {:f} h: {:f} f: {:f}".format(current.g, current.h, current.f))
                path.append(current.position)
                current = current.parent
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
            node_position[0] = current_node[0] + new_position[0]
            node_position[1] = current_node[1] + new_position[1]
            
            # Make sure position is within maze range
            if node_position[0] < 0 or node_position[0] > len(maze[0])-1 or node_position[1] < 0 or node_position[1] > len(maze)-1:
                continue
            
            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] == 1:
                continue

            # Create new node and append it to children list
            new_node = Node(current_node, node_position)
            new_node.delta = delta_signs[delta_index]
            children.append(new_node)
            
        # Loop through children
        print("         Children list:")
        printNodeList(children)
        print("         ------------------------------")
        for child in children:
            found_in_closed = False

            # Child is on the closed list?
            print("          child ({:d},{:d}) in closed_list?".format(child.position[0], child.position[1]))
            # TODO
            # for closed_child in closed_list:
            # if child == closed_child: ???
            if found_in_closed: continue
            print("          No!")
            print("          -------------------")

            # TODO
            # calculate new cost
            # Create the f, g, and h values

            # ???????
            # Child is already in the open list
            print("          child ({:d},{:d}) in open_list?".format(child.position[0], child.position[1]))
            found_in_open = False

            for open_node in open_list:
                if child == open_node:
                    found_in_open = True
                    print("          Yes!--> analyze g function: {:f} >{:f}".format(child.g, open_node.g))
                # TODO ...
                
            # Add the child to the open list
            if not found_in_open:
                print("          No!--> append child to open_list")
                mp.fill(child)
                open_list.append(child)
        print("Open List:")
        printNodeList(open_list)
        print("Closed List:")
        printNodeList(closed_list)
        mp.draw()
        print("------------------------------")
    if len(open_list) == 0:
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

    # maze = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    #         [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0],
    #         [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0],
    #         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0],
    #         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #         [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #         [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #         [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #         [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
    #         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #         [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #         [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

    # start = (12, 11)
    # end = (1, 24)


    maze = [[1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0],
            [1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0],
            [1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0]]

    start = (0, 13)
    end = (9, 13)

    path = astar(maze, start, end)
    print(path)

if __name__ == '__main__':
    main()
