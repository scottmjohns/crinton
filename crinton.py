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
    def get_payout(self, bet, deck, left, right):
        ''' Crinton payout '''
        if bet == 0: 
            return 1, None, deck
        else:
            middle, sl, sr = s.crank(deck.pop()), \
                             s.srank(left, (left,right)), \
                             s.srank(right, (left,right))
            sm = 0 if middle=='A' else s.srank(middle, (left,right))
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
