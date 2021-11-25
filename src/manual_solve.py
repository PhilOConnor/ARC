#!/usr/bin/python

import os, sys
import json
import numpy as np
import re

### YOUR CODE HERE: write at least three functions which solve
### specific tasks by transforming the input x and returning the
### result. Name them according to the task ID as in the three
### examples below. Delete the three examples. The tasks you choose
### must be in the data/training directory, not data/evaluation.
"""
Name           : Philip O Connor
Student Number : 21249304
Tasks          : d4f3cd78, 2dd70a9a, 83302e8f
GitHub link    : https://github.com/PhilOConnor/ARC

All three tasks are solved for training and test cases.

The three tasks below were solved mostly using base python, with numpy for arrays, to find 
elements in arrays and to compute the action for state-action pairs. Numpy being as powerful
as it is, I dont think it was utiliesd fully, but I'm not sure I could have used vectorising or matrix operations as my solutions were,
for the most part one a cell by cell level, but there are probably more efficient ways of taking the same actions I took.
My solutions required quite a bit of iterating, if these tasks grew, they could become very cumbersome an the number of elements in the array increases.


The random module was also used in the second and third task to reduce the amount of conditions
hard coded, I could randomly move about when needed and iterate until a solution was found. Itertools was used to help tidy up the loop in task 3
as the loop had 3 values to unpack.
In task 2, the number of random iterations could have been reduced if I had been able to store the
actions per iteration and prevent them from reoccurring, but I was not able to think through this so the number of
iterations is pretty high to make sure a path to the end point is found. Task 3 took two loops to make sure it was 
successful as the script would sometimes paint itself into a corner and miss the rest of the cells it needed to pass through.

Task 1 I thought of an an object detection problem - Find the box, fill it, then find the opening and fill the cells in that direction.
The tasks 2 & 3 were solved with mostly a similar approach, find a start point, determine a 
direction to go in, when the state needs to be changed, take an action and repeat until the goal is reached.
Task 2 was similar to a simplified Darpa grand challenge and an FSM was used in Boss to keep track of the cars 
current state - ['How Smart Mahcines Think', Sean Gerrish] - so it would also work for this task. As it worked so well
I used another one for task 3.  


"""
def solve_d4f3cd78(x):
    """
    Goal - Fill in the box and continue filling in cells in the direction of the opening in the box - Object detection.
    Solution - 
        1) Locate the box - this was done by scanning from the top and bottom for the boundary. Once found fill all the cells inside the boundary with value 8
        2) Locate the opening - With the boundary located, and center filled, only one cell will have a 0 - this must be the opening.
        3) Determine orientation - What direction is 'into space', slice the array and fill it in the correct direction.
    Success - All training and test arrays pass
    """
    # Iterate through the grid to find the top and bottom lines (have value of 5) and the box they enclose
    for i in range(x.shape[0]):
        top_line = np.where(x[i]==5)

        # Find the top line
        if len(top_line[0])>0:
            #print(i, top_line[0])
            break
    
    # to find the bottom line start at the bottom grid and work upwards
    for j in range(x.shape[0]-1,0,-1):
        bottom_line = np.where(x[j]==5)
        # Find the bottom line
        if len(bottom_line[0])>0:
            #print(j, bottom_line[0])
            break
    
    # Fill the contents of this grid with the 8 value
    for k in range(i+1, j):
        line = x[k]
        line[top_line[0][1]: top_line[0][-1]]=8

        
    # Create a grid in local space and identify the opening
    grid = x[i:j+1, top_line[0][0]: top_line[0][-1]+1]
    opening_local = np.argwhere(grid == 0)
    
    # Give the local opening a value not found anywhere in ARC so we can use this value to locate it in the global grid regardless of boundary colour in future
    grid[opening_local[0][0],opening_local[0][1]]=10

    # Find the opening in the global space and give it a value 8 now it's been correctly located
    opening_global = [np.where(x==10)[0][0], np.where(x==10)[1][0]]
    x[opening_global[0] ,opening_global[1]] =8
    # Find out which direction is into open space, once  found slice the array to give the remaining cells in that direction and assign 8 to these cells.
    for i in range(4):
        # North facing opening
        if x[opening_global[0] -1,opening_global[1]] == 0:
            x[0:opening_global[0] ,opening_global[1]] = 8
            #print("North facing")

            # South facing opening
        elif x[opening_global[0] +1,opening_global[1]] == 0:
            x[opening_global[0]: ,opening_global[1]] =8
            #print("South facing")

            # East facing opening
        elif x[opening_global[0] ,opening_global[1]+1] == 0:
            x[opening_global[0] ,opening_global[1]:] = 8
            #print("East facing")

            # West facing opening
        elif x[opening_global[0] ,opening_global[1]-1] == 0:
            x[opening_global[0] ,:opening_global[1]] =8
            #print("West facing")
    return x

