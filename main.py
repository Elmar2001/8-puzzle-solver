from collections import deque

GOAL_STATE = [0, 1, 2, 3, 4, 5, 6, 7, 8]
board_len = 9  # board length is 9 for 8 puzzle (0-8)
SIDE = 3  # side = sqrt(board_len)

initial_state = []  # initial state given by the user

moves = list()  # list moves to solution
GOAL_NODE = None

# goal node will be the latest node, will be backtracked from


class State:
    def __init__(self, state, parent, direction):
        self.state = state
        self.parent = parent
        self.direction = direction

        if self.state is not None:
            self.map = ','.join(str(e) for e in self.state)  # map will be state as a string

    def __eq__(self, other):  # check for equality
        return self.map == other.map


def move(state, pos):
    next_state = state[:]
    i = next_state.index(0)  # find the empty node

    if pos == 1:  # MOVE UP
        if i not in range(0, SIDE):
            next_state[i - SIDE], next_state[i] = next_state[i], next_state[i - SIDE]
            return next_state
        return None

    if pos == 2:  # MOVE DOWN
        if i not in range(board_len - SIDE, board_len):
            next_state[i + SIDE], next_state[i] = next_state[i], next_state[i + SIDE]
            return next_state
        return None

    if pos == 3:  # MOVE LEFT
        if i not in range(0, board_len, SIDE):
            next_state[i - 1], next_state[i] = next_state[i], next_state[i - 1]
            return next_state
        return None

    if pos == 4:  # MOVE RIGHT
        if i not in range(SIDE - 1, board_len, SIDE):
            next_state[i + 1], next_state[i] = next_state[i], next_state[i + 1]
            return next_state
        return None


def expand(node):
    neighbors = [State(move(node.state, 1), node, 1),
                 State(move(node.state, 2), node, 2),
                 State(move(node.state, 3), node, 3),
                 State(move(node.state, 4), node, 4)]  # get all neighbors

    return [neighbor for neighbor in neighbors if neighbor.state is not None]


def bfs_solve(start_state):
    global GOAL_NODE
    explored = set()  # explored states
    qu = deque([State(start_state, None, None)])

    while qu:
        node = qu.popleft()
        explored.add(node.map)

        if node.state == GOAL_STATE:
            GOAL_NODE = node
            return qu

        neighbors = expand(node)

        for neighbor in neighbors:
            if neighbor.map not in explored:
                qu.append(neighbor)
                explored.add(neighbor.map)


def dfs_solve(start_state):
    global GOAL_NODE
    explored = set()  # explored states

    stack = list([State(start_state, None, None)])
    while stack:
        node = stack.pop()
        explored.add(node.map)
        if node.state == GOAL_STATE:
            GOAL_NODE = node
            return stack

        neighbors = reversed(expand(node))

        for neighbor in neighbors:
            if neighbor.map not in explored:
                stack.append(neighbor)
                explored.add(neighbor.map)


def backtrace():
    curr = GOAL_NODE
    directions = {
        1: 'UP',
        2: 'DOWN',
        3: 'LEFT',
        4: 'RIGHT',
    }

    while initial_state != curr.state:
        moves.append(directions[curr.direction])
        curr = curr.parent  # go to the parent

    return moves[::-1]  # reverse all the moves (start to goal view)


def main():
    print("Enter 8-puzzle state seperated with commas: ")
    initial_state.extend([int(el) for el in input().split(',')])

    bfs_solve(initial_state)
    # dfs_solve(initial_state)

    path = backtrace()

    print("->".join(path))
    print("Solution path length: ", len(path))


if __name__ == '__main__':
    main()

