"""
N-Queens Problem using Backtracking
CS5303 - Design and Analysis of Algorithms Lab
Ex. No. 7
"""


def is_safe(board, row, col):
    """Check if a queen can be placed at (row, col) without conflict."""
    for prev_row in range(row):
        placed = board[prev_row]
        if placed == col:  # Same column
            return False
        if abs(prev_row - row) == abs(placed - col):  # Same diagonal
            return False
    return True


def solve_n_queens(n):
    """Solve the N-Queens problem using backtracking.

    Returns:
        solutions: list of solutions, each solution is a list where
                   solution[row] = col of the queen in that row
        backtrack_count: number of times the algorithm hit a dead end
                          and had to backtrack
    """
    board = [-1] * n
    solutions = []
    backtrack_count = [0]

    def backtrack(row):
        if row == n:
            solutions.append(board[:])
            return

        placed_any = False
        for col in range(n):
            if is_safe(board, row, col):
                board[row] = col
                backtrack(row + 1)
                board[row] = -1  # Undo (backtrack)
                placed_any = True

        if not placed_any:
            backtrack_count[0] += 1

    backtrack(0)
    return solutions, backtrack_count[0]


def display_board(solution, n):
    """Print the board with queens (Q) and empty cells (.)"""
    print('  +' + '---+' * n)
    for row in range(n):
        print('  |', end='')
        for col in range(n):
            if solution[row] == col:
                print(' Q |', end='')
            else:
                print(' . |', end='')
        print()
        print('  +' + '---+' * n)


# --- Solve for N=4 (show all solutions) and N=6, N=8 (count only) ---
if __name__ == '__main__':
    for n in [4, 6, 8]:
        solutions, backtracks = solve_n_queens(n)
        print(f'N={n}: {len(solutions)} solutions, {backtracks} backtracks')

        if n == 4:
            print(f'\nAll solutions for {n}-Queens:')
            for i, sol in enumerate(solutions, 1):
                print(f'\nSolution {i}: {sol}')
                display_board(sol, n)
        print()
