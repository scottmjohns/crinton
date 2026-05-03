from statistics import stdev
from main import GameType

class Analysis():
    def __init__(self, gtype: GameType, player_strategies, game_count: int, ante: int):
        self.gtype              = gtype
        self.player_strategies  = player_strategies
        self.game_count         = game_count
        self.ante               = ante
        self.player_count       = len(self.player_strategies)
        self.turns              = [0]*self.player_count
        self.chips_won          = [0]*self.player_count
        self.payouts            = [[] for _ in range(self.player_count)]

    def display_results(self):
        roi = [self.chips_won[i]/self.turns[i] if self.turns[i]!=0 else 0 \
               for i in range(self.player_count)]
        print(f"{self.gtype}\t\tNumber of games: {self.game_count}\t\tAnte: {self.ante}")
        for p in range(self.player_count):
           pl = f'Player {p}'
           strat = f'  Strategies: {self.player_strategies[p].name}'
           t = f'  Turns: {self.turns[p]:>10}'
           cw = f' Chips Won: {self.chips_won[p]:>9}'
           r = f' ROI/t: {roi[p]:10.5f}'
           cwg = f'\tChips Won/g: {sum(self.payouts[p])/self.game_count:8.3f}'
           sd = f' {stdev(self.payouts[p]):8.2f}' 
           print(pl+strat+t+cw+r+cwg+sd)
#           print(f"Player {p}  Strategies: {self.player_strategies[p].name}  Turns: {self.turns[p]:>10} Chips Won: {self.chips_won[p]:>9} ROI/t: {roi[p]:10.5f}\tChips Won/g: {sum(self.payouts[p])/self.game_count:8.3f} {stdev(self.payouts[p]):8.2f}")
