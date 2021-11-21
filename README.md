# Student Details

|Field   | Value |
|--------|-------|
|Name    | Philip O' Connor|
|Student # | 21249304 |
| GitHub link |https://github.com/PhilOConnor/ARC |
|Task 1    |d4f3cd78 |
|Task 2    | 2dd70a9a |
|Task 3    | 83302e8f |

# Solutions <br>

## Task 1  - d4f3cd78 - object detection: <br>
![Task 1: d4f3cd78](/images/d4f3cd78.JPG)  <br>
Script will iterate from top to bottom and bottom to top to find a row of 5s. Once found, these are used to define the box boundary.
The interior of the box is filled with the coloured cells.
A local gridspace is created using the box boundary - the benefit of this is it allows me to say any remaining 0 must be the opening. <br>
I fill this empty cell with a value not found in ARC - this allows me to search in the global gridspace for the opening and evaluate the direction of the opening. Once determined, slice the array as appropriate and assign the correct colour to the target cells


## Task 2 - 2dd70a9a - Finite state machine: <br>
![Task 1: d4f3cd78](/images/2dd70a9a.JPG) <br>
First, locate and determine the direction of the start and end points. Both start and end points are in the same orientation so only  need to find out the orientation of the start position. <br>
Once orientation is found, move in this direction until the next cell is taken. Then depending on the current state of the machine, take a random new direction perpendicular to current direction of travel and iterate until the end point is found. 
If the machine gets stuck in the same position for one full loop, it is reset to the initial state. If the next step would take the system out of the domaain of the grid, it is also returned to the initial state.



## Task 3 - 83302e8f - Finite State Machine:<br>

![Task 1: d4f3cd78](/images/83302e8f.JPG) <br>
First locate the walls and then the holes in these walls. Define a set of possible directions of travel (N/S/E/W). At each hole, make the cell yellow and while the next cell in a given direciton is not a wall, move into it and make it yellow. Iterate over the number of blank cells, possible directions and seed cells so each seed effectively grows out into the available area.
If the machine tries to take a step off the edge of the gridspace it is stopped and the next iteration of seed and direction kicks off.
At the end, all joined areas are yellow and unjoined areas are blank, assign all remaining blanks the green colour.
