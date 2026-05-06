from protocols import Strategy, GameExecution, Rank, crank, srank
from player import Player


class GamblorStrategy(Strategy):
    def __init__(self):
        self.name = 'GamblorStrategy'
    def left_ace(self):
        return 'L'
    def right_ace(self, left):
        if left == 'H': 
            return 'L'
        if left == 'L': 
            return 'H'
        return 'H' if srank(left) <= 7 else 'L'
    def bet_strategy(self, left, right):
        ''' Default Crinton bet strategy '''
        DEFAULT_BET = {0:0,   1:0,         2:1,  3:1,  \
                       4:1,   5:1,         6:1,  7:1,  \
                       8:4,   9:4,        10:4, 11:12, \
                       12:12, 13:1000000, 14:1000000}
        left, right = srank(left,(left,right)), srank(right,(left,right))
        gap = abs(right-left)
        return DEFAULT_BET[gap]
    def default_gamblor_strategy(l, r):
        gap = 13 - srank(r,(l,r)) + srank(l,(l,r))
        return 1 if gap >= 7 else 0

class CrintonExecution(GameExecution):
    def __init__(self, current_player: Player, players: list[Player], pot) -> int:
        self.player = current_player
        self.players = players
        self.strategy = self.player.strategy
        self.pot = pot

    def execute(self, deck) -> int:
        left, right, deck = self.deal_leftright(deck)
        bet: int = self.choose_bet(left=left, right=right)
        payout, middle, deck = self.get_payout(bet, deck, left=left, right=right)
        # return payout, deck
        if (bet > 0) and (self.pot > 0):
            obet          = dict()
            other_players = [p for p in range(self.player_count) if p!=self.player]
            for op in other_players:
                obet[op] = self.gamblor_choose_bet(op, l=left, r=right)
                payout2  = self.get_gamblor_payout(obet, op, left, right, middle)
                if payout2 and (((payout2 > 0) and (self.pot >= payout2)) or payout2 < 0):
                    self.process_payout(op, payout2)
                    self.players[op].payouts.append(payout2)


    def deal_leftright(self, deck) -> tuple[Rank, Rank]:
        left, right = crank(deck.pop()), crank(deck.pop())
        if left  == 'A': 
            left = self.strategy.left_ace()
        if right == 'A': 
            right = self.strategy.right_ace(left=left)
        if srank(left) > srank(right): 
            right, left = left, right
        return left, right, deck

    def choose_bet(self, left, right):
        return 0 if abs(srank(right,(left,right))-srank(left,(left,right))) < 2 \
                    else min(self.strategy.bet_strategy(left,right), self.pot)
    def gamblor_choose_bet(self, op, l, r):
        return self.players[op].gamblor_strategy(l,r)

    def get_payout(self, bet, deck, left, right):
        ''' Crinton payout '''
        if bet == 0: 
            return 1, None, deck
        else:
            middle, sl, sr = crank(deck.pop()), \
                             srank(left, (left,right)), \
                             srank(right, (left,right))
            sm = 0 if middle=='A' else srank(middle, (left,right))
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
            sl, sm, sr = srank(left,(left,right)), srank(middle,(left,right)),  srank(right,(left,right))
            if sm in [0,13] and ((sl in [0,13]) or (sr in [0,13])): payout = -2
            elif sl < sm < sr: payout = 0
            elif (sm==sl) or (sm==sr): payout = -2
            else: payout = 1
            return payout
        return None


''' GAMBLOR
                    Deal L, R.  --- uses above
                    Choose gamblor bet --- uses above
                    Loops through other players and chooses bets from them
                    Process payouts for other players
            '''