def solve_2dd70a9a(x):
    """
    Goal - Find a route between a start and end point, when the next cell is an 8, change direction perpendicular to the current direction of travel - Finite state machine.
    Solution -
     1) Find and determine the orientation of start and end points.
     2) Set up a state-action dictionary defining the next action depending on the contents of the next cell (continue or change direction)
     3) Take the step in that direction and iterate, if this path leads to the end point, return it. 
        If the explorer gets 'stuck' and does not move for an iteration, reset to the initial conditions.
    Success - All training and test arrays pass
    """

    import random
    x_ = x.copy()
    # State action pairs - this modifies the current position depending on the current direction of travel
    

    # Locate the start and end points
    start_point = np.argwhere(x ==3)
    end_point = np.argwhere(x ==2)

    # Define the environment boundary - will be used to keep the explorer 'in bounds'
    y_range, x_range = x.shape

    def orientation(start_point, end_point):
        """
        Get general orientation of the start points - the end points also have the same orientation
        """
        # If 0th element of each start point is different then the points are not on the same line... therefore muse be N/S orientation
        if start_point[0][0] != start_point[1][0]:
            orientation='NS'
            # Now find out if the starting position is north or south facing
            # If the start point has a higher 0th element value, it is further down the page -> End point is above it so must travel north.
            if start_point[0][0] > end_point[0][0]:
                direction = 'north'
                initial_position = [start_point[0][0], start_point[0][1]]          
            elif start_point[0][0] < end_point[0][0]:
                direction = 'south'
                initial_position = [start_point[1][0], start_point[1][1]]

        # If not North/South facing then it must be East/West
        elif start_point[0][1] != start_point[1][1]:
            orientation='EW'
            # If the start point is further right than the finish then we must go towards the west
            if start_point[0][1] > end_point[0][1]:
                direction = 'west'
                initial_position = [start_point[0][0], start_point[0][1]]
            elif start_point[0][1] < end_point[0][1]:
                direction = 'east'
                initial_position = [start_point[1][0], start_point[1][1]]

            # If the start and end points are aligned, go in the direction of more space
            elif start_point[0][1] == end_point[0][1]:
                if start_point[0][1]>x_range/2:
                    direction = 'west'
                    initial_position = [start_point[0][0], start_point[0][1]]
                else: 
                    direction = 'east'
                    initial_position = [start_point[1][0], start_point[1][1]]
        return direction, initial_position

    direction, initial_position = orientation(start_point, end_point)

    # Define the actions for each state
    state_action = {'north':(1, 0), 'south':(-1, 0), 'east': (0, -1), 'west':(0, 1)}
    # Before iterating, set up the current position as the start point
    current_position = initial_position.copy() 
    # This can take a lot of iterations to solve - I tried looking at something like a decision tree - so steps werent repeated but couldnt figure it out.
    for i in range(1000):
        # Take the current position - if pos1 == pos2 at the end then it's stuck in a corner and needs to be reset to the initial conditions.
        pos1 = current_position
        # If the current position is on the boundary, reset to the initial conditions to avoid falling off the edge of the world
        if current_position[0] == 0 or current_position[0] == y_range-1 or current_position[1] == 0 or current_position[1] == x_range-1:
            direction, initial_position = orientation(start_point, end_point)
            current_position = initial_position
            x_ = x.copy()
        else:
            pass

        # If the next step has the value 2 to show an end point, print the grid and stop the program
        if x_[np.subtract(current_position,  state_action[direction])[0],np.subtract(current_position,  state_action[direction])[1]] == 2:
            #print(x)
            success='yes'
            break
        else:
            pass
        # If the next gridspace is a 0, take the appropriate move according to the state-action dictionary and update cell value and the current position
        if x_[np.subtract(current_position,  state_action[direction])[0],np.subtract(current_position,  state_action[direction])[1]] ==0:
            current_position = np.subtract(current_position,  state_action[direction])[0],np.subtract(current_position,  state_action[direction])[1]
            x_[current_position] = 3
            pos2 = current_position
            #print(f'Initial point {initial_position}. Direction: {direction}. Current position: {current_position}')
            
        # If the next grid space is an 8, take a random direction depending on the current state of the system.
        
        elif x_[np.subtract(current_position,  state_action[direction])[0],np.subtract(current_position,  state_action[direction])[1]] == 8:

            if (direction == 'east') or (direction == 'west'):
                direction = random.choice(["north", "south"])
            

            elif (direction == 'north') or (direction == 'south'):
                direction = random.choice(["east", "west"])
        # If there is any situation that is not caught in the above, reset to the initial conditions
        else:
            direction, initial_position = orientation(start_point, end_point)
            current_position = initial_position
            x_ = x.copy()
            
    return x_

    
