import numpy as np

# Weighted Voting Game Class
class wvg:
    # Initializes WVG. Weights and Quota are optional and defaulted to [0],1 if not provided
    def __init__(self, weights = None, quota = None):
        
        self.weights = np.zeros((1), dtype=int) if weights is None else weights
        
        self.num_players = len(self.weights)

        self.quota = 1 if quota is None else quota


    # Getters
    def get_num_players(self):
        return self.num_players

    def get_weights(self):
        return self.weights

    def get_quota(self):
        return self.quota

    # Setters
    def set_num_players(self, num_players):
        self.num_players = num_players
        self.weights = np.zeros((num_players))

    def set_weights(self, weights):
        if self.num_players != len(weights):
            raise Exception("Weights array must be same size as num_players")

        self.weights = weights

    def set_quota(self, quota):
        self.quota = quota

    # Takes in subset of players (array of indices) and returns whether that is a winning coalition (1) or not (0)
    def v(self, players):
        total = 0
        for i in players:
            total += self.weights[i]

        if total >= self.quota:
            return 1 
        else: 
            return 0


