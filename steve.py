from random import shuffle
from statistics import mean, stdev
from functools import cache
import numpy as np
import crinton_strategies as cs
from enum import StrEnum, auto


STRAT_RANKS = 'L23456789TJQKH'

class GameType(StrEnum):
    CRINTON = auto()
    STEVE = auto()
    GAMBLOR = auto()


class Player:
    def __init__(self, \
                 chips: int, \
                 strategy: cs.Strategy, \
                 second_strategy: cs.Strategy | None = None):
        self.chips = chips
        self.strategy = strategy
        self.second_strategy = second_strategy
        self.turns = 0
        self.payouts = []


    ''' STEVE '''
    # def choose_left_gap(self, left, middle, right):
    #     l, r, m = srank(left,(left,right)), srank(right,(left,right)), srank(middle,(left,right))
    #     lg, rg  = abs(m-l), abs(r-m)
    #     if lg in [0,1]:         return rg <= 10
    #     if lg in [2,3,4,5,6,7]: return (rg in [2,3,4,5,6,7]) and (lg >= rg)
    #     if lg in [8,9,10]:      return (rg in [2,3,4,5,6,7]) or ((rg in [8,9,10]) and (lg >= rg))
    #     if lg in [11,12]:       return (rg <= 11) or ((lg==12) and (rg==12))
    #     if lg in [13]:          return True


class Game:
    def __init__(self, \
                 gtype: GameType, \
                 execution: cs.GameExecution, \
                 players: list[Player], \
                 player_ante: int) -> None:
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

    def play_game(self):
        self.ante()
        self.deal_deck()
        current_player = 0

        while self.pot > 0:
            if self.players[current_player].chips > 0: # only play the turn if the player has chips
                self.players[current_player].turns += 1 # increment player turn counter
                if len(self.deck) < self.min_count: 
                    self.deal_deck() # if there aren't enough cards remaining in the deck, reshuffle

                ''' CRINTON
                    Dealing L, R cards and choosing Low/High for Aces 
                    Choosing bet size
                    Crinton-specific deal middle card, payout
                    global processing payout 
                    Game(deck, players, GameExecution, ante)
                    Players(chips, GameStrategy)
                    '''
                # left, right     = self.crinton_deal_leftright(current_player) ###
                # bet             = self.choose_bet(current_player, l=left, r=right)
                # payout1, middle = self.get_crinton_payout(current_player, bet, l=left, r=right) ###
                payout = self.execution(current_player, self.players[current_player].strategy)
                self.process_payout(current_player, payout)
                self.players[current_player].payouts.append(payout)
            current_player = (current_player+1) % self.player_count

            ''' GAMBLOR
                    Deal L, R.  --- uses above
                    Choose gamblor bet --- uses above
                    Loops through other players and chooses bets from them
                    Process payouts for other players
            '''

                # if (self.gtype == 'gamblor') and (bet > 0) and (self.pot > 0):
                #     obet          = dict()
                #     other_players = [p for p in range(self.player_count) if p!=current_player]
                #     for op in other_players:
                #         obet[op] = self.gamblor_choose_bet(op, l=left, r=right)
                #         payout2  = self.get_gamblor_payout(obet, op, left, right, middle)
                #         if payout2 and (((payout2 > 0) and (self.pot >= payout2)) or payout2 < 0):
                #             self.process_payout(op, payout2)
                #             self.players[op].payouts.append(payout2)

                ''' STEVE
                    Deal L, R --- from above
                    ignore bet outcome from above
                    uses middle from above
                    determines which gap to bet
                    chooses bet size
                    processes payout
                    '''
                # if self.gtype == 'steve':
                #     if self.players[current_player].chips > 0 and self.pot > 0 and middle:
                #         nl, nr, left_gap, = self.steve_choose_leftright(current_player, left, middle, right)
                #         bet               = self.choose_bet(current_player, l=nl, r=nr)
                #         payout2, xmiddle  = self.get_steve_payout(current_player, bet, l=nl, r=nr)
                #         self.process_payout(current_player, payout2)
                #         self.players[current_player].payouts.append(payout2)


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


    def steve_choose_leftright(self, current_player, left, middle, right):
        left_gap = self.players[current_player].choose_left_gap(left, middle, right)
        nl       = left   if left_gap else middle
        nr       = middle if left_gap else right
        if nl=='A': nl='L'
        if nr=='A': nr='H'
        return nl, nr, left_gap

    def choose_bet(self, cp, l, r):
        return 0 if abs(srank(r,(l,r))-srank(l,(l,r))) < 2 \
                 else min(self.players[cp].strategy(l,r), self.pot) if self.gtype=='crinton' \
                 else min(self.players[cp].second_strategy(l,r), self.pot)

    def gamblor_choose_bet(self, op, l, r):
        return self.players[op].gamblor_strategy(l,r)


    def get_steve_payout(self, current_player, bet, l, r):
        if bet == 0: return 1, None
        else:
            middle = rank(self.deck.pop())
            sl, sm, sr = srank(l, (l,r)), srank(middle, (l,r)), srank(r, (l,r))
            if middle == 'A':
                payout = -bet
                if sl=='L' and sr!='H':   middle = 'H'
                elif sl=='H' and sr!='L': middle = 'L'
                elif sl not in ['H','L'] and \
                     sr not in ['H', 'L']:
                     llg, lrg, rlg, rrg = sl, sr, 13-sl, 13-sr
                     middle = 'L' if max(llg,lrg) >= max(rlg, rrg) else 'H'
            elif sm in [sl, sr]: payout = -2 * bet
            elif sl < sm < sr:   payout = bet
            else:                payout = -bet
            return payout, middle

    def get_gamblor_payout(self, obet, op, left, right, middle):
        if obet[op]==1:
            sl, sm, sr = srank(left,(left,right)), srank(middle,(left,right)),  srank(right,(left,right))
            if sm in [0,13] and ((sl in [0,13]) or (sr in [0,13])): payout = -2
            elif sl < sm < sr: payout = 0
            elif (sm==sl) or (sm==sr): payout = -2
            else: payout = 1
            return payout
        return None