def solve_83302e8f(x):
    """
    Goal - if areas are connected by a hole in the wall, colour them yellow, if the walls surrounding them are unbroken, they are green - finite state machine and object detection.
    Solution -
        1) Find locations for the holes in the walls and 'seed' them with a yellow cell.
        2) Set up permitted directions of travel
        3) Evaluate at each gap, the every cell and direction availble - if the next cell is blank, make it yellow and move onto the next iteration
        4) Iterate through 3 as the number of 'gaps' increases (gaps are yellows, a carry over from the initial problem statement) so yellows propogate through the allowed cells.
        5) Any cells remaining blank must be surrounded by a solid wall, so they can be made green now.
    Success - All training and test arrays pass
    """
    x_ = x.copy()
    import itertools

    # Create an array of gaps in walls - these will be used to 'seed' the yellows to make sure they propogate through the walls.
    gaps = np.empty((0,2), int)
    # find out how regular the walls are, the test space is square and walls are regularly spaced so only need to check one direction
    spacing = np.argwhere(x_[0]!=0)
    # Find the holes in the walls, first on the N/S running walls, then on the E/W running walls
    for row, i in itertools.product(range(len(x_)), spacing):
        if x_[row][i][0] ==0:
            #print(row, i[0], x[row][i][0], "vertical")
            gap = np.array([row, i[0]])
            gaps = np.concatenate((gaps,[gap]))

        elif x[i][0][row] ==0:
            #print(i[0], row, x[i][0][row], "horizontal")
            gap = np.array([i[0], row])
            gaps = np.concatenate((gaps,[gap]))
    
    # Where there are gaps, make it yellow/4
    for gap in gaps:
        x_[gap[0], gap[1]] = 4
    
    # Create the directions of travel for our explorer - N/S/E/W
    directions =[[1, 0],
                 [-1, 0],
                 [0, 1],
                 [0, -1]]
    # It takes a couple of runs to allow the 4s to propogate through the available space - the array of yellow cells needs to be updated after a while to get remaining ones in corners
    for run in ['run_1', 'run_2', 'run_3']:
        # Now iterate for every grid space, gap and direction
        for i, gap, direction in itertools.product(range(len(x)**2), gaps, directions):
            # Seed the current position at a gap in the wall
            current_pos = gap
            # Some movements are illegal, break out of the loop and move onto the next gap (move outside the array)
            try:
                # While, for a given grid space, if the next step in a given direction is into a blank space do...
                while x_[np.subtract(current_pos[0], direction[0]), np.subtract(current_pos[1], direction[1])] == 0 :
                    # If the next step would take our explorer off the edge of the earth, stop and move onto the next gap. No time for adventures/monsters here
                    if (np.subtract(current_pos[0], direction[0]) < 0 ) or (np.subtract(current_pos[1], direction[1]) < 0) :
                        break
                    elif (np.subtract(current_pos[0], direction[0]) >= len(x)) | (np.subtract(current_pos[1], direction[1]) >= len(x)) :
                        break
                    # If the next step wont be detrimental to our explorers health, re-assign the cell value to a 4 and update the current position for the next iteration
                    else:
                        x_[np.subtract(current_pos[0], direction[0]), np.subtract(current_pos[1], direction[1])] = 4
                        current_pos = np.subtract(current_pos[0], direction[0]), np.subtract(current_pos[1], direction[1])

            except:
                pass
        # Update our gaps array with all the cells marked 4 and loop through again - this will catch any cells we havent reached 
        # yet in case the explorer has painted itself into a corner
        gaps = np.argwhere(x_==4)
    
    # Finally, any remaining 0s need to be assigned to 3s.
    x_[x_==0] = 3
    return x_

