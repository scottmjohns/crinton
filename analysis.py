from statistics import stdev
from main import GameType
import protocols as pr

class Analysis():
    def __init__(self, gtype: GameType, player_strategies: list[pr.Strategy], \
                 game_count: int, ante: int) -> None:
        self.gtype : GameType = gtype
        self.player_strategies: list[pr.Strategy]  = player_strategies
        self.game_count: int  = game_count
        self.ante : int              = ante
        self.player_count: int       = len(self.player_strategies)
        self.turns: list[int]        = [0]*self.player_count
        self.chips_won: list[int]    = [0]*self.player_count
        self.payouts:list[list[int]] = [[] for _ in range(self.player_count)]

    def display_results(self):
        roi = [self.chips_won[i]/self.turns[i] if self.turns[i]!=0 else 0 \
               for i in range(self.player_count)]
        print(f"{self.gtype}\t\tNumber of games: {self.game_count}\t\tAnte: {self.ante}")
        for p in range(self.player_count):
           pl: str    = f'Player {p}'
           strat: str = f'  Strategies: {self.player_strategies[p].name}'
           t: str     = f'  Turns: {self.turns[p]:>10}'
           cw: str    = f' Chips Won: {self.chips_won[p]:>9}'
           r: str     = f' ROI/t: {roi[p]:10.5f}'
           cwg: str   = f'\tChips Won/g: {sum(self.payouts[p])/self.game_count:8.3f}'
           sd: str    = f' {stdev(self.payouts[p]):8.2f}' 
           print(pl+strat+t+cw+r+cwg+sd)
