from game import Game
import numpy as np

class isg(Game):
    def __init__(self, matrix = None):
        self.matrix = np.array(([[1]]), dtype=int) if matrix is None else np.array((matrix), dtype=int)
        self.num_players = matrix.shape[0]

    # Players should be an array of player id's i.e. [1,5,6]
    def v(self, players):
        total = 0
        for i in players:
            for j in players:
                if type(i) != "int" or type("j") != "int":
                    raise Exception("Subgraph must consist of integers")

                total += self.matrix[i][j]

        return total/2