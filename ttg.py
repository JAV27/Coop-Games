from game import Game

class ttg(Game):
    def __init__(self, num_players = 1, tasks = [(1,1)]):
        self.num_players = num_players
        self.tasks = tasks

    def v(self, players):

        maxVal = 0

        total_player_weight = 0
        for i in players:
            total_player_weight += i

        for task in self.tasks:
            if total_player_weight >= task[0] and task[1] >= maxVal:
                maxVal = task[1]

        return maxVal
        
    def get_num_players(self):
        return self.num_players

    def get_task(self):
        return self.tasks

