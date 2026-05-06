from functools import cache

STRAT_RANKS = 'L23456789TJQKH'

type Rank = str

@cache
def crank(card:str) -> Rank:
    ''' Given a card ("8C"), returns the rank ("8"). '''
    return card[0]

@cache
def srank(cr: Rank, lr: tuple[Rank,Rank]=None) -> int | None:
    ''' Returns the numerical rank of cr according to its index in STRAT_RANKS.
        Handles "cr is Ace" differently, in order to catch all cases when the 
        middle card is an Ace and matches one of the L/R cards: 
            If one of lr is an ace (L or H), match that value.
            Otherwise return L or H, whichever maximizes the gap between it 
                and the furthest L/R (for Steve purposes). '''
    if cr is None: 
        return None
    if cr == 'A':
        if lr[0] in ['L','H']: 
            return STRAT_RANKS.index(lr[0])
        if lr[1] in ['L','H']: 
            return STRAT_RANKS.index(lr[1])
        return STRAT_RANKS.index('H') if (13-STRAT_RANKS.index(lr[0]) >= STRAT_RANKS.index(lr[1])) \
                                      else STRAT_RANKS.index('L')
    return STRAT_RANKS.index(cr)

def left_ace_is_L(self, left: Rank=None) -> Rank:
    ''' When the left (first) card is an Ace, always choose low ("L"). '''
    return 'L'

def default_right_ace(self, left: Rank) -> Rank:
    ''' Delivers a low ("L") or high ("H") rank for an ace on the right card,
        the card drawn second. If the left card is an Ace, choose the opposite.
        Otherwise, choose L or H to maximize the size of the gap. '''
    if left == 'H': 
        return 'L'
    if left == 'L': 
        return 'H'
    return 'H' if srank(left) <= 7 else 'L'

def default_bet_strategy(self, left: Rank, right: Rank) -> int:
    ''' Default Crinton bet strategy. Given Ranks for a left and right card,
        delivers an int bet size based on the rank gap between them. '''
    DEFAULT_BET: dict[int,int] = {0:0,   1:0,         2:1,       3:1,  \
                                  4:1,   5:1,         6:1,       7:1,  \
                                  8:4,   9:4,        10:4,      11:12, \
                                  12:12, 13:1000000, 14:1000000}
    leftend: int  = srank(left,(left,right))
    rightend: int = srank(right,(left,right))
    gap: int      = abs(rightend-leftend)
    return DEFAULT_BET[gap]
