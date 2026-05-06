from functools import cache
from typing import Protocol
from player import Player

type Rank = str

STRAT_RANKS = 'L23456789TJQKH'

class GameExecution(Protocol):
    def __init__(self, current_player: Player, players: list[Player], pot) -> int:
        self.player = current_player
        self.players = players
        self.strategy = self.player.strategy
        self.pot = pot

    def deal_leftright() -> tuple[Rank, Rank]:
        ...   
    def choose_bet(left: Rank, right: Rank) -> int:
        ...
    def get_payout(bet: int, left: Rank, right: Rank) -> tuple[int, Rank]:
        ...

class Strategy(Protocol):
    def left_ace() -> Rank:
        ...
    def right_ace(left: Rank) -> Rank:
        ...
    def bet_strategy(left: Rank, right: Rank) -> int:
        ...

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








''' CRINTON strategy
    deal left, right
    make rank decision for left Ace, right Ace
    choose bet size
    deal middle card
    calculate payout


    STEVE strategy
    deal L, R (like above)
    make rank decision for left Ace, right Ace (like above)
    get middle card (like above)
    choose which gap to bet
    choose bet size
    deal xmiddle card
    calculate payout

    GAMBLOR strategy
    Deal L, R.  --- uses above
    Choose gamblor bet --- uses above
    choose other gamblor bets
    collect my payout
    collect other player playouts
'''





