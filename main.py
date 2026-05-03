import crinton as cr
import analysis as an
import numpy as np
from player import Player
from enum import StrEnum, auto

class GameType(StrEnum):
    CRINTON = auto()
    STEVE = auto()
    GAMBLOR = auto()

class Game:
    def __init__(self, \
                 gtype: GameType, \
                 execution: cr.GameExecution, \
                 players: list[Player], \
                 player_ante: int) \
                 -> None:
        self.gtype = gtype
        self.execution = execution
        self.players = players
        self.player_count = len(self.players)
        self.player_ante = player_ante
        self.starting_chips = [player.chips for player in self.players]
        self.pot = 0
        self.arg = None
        self.deck = None
        match self.gtype:
            case 'crinton':
                self.arg_count = 3
                self.min_count = 3
            case 'steve':
                self.arg_count = 5
                self.min_count = 4
            case 'gamblor':
                self.arg_count = 7
                self.min_count = 3
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
            self.arg = tuple([self.deck.pop() for _ in range(self.arg_count)])
            return self.deck
        self.deck = [e for e in self.deck if e not in self.arg]

    def play_game(self):
        self.ante()
        self.deal_deck()
        current_player = 0

        while self.pot > 0:
            if self.players[current_player].chips > 0: # only play the turn if the player has chips
                self.players[current_player].turns += 1 # increment player turn counter
                if len(self.deck) < self.min_count: 
                    self.deal_deck() # if there aren't enough cards remaining in the deck, reshuffle
                self.hand = self.execution(self.players[current_player], self.deck, self.pot)
                self.payout = self.hand.payout
                self.deck = self.hand.deck
                self.process_payout(current_player, self.payout)
                self.players[current_player].payouts.append(self.payout)
            current_player = (current_player+1) % self.player_count

def main():
    gtype = 'crinton'
    player_count = 5
    game_count = 100000
    player_ante = 4
    player_strategies = [cr.CrintonStrategy()]*player_count
    analysis = an.Analysis(gtype=gtype, \
                           player_strategies=player_strategies, \
                           game_count=game_count, \
                           ante=player_ante)
    for i in range(game_count):
        players = [Player(chips=160, strategy=player_strategies[j]) \
                   for j in range(player_count)]
        game = Game(gtype=gtype, \
                    execution=cr.CrintonExecution, \
                    players=players, \
                    player_ante=player_ante)
        for j in range(player_count):
            analysis.turns[j] += game.players[j].turns
            analysis.chips_won[j] += game.players[j].chips-game.starting_chips[j]
            analysis.payouts[j].extend([sum(game.players[j].payouts)])
    analysis.display_results()

if __name__ == "__main__":
    main()
