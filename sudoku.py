import copy

test_board = [
    [0, 5, 0, 3, 1, 4, 0, 6, 0],
    [8, 7, 0, 0, 0, 9, 4, 0, 3],
    [6, 4, 3, 5, 0, 7, 1, 9, 2],
    [0, 0, 7, 8, 0, 5, 2, 1, 0],
    [4, 1, 0, 9, 0, 0, 0, 0, 0],
    [0, 2, 5, 0, 6, 1, 9, 0, 7],
    [7, 9, 0, 2, 5, 0, 8, 4, 0],
    [0, 0, 4, 0, 9, 6, 0, 0, 5],
    [0, 3, 0, 1, 0, 8, 6, 7, 0],
]

solved_board = [
    [2, 5, 9, 3, 1, 4, 7, 6, 8],
    [8, 7, 1, 6, 2, 9, 4, 5, 3],
    [6, 4, 3, 5, 8, 7, 1, 9, 2],
    [9, 6, 7, 8, 3, 5, 2, 1, 4],
    [4, 1, 8, 9, 7, 2, 5, 3, 6],
    [3, 2, 5, 4, 6, 1, 9, 8, 7],
    [7, 9, 6, 2, 5, 3, 8, 4, 1],
    [1, 8, 4, 7, 9, 6, 3, 2, 5],
    [5, 3, 2, 1, 4, 8, 6, 7, 9],
]

test_impossible_board = [
    [0, 5, 0, 3, 1, 4, 0, 6, 0],
    [8, 7, 0, 0, 0, 9, 4, 0, 3],
    [6, 4, 3, 5, 0, 7, 1, 9, 2],
    [0, 0, 7, 8, 0, 5, 2, 1, 0],
    [4, 1, 0, 9, 6, 0, 0, 0, 0],
    [0, 2, 5, 0, 6, 1, 9, 0, 7],
    [7, 9, 0, 2, 5, 0, 8, 4, 0],
    [0, 0, 4, 0, 9, 6, 0, 0, 5],
    [0, 3, 0, 1, 0, 8, 6, 7, 0],
]

complete_set = [1, 2, 3, 4, 5, 6, 7, 8, 9]


def print_board(board):
    for row in board:
        print(row)


def get_next_space_to_solve(board, x, y):
    while y < 9:
        while x < 9:
            if board[y][x] == 0:
                return (x, y)
            x += 1
        x = 0
        y += 1

    return (-1, -1)


# Returns the contents of a 3x3 square numbered from 1-9 as a single list
def get_square(board, square):
    start_x = ((square - 1) * 3) % 9
    start_y = ((square - 1) // 3) * 3

    square_list = []

    for y in range(0, 3):
        for x in range(0, 3):
            square_list.append(board[start_y + y][start_x + x])

    return square_list


def get_col(board, col):
    return [row[col] for row in board]


def is_solved(board):
    # Check rows
    for row in board:
        this_row = list(row)
        this_row.sort()
        if this_row != complete_set:
            return False
    # Check columns
    for col in range(0, 9):
        this_col = get_col(board, col)
        this_col.sort()
        if this_col != complete_set:
            return False
    # Check squares
    for square in range(1, 10):
        this_square = get_square(board, square)
        this_square.sort()
        if this_square != complete_set:
            return False

    return True


def get_possibilities(board, x, y):
    if x == -1 or y == -1:
        return set()

    possibilites = set(complete_set)
    taken_numbers = set()

    row = board[y]
    col = get_col(board, x)
    square_n = ((x // 3) + ((y // 3) * 3)) + 1

    taken_numbers.update(row)
    taken_numbers.update(col)
    taken_numbers.update(get_square(board, square_n))

    possibilites.difference_update(taken_numbers)
    return possibilites


def solve(arg_board, solve_x, solve_y):
    if is_solved(arg_board):
        return arg_board

    if solve_x < 0 or solve_y < 0:
        return False

    board = copy.deepcopy(arg_board)
    solved = False

    this_space_possibilities = get_possibilities(board, solve_x, solve_y)
    for possibility in this_space_possibilities:
        board[solve_y][solve_x] = possibility
        new_x, new_y = get_next_space_to_solve(board, solve_x, solve_y)
        solved = solve(board, new_x, new_y)
        if solved:
            break

    return solved


if __name__ == "__main__":
    print("Trying to solve:")
    print_board(test_board)
    print("")

    x, y = get_next_space_to_solve(test_board, 0, 0)
    done = solve(test_board, x, y)

    if not done:
        print("Solving failed")
    else:
        print("Solved:")
        print_board(done)

    print("\n\nTrying to solve (impossible):")
    print_board(test_impossible_board)
    print("")

    x, y = get_next_space_to_solve(test_impossible_board, 0, 0)
    done = solve(test_impossible_board, x, y)

    if not done:
        print("Solving failed")
    else:
        print("Solved:")
        print_board(done)
