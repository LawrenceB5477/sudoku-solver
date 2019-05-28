def board_file_reader(file):
    file = open("board.txt", "r")
    board = []
    for line in file:
        board.append(list(line)[:9])
    for i in range(len(board)):
        for j in range(len(board[i])):
            board[i][j] = int(board[i][j])
    return Sudoku(board)

class Sudoku():
    def __init__(self, board):
        self.board = board
        self.hints = set()
        for i in range(9):
            for j in range(9):
                if self.get((i, j)) != 0:
                    self.hints.add(i * 9 + j)

    def get(self, coords):
        x, y = coords
        return self.board[x][y]

    def set(self, coords, num):
        x, y = coords
        self.board[x][y] = num

    def __str__(self):
        string = []
        for line in self.board:
            string.append(str(line))
        return str(string)

class SudokuSolver():

    def __init__(self, board):
        myBoard = []
        for row in board.board:
            myBoard.append(row.copy())
        self.board = Sudoku(myBoard)

    def position_allowed(self, coords):
        x, y = coords
        test = self.board.get(coords)

        #Check row
        for c in range(9):
            if y != c and self.board.get((x, c)) == test:
                return False

        #Check column
        for r in range(9):
            if x != r and self.board.get((r, y)) == test:
                return False

        #Check square
        return self.in_square(coords)

    def in_square(self, pos):
        x, y = pos
        xoffset = x // 3
        yoffset = y // 3

        for i in range(xoffset * 3, 3 * xoffset + 3):
            for j in range(yoffset * 3, yoffset * 3 + 3):
                if i != x and j != y and self.board.get((i, j)) == self.board.get(pos):
                    return False

        return True

    def __str__(self):
        string = ""
        for i in range(9):
            for j in range(9):
                string += str(self.board.get((i, j))) + " "
            string += "\n"
        return string

    def backtrack_solve(self, cell):
        x = cell // 9
        y = cell % 9

        if (cell in self.board.hints):
            if cell == 80:
                return True
            if self.backtrack_solve(cell + 1):
                return True
        else:
            for i in range(9):
                self.board.set((x, y), i + 1)
                if (self.position_allowed((x, y))):
                    if cell == 80:
                        return True
                    if self.backtrack_solve(cell + 1):
                        return True

        if cell not in self.board.hints:
            self.board.set((x, y), 0)
        return False

if __name__ == "__main__":
    board = board_file_reader("board.txt")
    solver = SudokuSolver(board)
    answer = solver.backtrack_solve(0)
    print(answer)
    print(solver)