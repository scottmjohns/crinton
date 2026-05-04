from protocols import Strategy, GameExecution, Rank, crank, srank
from player import Player

'''
        match self.gtype:
            case 'crinton':
                self.arg_count = 3
                self.min_count = 3
            case 'steve':
                self.arg_count = 5
                self.min_count = 4
            case 'gamblor':
                self.arg_count = 7
                self.min_count = 3

'''
''' GAMBLOR
                    Deal L, R.  --- uses above
                    Choose gamblor bet --- uses above
                    Loops through other players and chooses bets from them
                    Process payouts for other players
            '''

                # if (self.gtype == 'gamblor') and (bet > 0) and (self.pot > 0):
                #     obet          = dict()
                #     other_players = [p for p in range(self.player_count) if p!=current_player]
                #     for op in other_players:
                #         obet[op] = self.gamblor_choose_bet(op, l=left, r=right)
                #         payout2  = self.get_gamblor_payout(obet, op, left, right, middle)
                #         if payout2 and (((payout2 > 0) and (self.pot >= payout2)) or payout2 < 0):
                #             self.process_payout(op, payout2)
                #             self.players[op].payouts.append(payout2)

def gamblor_choose_bet(self, op, l, r):
    return self.players[op].gamblor_strategy(l,r)

    def get_gamblor_payout(self, obet, op, left, right, middle):
        if obet[op]==1:
            sl, sm, sr = srank(left,(left,right)), srank(middle,(left,right)),  srank(right,(left,right))
            if sm in [0,13] and ((sl in [0,13]) or (sr in [0,13])): payout = -2
            elif sl < sm < sr: payout = 0
            elif (sm==sl) or (sm==sr): payout = -2
            else: payout = 1
            return payout
        return None

def default_gamblor_strategy(l, r):
    gap = 13 - srank(r,(l,r)) + srank(l,(l,r))
    return 1 if gap >= 7 else 0
