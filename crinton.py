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
    def __init__(self, current_player: Player, deck, pot) -> int:
        self.player = current_player
        self.strategy = self.player.strategy
        self.deck = deck
        self.pot = pot
        self.payout = self.execute()

    def execute(self):
        left, right = self.deal_leftright()
        bet = self.choose_bet(left=left, right=right)
        payout, middle = self.get_payout(bet, left=left, right=right)
        return payout
    
    def deal_leftright(self) -> tuple[Rank, Rank]:
        left, right = crank(self.deck.pop()), crank(self.deck.pop())
        if left  == 'A': 
            left = self.strategy.left_ace()
        if right == 'A': 
            right = self.strategy.right_ace(left=left)
        if srank(left) > srank(right): 
            right, left = left, right
        return left, right
    def choose_bet(self, left, right):
        return 0 if abs(srank(right,(left,right))-srank(left,(left,right))) < 2 \
                    else min(self.strategy.bet_strategy(left,right), self.pot)
    def get_payout(self, bet, left, right):
        ''' Crinton payout '''
        if bet == 0: 
            return 1, None
        else:
            middle, sl, sr = crank(self.deck.pop()), \
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
            return payout, middle    
