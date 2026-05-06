from protocols import Strategy, GameExecution
import strategies as s
import executions as ex

class GamblorStrategy(Strategy):
    ''' Standard (and initial) Gamblor player strategy. 
            Always chooses low for left ace.
            Chooses low or high for right ace to maximize gap.
            Uses a conservative, default bet size strategy.
            Other players bet when outer gap is seven or larger. '''
    def __init__(self):
        self.name = 'GamblorStrategy'
    left_ace     = s.left_ace_is_L
    right_ace    = s.default_right_ace
    bet_strategy = s.default_bet_strategy
    def default_gamblor_strategy(self, left: s.Rank, right: s.Rank) -> int:
        gap: int = 13 - s.srank(right,(left,right)) + s.srank(left,(left,right))
        return 1 if gap >= 7 else 0

class GamblorExecution(GameExecution):
    ''' Gamblor turn execution.
            Handles main player like Crinton.
            Gives all other players a chance to bet one in missing the gap.
                'gamblor_choose_bet' applies chosen other player betting strategy
                'get_gamblor_payout' applies standard payouts to other players
                    assuming bet size one.
            If pot empties during payout of other players, players are paid
                from left to right.
    '''
    def execute(self, deck: list[str]) -> int:
        payouts: dict[int,int]
        left: s.Rank
        middle: s.Rank
        right: s.Rank
        bet: int
        payouts, left, middle, right, deck, bet = ex.crinton_execute(self, deck)
        if (bet > 0) and (self.pot > 0):
            obet: dict[int,int] = dict()
            other_players: list[int] = [p for p in range(len(self.players)) \
                                        if self.players[p]!=self.player]
            opayout: int = sum(payouts.values())
            for op in other_players:
                obet[op]      = self.gamblor_choose_bet(op, left=left, right=right)
                payout2: int  = self.get_gamblor_payout(obet, op, left, right, middle)
                if payout2 and (((payout2 > 0) and (self.pot - opayout >= payout2)) or payout2 < 0):
                    payouts[op] = payout2
                    opayout += payout2
        return payouts, deck

    deal_leftright = ex.default_deal_leftright
    choose_bet     = ex.default_choose_bet
    get_payout     = ex.get_standard_payout

    def gamblor_choose_bet(self, op: int, left: s.Rank, right: s.Rank) -> int:
        return self.players[op].strategy.default_gamblor_strategy(left,right)
    def get_gamblor_payout(self, obet: int, op: int, \
                           left: s.Rank, right: s.Rank, middle: s.Rank) -> int:
        if obet[op]==1:
            payout: int
            sl: int = s.srank(left,  (left,right))
            sm: int = s.srank(middle,(left,right))
            sr: int = s.srank(right, (left,right))
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