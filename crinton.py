from protocols import Strategy, GameExecution
import strategies as s
import executions as ex

class CrintonStrategy(Strategy):
    def __init__(self):
        self.name = 'CrintonStrategy'
    left_ace = s.left_ace_is_L
    right_ace = s.default_right_ace
    bet_strategy = s.default_bet_strategy

class CrintonExecution(GameExecution):
    def execute(self, deck) -> int:
        payouts, _, _, _, deck, _ = ex.crinton_execute(self, deck)
        return payouts, deck
    deal_leftright = ex.default_deal_leftright
    choose_bet = ex.default_choose_bet
    get_payout = ex.get_standard_payout