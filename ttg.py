from game import Game
import numpy as np

class ttg(Game):
    def __init__(self, weights = None, tasks = None):
        self.weights = np.zeros((1), dtype=int) if weights is None else weights
        self.num_players = len(self.weights)
        self.tasks = [(1,1)] if tasks is None else tasks

    def v(self, players):

        maxVal = 0

        total_player_weight = 0
        for i in players:
            total_player_weight += i

        for task in self.tasks:
            if total_player_weight >= task[0] and task[1] >= maxVal:
                maxVal = task[1]

        return maxVal
        
    def get_weights(self):
        return self.weights
        
    def get_num_players(self):
        return self.num_players

    def get_task(self):
        return self.tasks

    def set_weights(self, weights):
        if self.num_players != len(weights):
            raise Exception("Weights array must be same size as num_players")

        self.weights = weights

