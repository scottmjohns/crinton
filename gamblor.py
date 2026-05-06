from protocols import Strategy, GameExecution
import strategies as s
import executions as ex


class GamblorStrategy(Strategy):
    def __init__(self):
        self.name = 'GamblorStrategy'
    left_ace = s.left_ace_is_L
    right_ace = s.default_right_ace
    bet_strategy = s.default_bet_strategy
    def default_gamblor_strategy(self, left, right):
        gap = 13 - s.srank(right,(left,right)) + s.srank(left,(left,right))
        return 1 if gap >= 7 else 0

class GamblorExecution(GameExecution):
    def execute(self, deck) -> int:
        payouts, left, middle, right, deck, bet = ex.crinton_execute(self, deck)
        if (bet > 0) and (self.pot > 0):
            obet          = dict()
            other_players = [p for p in range(len(self.players)) \
                               if self.players[p]!=self.player]
            opayout = sum(payouts.values())
            for op in other_players:
                obet[op] = self.gamblor_choose_bet(op, left=left, right=right)
                payout2  = self.get_gamblor_payout(obet, op, left, right, middle)
                if payout2 and (((payout2 > 0) and (self.pot - opayout >= payout2)) or payout2 < 0):
                    payouts[op] = payout2
                    opayout += payout2
#        print(f'{payouts=} {left=} {middle=} {right=} {self.pot-sum(payouts.values())=}')
#        input()
        return payouts, deck

    deal_leftright = ex.default_deal_leftright
    choose_bet = ex.default_choose_bet

    def gamblor_choose_bet(self, op, left, right):
        return self.players[op].strategy.default_gamblor_strategy(left,right)

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
    def get_gamblor_payout(self, obet, op, left, right, middle):
        if obet[op]==1:
            sl, sm, sr = s.srank(left,(left,right)), s.srank(middle,(left,right)), s.srank(right,(left,right))
            if sm in [0,13] and ((sl in [0,13]) or (sr in [0,13])): 
                payout = -2
            elif sl < sm < sr: 
                payout = -1
            elif (sm==sl) or (sm==sr): 
                payout = -2
            else: 
                payout = 1
            return payout
        return None