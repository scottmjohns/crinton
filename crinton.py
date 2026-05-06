from protocols import Strategy, GameExecution, Rank, crank, srank
from player import Player

class CrintonStrategy(Strategy):
    def __init__(self):
        self.name = 'CrintonStrategy'
    def left_ace(self):
        return 'L'
    def right_ace(self, left):
        if left == 'H': 
            return 'L'
        if left == 'L': 
            return 'H'
        return 'H' if srank(left) <= 7 else 'L'
    def bet_strategy(self, left, right):
        ''' Default Crinton bet strategy '''
        DEFAULT_BET = {0:0,   1:0,         2:1,  3:1,  \
                       4:1,   5:1,         6:1,  7:1,  \
                       8:4,   9:4,        10:4, 11:12, \
                       12:12, 13:1000000, 14:1000000}
        left, right = srank(left,(left,right)), srank(right,(left,right))
        gap = abs(right-left)
        return DEFAULT_BET[gap]

class CrintonExecution(GameExecution):
    def __init__(self, current_player: Player, players: list[Player], pot) -> int:
        self.player = current_player
        self.players = players
        self.strategy = self.player.strategy
        self.pot = pot

    def execute(self, deck) -> int:
        left, right, deck = self.deal_leftright(deck)
        bet: int = self.choose_bet(left=left, right=right)
        payout, middle, deck = self.get_payout(bet, deck, left=left, right=right)
        payouts = {p: payout if self.players[p]==self.player else 0 for p in range(len(self.players))}
        return payouts, deck

    def deal_leftright(self, deck) -> tuple[Rank, Rank]:
        left, right = crank(deck.pop()), crank(deck.pop())
        if left  == 'A': 
            left = self.strategy.left_ace()
        if right == 'A': 
            right = self.strategy.right_ace(left=left)
        if srank(left) > srank(right): 
            right, left = left, right
        return left, right, deck
    def choose_bet(self, left, right):
        return 0 if abs(srank(right,(left,right))-srank(left,(left,right))) < 2 \
                    else min(self.strategy.bet_strategy(left,right), self.pot)
    def get_payout(self, bet, deck, left, right):
        ''' Crinton payout '''
        if bet == 0: 
            return 1, None, deck
        else:
            middle, sl, sr = crank(deck.pop()), \
                             srank(left, (left,right)), \
                             srank(right, (left,right))
            sm = 0 if middle=='A' else srank(middle, (left,right))
            if sm==0 and \
                ((sl in [0,13]) or \
                (sr in [0,13])): 
                payout = -2 * bet
            elif sm in [sl, sr]: 
                payout = -2 * bet
            elif sl < sm < sr:   
                payout = bet
            else:
                payout = -bet
            return payout, middle, deck    
