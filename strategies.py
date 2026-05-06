from functools import cache

STRAT_RANKS = 'L23456789TJQKH'

type Rank = str

@cache
def crank(card):
    return card[0]

@cache
def srank(cr, lr=None):
    if cr is None: 
        return None
    if cr == 'A':
        if lr[0] in ['L','H']: 
            return STRAT_RANKS.index(lr[0])
        if lr[1] in ['L','H']: 
            return STRAT_RANKS.index(lr[1])
        return STRAT_RANKS.index('H') if (13-STRAT_RANKS.index(lr[0]) >= STRAT_RANKS.index(lr[1])) else STRAT_RANKS.index('L')
    return STRAT_RANKS.index(cr)

def left_ace_is_L(self) -> str:
    return 'L'

def default_right_ace(self, left: str) -> str:
    if left == 'H': 
        return 'L'
    if left == 'L': 
        return 'H'
    return 'H' if srank(left) <= 7 else 'L'

def default_bet_strategy(self, left: str, right: str) -> int:
    ''' Default Crinton bet strategy '''
    DEFAULT_BET = {0:0,   1:0,         2:1,  3:1,  \
                    4:1,   5:1,         6:1,  7:1,  \
                    8:4,   9:4,        10:4, 11:12, \
                    12:12, 13:1000000, 14:1000000}
    left, right = srank(left,(left,right)), srank(right,(left,right))
    gap = abs(right-left)
    return DEFAULT_BET[gap]
