from functools import cache
from typing import Protocol
import steve as s

type Rank = str

STRAT_RANKS = 'L23456789TJQKH'

@cache
def crank(card):
    return card[0]

@cache
def srank(cr, lr=None):
    if cr is None: 
        return None
    if cr == 'A':
        if lr[0] in ['L','H']: return STRAT_RANKS.index(lr[0])
        if lr[1] in ['L','H']: return STRAT_RANKS.index(lr[1])
        return STRAT_RANKS.index('H') if (13-STRAT_RANKS.index(lr[0]) >= STRAT_RANKS.index(lr[1])) else STRAT_RANKS.index('L')
    return STRAT_RANKS.index(cr)

class GameExecution(Protocol):
    def deal_leftright() -> tuple[Rank, Rank]:
        ...   
    def choose_bet(l: Rank, r: Rank) -> int:
        ...
    def get_payout(bet: int, l: Rank, r: Rank) -> int, Rank:
        ...

class Strategy(Protocol):
    def left_ace() -> Rank:
        ...
    def right_ace(left: Rank) -> Rank:
        ...
    def bet_strategy(l: Rank, r: Rank) -> int:
        ...

class CrintonStrategy(Strategy):
    def left_ace(self):
        return 'L'
    def right_ace(self, left):
        if left == 'H': 
            return 'L'
        if left == 'L': 
            return 'H'
        return 'H' if srank(left) <= 7 else 'L'
    def bet_strategy(l, r):
        ''' Default Crinton bet strategy '''
        DEFAULT_BET = {0:0, 1:0, 2:1, 3:1,\
                        4:1, 5:1, 6:1, 7:1,\
                        8:4, 9:4, 10:4, 11:12,\
                        12:12,13:1000000,14:1000000}
        left, right = srank(l,(l,r)), srank(r,(l,r))
        gap = abs(right-left)
        return DEFAULT_BET[gap]

class CrintonExecution(GameExecution):
    def __init__(self, current_player: s.Player, strategy: Strategy) -> int:
        self.player = current_player
        self.strategy = strategy
        left, right = self.deal_leftright()
        bet = self.choose_bet(l=left, r=right)
        payout, middle = self.get_payout(bet, l=left, r=right)
        return payout

    def deal_leftright(self) -> tuple[s.Rank, s.Rank]:
        left, right = crank(deck.pop()), crank(deck.pop())
        if left  == 'A': 
            left = self.strategy.left_ace()
        if right == 'A': 
            right = self.strategy.right_ace(left)
        if srank(left) > srank(right): 
            right, left = left, right
        return left, right

    def choose_bet(self, l, r):
        return 0 if abs(srank(r,(l,r))-srank(l,(l,r))) < 2 \
                    else min(self.strategy.bet_strategy(l,r), self.pot)

    def get_payout(self, bet, l, r):
        ''' Crinton payout '''
        if bet == 0: 
            return 1, None
        else:
            middle, sl, sr = crank(self.deck.pop()), srank(l, (l,r)), srank(r, (l,r))
            sm = 0 if middle=='A' else srank(middle, (l,r))
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









''' CRINTON strategy
    deal left, right
    make rank decision for left Ace, right Ace
    choose bet size
    deal middle card
    calculate payout
'''

''' STEVE strategy
    deal L, R (like above)
    make rank decision for left Ace, right Ace (like above)
    get middle card (like above)
    choose which gap to bet
    choose bet size
    deal xmiddle card
    calculate payout
'''

''' GAMBLOR strategy
    Deal L, R.  --- uses above
    Choose gamblor bet --- uses above
    choose other gamblor bets
    collect my payout
    collect other player playouts
'''




def default_gamblor_strategy(l, r):
    gap = 13 - srank(r,(l,r)) + srank(l,(l,r))
    return 1 if gap >= 7 else 0
