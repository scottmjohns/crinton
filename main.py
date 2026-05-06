import crinton as cr
import steve as st
import analysis as an
import numpy as np
import protocols as p
from player import Player
from enum import StrEnum, auto

class GameType(StrEnum):
    CRINTON = auto()
    STEVE   = auto()
    GAMBLOR = auto()

ARG_COUNT = {'crinton': 3, 'steve': 5, 'gamblor': 7}
MIN_COUNT = {'crinton': 3, 'steve': 4, 'gamblor': 3}

class Game:
    def __init__(self, 
                 gtype: GameType, 
                 execution: cr.GameExecution, 
                 players: list[Player], 
                 player_ante: int) \
                 -> None:
        self.gtype     = gtype
        self.execution = execution
        self.players   = players
        self.player_count: int = len(self.players)
        self.player_ante       = player_ante
        self.starting_chips: list[int] = [player.chips for player in self.players]
        self.pot: int                  = 0
        self.arg: int | None           = None
        self.deck: list[str] | None    = None
        self.play_game()

    def ante(self):
        self.pot = self.player_ante * self.player_count
        for player in self.players:
            player.chips -= self.player_ante
            player.payouts.append(-self.player_ante)

    def process_payout(self, cp, payout):
        self.players[cp].chips += payout
        self.pot -= payout

    def deal_deck(self):
        self.deck = [r+s for r in '23456789TJQKA' for s in 'SCHD']
        np.random.shuffle(self.deck)
        if not self.arg:
            self.arg = tuple([self.deck.pop() for _ in range(ARG_COUNT[self.gtype])])
            return self.deck
        self.deck = [e for e in self.deck if e not in self.arg]

    def play_game(self):
        self.ante()
        self.deal_deck()
        current_player = 0

        while self.pot > 0:
            if self.players[current_player].chips > 0: # only play the turn if the player has chips
                self.turn = self.execution(self.players[current_player], self.players, self.pot)
                self.players[current_player].turns += 1 # increment player turn counter
                if len(self.deck) < MIN_COUNT[self.gtype]: 
                    self.deal_deck() # if there aren't enough cards remaining in the deck, reshuffle
                payouts, self.deck = self.turn.execute(self.deck)
                # self.process_payout(current_player, self.payout)
                # self.players[current_player].payouts.append(self.payout)
                for p in range(len(self.players)):
                    if payouts[p] != 0:
                        self.process_payout(p, payouts[p])
                        self.players[p].payouts.append(payouts[p])
            current_player = (current_player+1) % self.player_count

def run_analysis(gtype: GameType, 
                 player_count: int, 
                 game_count: int, 
                 player_ante: int, 
                 execution: p.GameExecution,
                 player_strategies: list[p.Strategy]):
    analysis: an.Analysis = an.Analysis(gtype=gtype, 
                                        player_strategies=player_strategies, 
                                        game_count=game_count, 
                                        ante=player_ante)
    for _ in range(game_count):
        players = [Player(chips=160, 
                          strategy=player_strategies[j]) 
                   for j in range(player_count)]
        game = Game(gtype=gtype, 
                    execution=execution, 
                    players=players, 
                    player_ante=player_ante)
        for j in range(player_count):
            analysis.turns[j]     += game.players[j].turns
            analysis.chips_won[j] += game.players[j].chips-game.starting_chips[j]
            analysis.payouts[j].extend([sum(game.players[j].payouts)])
    analysis.display_results()

def main():
    player_count: int = 5
    run_analysis(gtype='crinton',
                 player_count=player_count,
                 game_count=10,
                 player_ante=4,
                 execution=cr.CrintonExecution,
                 player_strategies = [cr.CrintonStrategy()]*player_count)
    run_analysis(gtype='steve',
                 player_count=player_count,
                 game_count=10,
                 player_ante=4,
                 execution=st.SteveExecution,
                 player_strategies = [st.SteveStrategy()]*player_count)

if __name__ == "__main__":
    main()
