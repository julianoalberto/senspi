class Position:
    def __init__(self, line, column):
        self.line = line
        self.column = column
        self.next = None

    def __str__(self):
        return str(self.line) + ":" \
            + str(self.column) + "->" \
            + str(self.next)

    def tail(self):
        if self.next == None:
            return self
        return self.next.tail()

    def move(self, line, column):
        oldl = self.line
        oldc = self.column
        self.line = line
        self.column = column

        if self.next != None:
            self.next.move(oldl, oldc)
    
    def append(self, piece):
        if self.next == None:
            # resets tail to avoid circular references
            piece.next = None           
            self.next = piece
        else:
            self.next.append(piece)

    # returns new instance
    def prepend(self, piece):
        piece.next = self
        return piece

    def size(self):
        if self.next == None:
            return 1
        else:
            return 1 + self.next.size()

    





# p = Position(0, 0)
# print(p)


# while p != None:
#     print(p.line)
#     p = p.next

p = Position(0, 0)
print(p.size())

