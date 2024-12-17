


class goban:
    def __init__(self, size):
        self.size = size
        self.board = [0 for i in range(size * size)]
        self.markings = [0 for i in range(size * size)]


    def GetBoard(self, i, j):
        if i < 0 or i >= self.size or j < 0 or j >= self.size:
            return -1
        else:
            return self.board[i + self.size * j]
        
    def SetBoard(self, i, j, color):
        if i < 0 or i >= self.size or j < 0 or j > self.size:
            pass
        else:
            self.board[i + self.size * j] = color

    def GetMarks(self, i, j):
        if i < 0 or i >= self.size or j < 0 or j > self.size:
            return -1
        else:
            return self.markings[i + self.size * j]
        
    def SetMarks(self, i, j, mark):
        if i < 0 or i >= self.size or j < 0 or j > self.size:
            pass
        else:
            self.markings[i + self.size * j] = mark

    def GetAdjacent(self, i, j):
        adj = []
        if self.GetBoard(i -1, j) != -1:
            adj += [i -1 + self.size * j]
        if self.GetBoard(i + 1, j) != -1:
            adj += [i + 1 + self.size * j]
        if self.GetBoard(i, j - 1) != -1:
            adj += [i + self.size * (j - 1)]
        if self.GetBoard(i, j + 1) != -1:
            adj += [i + self.size * (j + 1)]
        return adj


    def chainsandliberties(self):
        chains = []
        for i in range(self.size):
            for j in range(self.size):
                newchain = True
                color = self.GetBoard(i, j)
                if color != 0:
                    for chain in chains:
                        for stone in chain[0]:
                            if stone == i + self.size * j:
                                newchain = False
                else:
                    newchain = False
                if newchain:
                    neighbors = self.GetAdjacent(i, j)
                    chain = [i + self.size * j]
                    liberties = []
                    while len(neighbors) > 0:
                        n = neighbors.pop()
                        if self.board[n] == color and n not in chain:
                            chain += [n]
                            neighbors += self.GetAdjacent(n % self.size, int(n / self.size))
                        if self.board[n] == 0 and n not in liberties:
                            liberties += [n]
                    chains += [(chain, color, len(liberties))]
        return chains
                


    def makemove(self, color, i, j, capturing = True):
        if self.GetBoard(i,j) == 0:
            self.SetBoard(i,j,color)
            if capturing:
                chains = self.chainsandliberties()
                for chain in chains:
                    if chain[1] != color and chain[2] == 0:
                        for stone in chain[0]:
                            self.board[stone] = 0
                chains = self.chainsandliberties()
                for chain in chains:
                    if chain[1] == color and chain[2] == 0:
                        for stone in chain[0]:
                            self.board[stone] = 0


        else:
            return -1 # occupied
        
    def remove(self, i, j):
        self.SetBoard(0, i, j)
        



def main():
    pass


if __name__ == "__main__":
    main()