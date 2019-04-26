from __future__ import print_function
from simpleai.search import breadth_first, SearchProblem


GOAL = '''x-x-x-x-x-x-x-x-x-x
x-e-e-e-e-e-e-e-e-x
x-e-e-e-e-e-e-x-e-x
x-e-e-e-e-e-e-x-e-x
x-e-e-e-e-e-e-x-e-x
x-e-e-e-e-x-x-x-e-x
x-e-x-e-e-x-e-e-e-x
x-x-x-e-e-x-e-e-e-x
x-e-x-e-e-e-e-e-e-x
x-e-x-e-e-e-e-e-e-x
x-e-x-e-x-e-x-x-x-x
x-e-x-e-x-e-e-x-e-x
x-e-e-e-x-e-e-x-e-x
x-e-e-x-x-x-e-x-e-x
x-e-e-e-e-x-e-x-e-x
x-e-e-e-e-x-e-x-e-x
x-x-x-x-e-x-e-x-e-x
x-e-e-e-e-e-e-x-e-x
x-e-e-e-e-e-e-e-e-x
x-e-e-e-e-e-e-e-e-x
x-e-e-x-x-x-e-e-e-x
x-e-e-e-e-x-e-e-e-x
x-e-e-e-e-x-e-e-e-x
x-e-e-e-e-x-e-e-e-x
x-e-x-x-e-x-e-e-e-x
x-e-e-x-e-x-x-x-x-x
x-e-c-x-e-e-e-e-e-x
x-e-e-x-e-e-e-e-e-x
x-e-e-x-e-e-e-e-e-x
x-x-x-x-x-x-x-x-x-x
'''

INITIAL = '''x-x-x-x-x-x-x-x-x-x
x-e-e-e-e-e-e-e-e-x
x-e-e-e-e-e-e-x-e-x
x-e-e-e-e-e-c-x-e-x
x-e-e-e-e-e-e-x-e-x
x-e-e-e-e-x-x-x-e-x
x-e-x-e-e-x-e-e-e-x
x-x-x-e-e-x-e-e-e-x
x-e-x-e-e-e-e-e-e-x
x-e-x-e-e-e-e-e-e-x
x-e-x-e-x-e-x-x-x-x
x-e-x-e-x-e-e-x-e-x
x-e-e-e-x-e-e-x-e-x
x-e-e-x-x-x-e-x-e-x
x-e-e-e-e-x-e-x-e-x
x-e-e-e-e-x-e-x-e-x
x-x-x-x-e-x-e-x-e-x
x-e-e-e-e-e-e-x-e-x
x-e-e-e-e-e-e-e-e-x
x-e-e-e-e-e-e-e-e-x
x-e-e-x-x-x-e-e-e-x
x-e-e-e-e-x-e-e-e-x
x-e-e-e-e-x-e-e-e-x
x-e-e-e-e-x-e-e-e-x
x-e-x-x-e-x-e-e-e-x
x-e-e-x-e-x-x-x-x-x
x-e-e-x-e-e-e-e-e-x
x-e-e-x-e-e-e-e-e-x
x-e-e-x-e-e-e-e-e-x
x-x-x-x-x-x-x-x-x-x
'''

def list_to_string(list_):
    return '\n'.join(['-'.join(row) for row in list_])


def string_to_list(string_):
    return [row.split('-') for row in string_.split('\n')]


def find_location(rows, element_to_find):
    '''Find the location of a piece in the puzzle.
       Returns a tuple: row, column'''
    for ir, row in enumerate(rows):
        for ic, element in enumerate(row):
            if element == element_to_find:
                return ir, ic


# we create a cache for the goal position of each piece, so we don't have to
# recalculate them every time
goal_positions = {}
rows_goal = string_to_list(GOAL)
for food in 'c':
    goal_positions['c'] = find_location(rows_goal, food)




class SnakeProblem(SearchProblem):
    def actions(self, state):
        '''Returns a list of the pieces we can move to the empty space.'''
        rows = string_to_list(state)
        row_c, col_c = find_location(rows, 'c')

        actions = []
        if rows[row_c-1][col_c] == 'f':
            actions.append("UP")
            rows[row_c-1][col_c]='e'
        if rows[row_c+1][col_c] == 'f':
            actions.append("DOWN")
            rows[row_c+1][col_c] = 'e'
        if rows[row_c][col_c-1] == 'f':
            actions.append("LEFT")
            rows[row_c][col_c-1] = 'e'
        if rows[row_c][col_c+1] == 'f':
            actions.append("RIGHT")
            rows[row_c][col_c+1] = 'e'
        else:
            if rows[row_c-1][col_c] == 'e':
                actions.append("UP")
            if rows[row_c+1][col_c] == 'e':
                actions.append("DOWN")
            if rows[row_c][col_c-1] == 'e':
                actions.append("LEFT")
            if rows[row_c][col_c+1] == 'e':
                actions.append("RIGHT")

        return actions


    def result(self, state, action):
        '''Return the resulting state after moving a piece to the empty space.
           (the "action" parameter contains the piece to move)
        '''
        rows = string_to_list(state)
        row_c, col_c = find_location(rows, 'c')

        if action == "UP":
            rows[row_c][col_c], rows[row_c-1][col_c] = rows[row_c-1][col_c], rows[row_c][col_c]
        if action == "DOWN":
            rows[row_c][col_c], rows[row_c+1][col_c] = rows[row_c+1][col_c], rows[row_c][col_c]
        if action == "RIGHT":
            rows[row_c][col_c], rows[row_c][col_c+1] = rows[row_c][col_c+1], rows[row_c][col_c]
        if action == "LEFT":
            rows[row_c][col_c], rows[row_c][col_c-1] = rows[row_c][col_c-1], rows[row_c][col_c]
        
        return list_to_string(rows)


    def is_goal(self, state):
        '''Returns true if a state is the goal state.'''
        return state == GOAL

    def cost(self, state1, action, state2):
        '''Returns the cost of performing an action. No useful on this problem, i
           but needed.
        '''
        return 1

    def heuristic(self, state):
        '''Returns an *estimation* of the distance from a state to the goal.
           We are using the manhattan distance.
        '''
        rows = string_to_list(state)

        distance = 0

        row_c, col_c = find_location(rows, 'c')
        row_c_goal, col_c_goal = goal_positions['c']

        distance += abs(row_c - row_c_goal) + abs(col_c - col_c_goal)

        return distance


result = breadth_first(SnakeProblem(INITIAL),graph_search=True)

for action, state in result.path():
    print('Move ', action)
print(state)