def main():
    # Find all the functions defined in this file whose names are
    # like solve_abcd1234(), and run them.

    # regex to match solve_* functions and extract task IDs
    p = r"solve_([a-f0-9]{8})" 
    tasks_solvers = []
    # globals() gives a dict containing all global names (variables
    # and functions), as name: value pairs.
    for name in globals(): 
        m = re.match(p, name)
        if m:
            # if the name fits the pattern eg solve_abcd1234
            ID = m.group(1) # just the task ID
            solve_fn = globals()[name] # the fn itself
            tasks_solvers.append((ID, solve_fn))

    for ID, solve_fn in tasks_solvers:
        # for each task, read the data and call test()
        directory = os.path.join("..", "data", "training")
        json_filename = os.path.join(directory, ID + ".json")
        data = read_ARC_JSON(json_filename)
        test(ID, solve_fn, data)
    
def read_ARC_JSON(filepath):
    """Given a filepath, read in the ARC task data which is in JSON
    format. Extract the train/test input/output pairs of
    grids. Convert each grid to np.array and return train_input,
    train_output, test_input, test_output."""
    
    # Open the JSON file and load it 
    data = json.load(open(filepath))

    # Extract the train/test input/output grids. Each grid will be a
    # list of lists of ints. We convert to Numpy.
    train_input = [np.array(data['train'][i]['input']) for i in range(len(data['train']))]
    train_output = [np.array(data['train'][i]['output']) for i in range(len(data['train']))]
    test_input = [np.array(data['test'][i]['input']) for i in range(len(data['test']))]
    test_output = [np.array(data['test'][i]['output']) for i in range(len(data['test']))]

    return (train_input, train_output, test_input, test_output)


def test(taskID, solve, data):
    """Given a task ID, call the given solve() function on every
    example in the task data."""
    print(taskID)
    train_input, train_output, test_input, test_output = data
    print("Training grids")
    for x, y in zip(train_input, train_output):
        yhat = solve(x)
        show_result(x, y, yhat)
    print("Test grids")
    for x, y in zip(test_input, test_output):
        yhat = solve(x)
        show_result(x, y, yhat)

        
def show_result(x, y, yhat):
    print("Input")
    print(x)
    print("Correct output")
    print(y)
    print("Our output")
    print(yhat)
    print("Correct?")
    if y.shape != yhat.shape:
        print(f"False. Incorrect shape: {y.shape} v {yhat.shape}")
    else:
        print(np.all(y == yhat))


if __name__ == "__main__": main()

