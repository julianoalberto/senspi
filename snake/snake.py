from grid import Grid
from grid import Cell
import random
import readchar

# directions
RIGHT = "d"
LEFT = "a"
UP = "w"
DOWN = "s"

# key mapping
KEY_UP = "'\\x1b[A'"
KEY_DOWN = "'\\x1b[B'"
KEY_LEFT = "'\\x1b[D'"
KEY_RIGHT = "'\\x1b[C'"
KEY_QUIT = "'q'"

# cell content
EMPTY = Cell(" ")
FOOD = Cell("o")
SNAKE = Cell("S")
SNAKE_EDGE = Cell("X")

DIMENSION = 4

class Snake:
    def __init__(self):
        self.grid = Grid(DIMENSION, DIMENSION)
        self.grid.fill(EMPTY)
        self.line = round(DIMENSION / 2)
        self.column = self.line
        self.snake = SNAKE
        self.grid.set(self.line, self.column, self.snake)

        self.foodline = -1
        self.foodcolumn = -1

        self.eaten = 0

        self.randomfood()
        self.start()

    def hassnake(self, line, column):
        return (line == self.line) and (column == self.column)
    
    def hasfood(self, line, column):
        return (line == self.foodline) and (column == self.foodcolumn)

    def randomfood(self):
        random.seed()
        line = random.randrange(0, DIMENSION)
        column = random.randrange(0, DIMENSION)

        if not self.hassnake(line, column):
            self.grid.set(line, column, FOOD)
            self.foodline = line
            self.foodcolumn = column
        else:
            self.randomfood()

    def start(self):
        while True:
            self.display()
            key = repr(readchar.readkey())
            self.processkey(key)

    def display(self):
        if self.inedge():
            self.snake = SNAKE_EDGE
        else:
            self.snake = SNAKE

        # clears grid
        self.grid.fill(EMPTY)
        # update elements
        self.grid.set(self.line, self.column, self.snake)
        self.grid.set(self.foodline, self.foodcolumn, FOOD)
        
        # header
        s = "Use ←↑↓→ \n"
        s += " " + "|"
        for c in range(0, DIMENSION):
            s += str(c) + " "
        s += "\n"

        for l in range(0, DIMENSION):
            s += str(l) +"|"
            for c in range(0, DIMENSION):
                s += self.grid.get(l, c).content
                s += " "
            s += "\n"
        s += "Score: " + str(self.eaten)
        print('\x1bc') # clear
        print(s)   
        
    def inedge(self):
        return not (self.canmove(UP) \
            and self.canmove(DOWN) \
            and self.canmove(RIGHT) \
            and self.canmove(LEFT))

    # return (line, column) for given direction
    # return (-1, -1) if out of grid
    def neighbor(self, direction):
        l = self.line
        c = self.column
        if direction == RIGHT:
            c += 1
        if direction == LEFT:
            c -= 1
        if direction == UP:
            l -= 1
        if direction == DOWN:
            l += 1

        if self.grid.inrange(l, c):
            return l, c
        else:
            return -1, -1

    def canmove(self, direction):
        return self.neighbor(direction) != (-1, -1)

    def move(self, direction):
        if self.canmove(direction):
            newl = self.line
            newc = self.column

            if direction == RIGHT:
                newc += 1
            if direction == LEFT:
                newc -= 1
            if direction == UP:
                newl -= 1
            if direction == DOWN:
                newl += 1

            self.grid.set(newl, newc, self.snake)
            self.line = newl
            self.column = newc

            if self.hasfood(newl, newc):
                self.eaten += 1
                self.randomfood()

            return True

        else:
            return False
            
    def processkey(self, key):
        if key == KEY_UP:
            self.move(UP)
        elif key == KEY_DOWN:
            self.move(DOWN)
        elif key == KEY_LEFT:
            self.move(LEFT)
        elif key == KEY_RIGHT:
            self.move(RIGHT)
        elif key == KEY_QUIT:
            quit()
        
s = Snake()

s.start()
