import numpy as np

# Weighted Voting Game Class
class wvg:
    # Initializes WVG. Weights and Quota are optional and defaulted to 0 if not provided
    def __init__(self, weights = None, quota = None):
        self.num_players = len(self.weights)

        self.weights = np.zeros((self.num_players), dtype=int) if weights is None else weights

        # Make sure there are same number of weights as players
        #if self.num_players != len(self.weights):
        #    raise Exception("Weights array must be same size as num_players")

        self.quota = 0 if quota is None else quota


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
