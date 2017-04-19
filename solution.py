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
    pass


def eliminate(values):
    pass


def only_choice(values):
    pass


def reduce_puzzle(values):
    pass


def search(values):
    pass


def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """

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
