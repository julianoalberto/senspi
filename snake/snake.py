#!/bin/python3
from grid import Grid
from grid import Cell
from position import Position
import random
import readchar

# directions
RIGHT = 6
LEFT = 4
UP = 8
DOWN = 2
NONE = 5

# key mapping
KEY_UP = "'\\x1b[A'"
KEY_DOWN = "'\\x1b[B'"
KEY_LEFT = "'\\x1b[D'"
KEY_RIGHT = "'\\x1b[C'"
KEY_QUIT = "'q'"

# cell content
EMPTY = Cell(" ")
FOOD = Cell("X")

SNAKE_BODY = Cell("o")
SNAKE_TAIL = Cell("*")
SNAKE_UP = Cell("ʌ")
SNAKE_DOWN = Cell("v")
SNAKE_LEFT = Cell("<")
SNAKE_RIGHT = Cell(">")

DIMENSION = 9

class Snake:
    key = None
    def __init__(self):
        self.grid = Grid(DIMENSION, DIMENSION)
        self.grid.fill(EMPTY)
        self.line = round(DIMENSION / 2)
        self.column = self.line
        self.snake = SNAKE_UP
        self.grid.set(self.line, self.column, self.snake)
        self.position = Position(self.line, self.column)
        self.foodline = -1
        self.foodcolumn = -1
        self.movingdir = UP
        self.alive = True

        self.eaten = 0

        self.randomfood()
        self.start()

    def hassnake(self, line, column):
        return self.grid.get(line, column) == SNAKE_BODY \
                or self.grid.get(line, column) == SNAKE_TAIL \
                or self.grid.get(line, column) == SNAKE_UP \
                or self.grid.get(line, column) == SNAKE_DOWN \
                or self.grid.get(line, column) == SNAKE_LEFT \
                or self.grid.get(line, column) == SNAKE_RIGHT
    
    def hasfood(self, line, column):
        return (line == self.foodline) and (column == self.foodcolumn)

    def randomfood(self):
        random.seed()
        line = random.randrange(0, DIMENSION)
        column = random.randrange(0, DIMENSION)

        if not self.hassnake(line, column) and not self.hasfood(line, column):
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
        # clears grid
        self.grid.fill(EMPTY)
        # update elements
        self.grid.set(self.foodline, self.foodcolumn, FOOD)
        
        pos = self.position
        while pos != None:
            self.grid.set(pos.line, pos.column, self.snake)
            self.snake = SNAKE_BODY
            pos = pos.next
        
        if self.movingdir == UP:
            self.snake = SNAKE_UP
        if self.movingdir == DOWN:
            self.snake = SNAKE_DOWN
        if self.movingdir == LEFT:
            self.snake = SNAKE_LEFT
        if self.movingdir == RIGHT:
            self.snake = SNAKE_RIGHT
        self.grid.set(self.position.line, self.position.column, self.snake)

        pos = self.position
        if pos.size() > 2:
            self.grid.set(pos.tail().line, pos.tail().column, SNAKE_TAIL)
        

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

        # footer
        s += "Score: " + str(self.eaten)
        s += "\nLeft : " + str(DIMENSION * DIMENSION - self.eaten)
        #s += "\n" + str(self.position)
        s += "\nMoving: " + str(self.movingdir)
        s += "\nAlive: " + str(self.alive)
        print('\x1bc') # clear
        print(s)   
        
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

        if self.grid.inrange(l, c) and not self.hassnake(l, c):
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
            
            if self.hasfood(newl, newc):
                self.eaten += 1
                self.randomfood()
                self.position = self.position.prepend(Position(newl, newc))
            
            self.line = newl
            self.column = newc

            self.position.move(self.line, self.column)

            self.movingdir = direction

            return True

        else:
            self.alive = False
            self.eaten = 0
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
