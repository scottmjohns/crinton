from protocols import Strategy, GameExecution
import strategies as s
import executions as ex

class CrintonStrategy(Strategy):
    ''' Standard (and initial) Crinton player strategy. 
            Always chooses low for left ace.
            Chooses low or high for right ace to maximize gap.
            Uses a conservative, default bet size strategy. '''
    def __init__(self):
        self.name = 'CrintonStrategy'
    left_ace     = s.left_ace_is_L
    right_ace    = s.default_right_ace
    bet_strategy = s.default_bet_strategy

class CrintonExecution(GameExecution):
    ''' Initial Crinton turn execution.
            Handles main player with default strategies.
    '''
    def execute(self, deck: list[str]) -> tuple[dict[int,int], list[str]]:
        payouts: dict[int,int]
        payouts, _, _, _, deck, _ = ex.crinton_execute(self, deck)
        return payouts, deck
    deal_leftright = ex.default_deal_leftright
    choose_bet     = ex.default_choose_bet
    get_payout     = ex.get_standard_payout