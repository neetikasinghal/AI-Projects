import numpy as np


def take_input():
    with open('input.txt') as fin:
        file_data = fin.read()
        input = file_data.split("\n")
        n = int(input[0])
        p = int(input[1])
        s = int(input[2])
        t = s * 12
        i = 3
        matrix = [[0 for x in range(n)] for y in range(n)]
        while (t != 0):
            coord = input[i]
            coord_split = coord.split(",")
            x = int(coord_split[0])
            y = int(coord_split[1])
            matrix[x][y] = matrix[x][y] + 1
            i = i + 1
            t = t - 1
        return n, p, matrix
    fin.close()


class BitMagic:
    def __init__(self, N, K, matrix, print_solutions=True):
        self.N = N
        self.K = K
        self.board = [[0 for x in range(N)] for y in range(N)]
        self.number_of_solutions = 0
        self.all_ones = (1 << N) - 1
        self.solution_board = []
        self.matrix = matrix
        self.print_solutions = print_solutions
        self.energy_points = 0

    def run(self):
        self.solve(0, 0, 0, 0)

    def solve(self, column, left_diagonal, right_diagonal, queens_placed):
        if queens_placed == self.K:
            self.number_of_solutions += 1
            if self.print_solutions:
                sum = 0
                for i, j in enumerate(self.solution_board):
                    sum = sum + self.matrix[i][j]
                self.energy_points = max(self.energy_points, sum)
            return

        valid_spots = self.all_ones & ~(column | left_diagonal | right_diagonal)
        while valid_spots != 0:
            current_spot = -valid_spots & valid_spots
            self.solution_board.append((current_spot & -current_spot).bit_length() - 1)
            valid_spots ^= current_spot
            self.solve((column | current_spot), (left_diagonal | current_spot) >> 1,
                       (right_diagonal | current_spot) << 1, queens_placed + 1)
            self.solution_board.pop()

    def get_number_of_solutions(self):
        return self.number_of_solutions

    def get_number_of_energy_points(self):
        return self.energy_points


class Greedy:
    def __init__(self, N, K, matrix, print_solutions=True):
        self.N = N
        self.K = K
        self.board = [[0 for x in range(N)] for y in range(N)]
        self.solution_board = []
        self.matrix = matrix
        self.print_solutions = print_solutions
        self.energy_points = 0
        self.result = [0 for x in range(1, n * n, 1)]

    def run(self):
        self.solve(0, 0, 0, 0)

    def is_safe(self, grid, n, row, col):
        for i in range(n):
            if grid[row][i] == 1 or grid[i][col] == 1:
                return False
        for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
            if grid[i][j] == 1:
                return False
        for i, j in zip(range(row, n, 1), range(col, -1, -1)):
            if grid[i][j] == 1:
                return False
        for i, j in zip(range(row, -1, -1), range(col, n, 1)):
            if grid[i][j] == 1:
                return False
        for i, j in zip(range(row, n, 1), range(col, n, 1)):
            if grid[i][j] == 1:
                return False
        return True

    def max_activity(self, M):
        largest = None
        col = None
        for r, row in enumerate(M):
            for c, num in enumerate(row):
                if num > largest or largest is None:
                    largest = num
                    row1 = r
                    col = c
        return (largest, row1, col)

    def run(self):
        for i in range(1, n * n, 1):
            arr = map(list, matrix)
            M = [[0 for x in range(n)] for y in range(n)]
            j = 0
            k = 0
            activity_points = 0
            if i != 1:
                for x in range(1, i, 1):
                    a, b, c = self.max_activity(arr)
                    arr[b][c] = -4
                activity_points_local, r, c = self.max_activity(arr)
                arr = map(list, matrix)
                arr[r][c] = -1
                M[r][c] = 1
                activity_points += activity_points_local
                k += 1
                j += 1
            while k < p and j < (n * n):
                activity_points_local, r, c = self.max_activity(arr)
                if (self.is_safe(M, n, r, c)):
                    M[r][c] = 1
                    arr[r][c] = -1
                    activity_points += activity_points_local
                    k += 1
                else:
                    arr[r][c] = -2

                j += 1
            if k == p:
                self.result[i - 1] = activity_points

    def get_result(self):
        return self.result


class Backtracking:
    def __init__(self, N, K, matrix):
        self.N = N
        self.K = K
        self.matrix = matrix
        self.rows = {}
        self.columns = {}
        self.diagonals = {}
        self.antidiagonals = {}
        self.maxValue = -1
        self.board = np.zeros((n, n))

    def is_safe(self, row, column):
        if row in self.rows and self.rows[row] > 0:
            return False
        if column in self.columns and self.columns[column] > 0:
            return False
        if row - column in self.diagonals and self.diagonals[row - column] > 0:
            return False
        if row + column in self.antidiagonals and self.antidiagonals[row + column] > 0:
            return False
        return True

    def solve_using_backtracking(self, board, col, queens, activity_score, rows, columns, diagonals, antidiagonals):
        if n - col < queens:
            return
        if (col == n and queens == 0) or queens == 0:
            self.maxValue = max(self.maxValue, activity_score)
            return
        if col == n:
            return
        while col < n:
            for row in range(n):
                if self.is_safe(row, col):
                    board[row][col] = 1
                    rows[row] = True
                    columns[col] = True
                    diagonals[row - col] = True
                    antidiagonals[row + col] = True
                    self.solve_using_backtracking(board, col + 1, queens - 1, activity_score + matrix[row][col], rows,
                                                  columns, diagonals, antidiagonals)

                    board[row][col] = 0
                    rows[row] = False
                    columns[col] = False
                    diagonals[row - col] = False
                    antidiagonals[row + col] = False
            col = col + 1

    def run(self):
        self.solve_using_backtracking(self.board, 0, p, 0, self.rows, self.columns, self.diagonals, self.antidiagonals)
        return self.maxValue


if __name__ == '__main__':

    n, p, matrix = take_input()
    fout = open("output.txt", "w+")
    if p == n:
        solver = BitMagic(n, p, matrix)
        solver.run()
        fout.write(str(solver.get_number_of_energy_points()))
    else:
        if (n > 11) or (n == 11 and (p == 7 or p == 8)):
            solver = Greedy(n, p, matrix)
            solver.run()
            fout.write((str(max(solver.get_result()))))

        else:
            solver = Backtracking(n, p, matrix)
            fout.write(str(solver.run()))