from typing import Protocol
from player import Player

type Rank = str

STRAT_RANKS = 'L23456789TJQKH'

class GameExecution(Protocol):
    ''' Protocol for executing a turn of a game for a player.
            'deal_leftright' delivers left and right cards, handles ranking Aces,
               and ensures left card is lower ranked than right card.
            'choose_bet' makes the betting decision and refers to strategy as needed.
            'get_payout' resolves the turn and determines the payout to the player. 
    '''
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
    ''' Strategy models the choices players can make - they differentiate among 
        types of player.
            'left_ace' makes the choice of low or high for the first card being an Ace.
            'right_ace' makes the same chocie for the second card being an Ace.
            'bet_strategy' chooses the bet size given the cards dealt.
    '''
    def left_ace() -> Rank:
        ...
    def right_ace(left: Rank) -> Rank:
        ...
    def bet_strategy(left: Rank, right: Rank) -> int:
        ...



