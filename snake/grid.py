import random

class Grid:
    def __init__(self, columns, lines):
        self.columns = columns
        self.lines = lines
        self.clear()

    def fill(self, cell):
        self.cells = [[cell] * self.lines for i in range(self.columns)]

    def clear(self):
        self.fill(Cell(None))

    def clearcell(self, line, column):
        return self.set(line, column, Cell(None))

    def set(self, line, column, cell):
        if self.inrange(line, column):
            self.cells[line][column] = cell
            return True
        else:
            return False
    
    def get(self, line, column):
        if self.inrange(line, column):
            return self.cells[line][column]
        else:
            return False

    def inrange(self, line, column):
        return (line >= 0 and line < self.lines) and (column >= 0 and column < self.columns)

    def __str__(self):
        s = "Grid[lines:" + str(self.lines) + ",columns:" + str(self.columns) + "]"
        return s

    def printgrid(self):
        print(self)
        for l in range(0, self.lines):
            for c in range(0, self.columns):
                print("[" + str(l) + str(c) + "]" + str(self.cells[l][c]))


class Cell:
    def __init__(self, content):
        self.content = content

    def isempty(self):
        if self.content == None:
            return True
        else:
            return False
    
    def __str__(self):
        return "Cell[isempty:" + str(self.isempty()) + ", content:" + str(self.content) + "]"