def main(gtype: GameType, player_count: int, ante: int, game_count: int) -> None:
    turns  = [0 for _ in range(player_count)]
    chips_won = [0 for _ in range(player_count)]
    payouts = [[] for _ in range(player_count)]
    for i in range(game_count):
        player_list = [Player(160, \
                              strategy=default_strategy, \
                              second_strategy=default_strategy, \
                              gamblor_strategy=default_gamblor_strategy) \
                              for _ in range(player_count)]
        game        = Game(gtype, player_list, ante)
        turns       = [turns[i]+game.players[i].turns for i in range(len(turns))]
        chips_won   = [chips_won[i]+game.players[i].chips-game.starting_chips[i] for i in range(len(chips_won))]
        for j in range(player_count):
            payouts[j].extend([sum(game.players[j].payouts)])
    roi = [chips_won[i]/turns[i] if turns[i]!=0 else 0 for i in range(len(payouts))]
    print(f"{game.gtype}\tNumber of games: {game_count}\tAnte: {game.player_ante}")
    for p in range(player_count):
        print(f"Player {p}  Strategies: {game.players[p].strategy.__name__}\tTurns: {turns[p]:>10}\tChips Won: {chips_won[p]:>9}\tROIt: {roi[p]:10.5f}\tChips Won/g: {sum(payouts[p])/game_count:8.3f} {stdev(payouts[p]):8.3f}")

if __name__ == "__main__":
    main(gtype='crinton', player_count=5, ante=4, game_count=10_000)
    # main(gtype='gamblor', player_count=5, ante=4, game_count=10_000)
    # main(gtype='steve',   player_count=5, ante=4, game_count=10_000)

'''
crinton	Number of games: 100000000	Ante: 4
Player 0  Strategies: default_strategy	Turns: 1212274237	Chips Won:  13198830	ROIt:    0.01089	Chips Won/g:    0.132   14.930
Player 1  Strategies: default_strategy	Turns: 1192117310	Chips Won:   6641883	ROIt:    0.00557	Chips Won/g:    0.066   14.824
Player 2  Strategies: default_strategy	Turns: 1172051867	Chips Won:   -438236	ROIt:   -0.00037	Chips Won/g:   -0.004   14.791
Player 3  Strategies: default_strategy	Turns: 1151952839	Chips Won:  -6530812	ROIt:   -0.00567	Chips Won/g:   -0.065   14.724
Player 4  Strategies: default_strategy	Turns: 1132160994	Chips Won: -12871665	ROIt:   -0.01137	Chips Won/g:   -0.129   14.631
gamblor	Number of games: 100000000	Ante: 4
Player 0  Strategies: default_strategy	Turns:  399177581	Chips Won:  12140635	ROIt:    0.03041	Chips Won/g:    0.121    7.086
Player 1  Strategies: default_strategy	Turns:  380248506	Chips Won:   9287388	ROIt:    0.02442	Chips Won/g:    0.093    6.939
Player 2  Strategies: default_strategy	Turns:  360924778	Chips Won:   1994567	ROIt:    0.00553	Chips Won/g:    0.020    6.792
Player 3  Strategies: default_strategy	Turns:  341723389	Chips Won:  -6883136	ROIt:   -0.02014	Chips Won/g:   -0.069    6.649
Player 4  Strategies: default_strategy	Turns:  320537055	Chips Won: -16539454	ROIt:   -0.05160	Chips Won/g:   -0.165    6.476
steve	Number of games: 100000000	Ante: 4
Player 0  Strategies: default_strategy	Turns:  371478958	Chips Won:  51365223	ROIt:    0.13827	Chips Won/g:    0.514    9.413
Player 1  Strategies: default_strategy	Turns:  351338669	Chips Won:  25775952	ROIt:    0.07336	Chips Won/g:    0.258    9.228
Player 2  Strategies: default_strategy	Turns:  331287884	Chips Won:    186870	ROIt:    0.00056	Chips Won/g:    0.002    9.033
Player 3  Strategies: default_strategy	Turns:  311038415	Chips Won: -25627346	ROIt:   -0.08239	Chips Won/g:   -0.256    8.824
Player 4  Strategies: default_strategy	Turns:  290991568	Chips Won: -51700699	ROIt:   -0.17767	Chips Won/g:   -0.517    8.609
'''
