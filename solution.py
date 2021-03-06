assignments = []

rows = 'ABCDEFGHI'
cols = '123456789'

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers
    for unit in unitList:
        unit_boxes = [] #list to hold values of boxes in the unit
        for b in unit:
            unit_boxes.append(values[b])
        twins = []
        for ptwin in unit_boxes:
            if unit_boxes.count(ptwin) == 2 and len(ptwin) == 2: #Constraints to check for possible twins
                twins.append(ptwin)
        print(twins) # Check that twins have been added to the list
        for twin in twins:
            for d in twin: #the value of twin
                for peer in unit:# check peers within the unit
                    if values[peer] != twin: # check to remove twins in peer
                        assign_value(values, peer, values[peer].replace(d, ''))
    print(twins)
    return values


def cross(A, B):
    """Cross product of elements in A and elements in B.
     - helper function to build grid"""
    new_list = []
    for s in A:
        for t in B:
            new_list.append(s + t)# Covers all possible combinations of A + B
    return new_list

boxes = cross(rows,cols) # Creates boxes using cross function

row_units = [] # Assigning rows to their respective units
for r in rows:
    row_units.append(cross(r,cols))

col_units = [] # Assigning cols to their respective units
for c in cols:
    col_units.append(cross(rows,c))

square_units = [] # Assigning square units(3x3)
for rs in ('ABC', 'DEF', 'GHI'):
    for cs in ('123', '456', '789'):
        square_units.append(cross(rs,cs))

# Diagonal Implementation
diag_unitR2L = [] # Assigning diagonal right unit
for s in zip(rows,cols):
    # used boxes formula, couldn't understand why I couldn't iterate through boxes
    diag_unitR2L.append(s[0] + s[1])

diag_unitL2R = [] # Assigning diagonal left unit
for s in zip(rows,reversed(cols)):
    # reverses rows for left to right row
    diag_unitL2R.append(s[0] + s [1])

# Combining the two diagionals in to one
diag_units = [diag_unitR2L, diag_unitL2R]

unitList = row_units + col_units + square_units + diag_units
# A list of all units required for diagonal sudoku, remove '+ diag_units' for standard

units = dict((s,[u for u in unitList if s in u])
             for s in boxes)

peers = dict((s, set(sum(units[s],[])) - set([s]))
             for s in boxes)


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    flag = [] # A list for values and empties
    nums = '123456789'
    for c in grid:
        if c == '.':
            flag.append(nums) # Appends nums for '.' - empties

        elif c in nums:
            flag.append(c) # Appends the found value
    assert len(grid) == 81
    return dict(zip(boxes, flag))
    # returns the dictionary with the Keys(boxes) and Values(flag)


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1 + max(len(values[box])for box in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF':print(line)
    return


def eliminate(values):
    """
    Takes parameter values - in the form of a dictionary
    flag cannot contain the same value as peers
    eliminates this single value from its peers
    returns the updated Sudoku dictionary - values
    """
    flag = []
    for box in values.keys():
        if len(values[box]) == 1: # if changed to 2 would that equate to twin-snakes?
            flag.append(box)
    for box in flag:
        for peer in peers[box]:
            #values[peer] = values[peer].replace(values[box], '')# removes value and replaces it with ''
            assign_value(values, peer, values[peer].replace(values[box], ''))
    return values


def only_choice(values):
    """
    Takes parameter values - in the form of a dictionary
    Goes through all units in the unitList, if unit has only one possible value
    Assign that value to that box
    returns the updated Sudoku dictionary - values
    """
    for unit in unitList:
        for d in '123456789':
            final_spot = []
            for box in unit:
                if d in values[box]:
                    final_spot.append(box)
            if len(final_spot) == 1:
                assign_value(values,final_spot[0], d)

    return values


def reduce_puzzle(values):
    """
    Takes parameter values - in the form of a dictionary
    Checks to the dictionary for solved boxes
    Calls eliminate function to remove these values from its peers
    Calls only_choice function to assign this singular value to a box
    Performs check for how many boxes are solved
    The above is performed in a loop, exits if counter becomes true
    returns the updates Sudoku dictionary - values
    """
    solved = [box for box in values.keys() if len(values[box])]
    counter = False
    while not counter:
        before = [] #list containing values before
        for box in values.keys():
            if len(values[box]) == 1:
                before.append(box)
        solved_before = len(before)
        # Call to eliminate function
        values = eliminate(values)
        # Call to naked_twins function
        values = naked_twins(values)
        # Call to only_choice function
        values = only_choice(values)

        after = []#list containing values after
        for box in values.keys():
            if len(values[box]) == 1:
                after.append(box)
        solved_after = len(after)

        # Check to break the loop, counter becomes not true -> False
        counter = solved_before == solved_after
        #Sanity check, if box has no available values return false
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    """
    Using Depth-First Search Algorithm and propagation
    Creates a tree to solve the sudoku
    :param values:
    :return: values
    """
    # Call to reduce_puzzle function to reduce the puzzle's possible values for each box
    values = reduce_puzzle(values)
    if values is False:
        return False
    if all(len(values[s]) == 1 for s in boxes):
        return values
    # Pick one unfilled box with the fewest possible values
    n,s = min((len(values[s]),s)for s in boxes if len(values[s]) > 1)
    # Recursive call to solve each one of the updated sudokus - if one returns a value return that one
    for val in values[s]:
        sudoku_new = values.copy()
        sudoku_new[s] = val
        attempt = search(sudoku_new)
        if attempt:
            return attempt


def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    print(diag_unitL2R)
    print(diag_unitR2L)
    #print(diag_units)
    #print(zip(rows,cols))
    values = search(grid_values(grid))
    assert values
    return values

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
