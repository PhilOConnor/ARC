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
def solve_d4f3cd78(x):
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

    # Create an entry for the opening we can use to locate it in the global grid 
    grid[opening_local[0][0],opening_local[0][1]]=10

    opening_global = [np.where(x==10)[0][0], np.where(x==10)[1][0]]
    x[opening_global[0] ,opening_global[1]] =8
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

