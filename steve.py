from protocols import Strategy, GameExecution
import strategies as s
import executions as ex


class SteveStrategy(Strategy):
    def __init__(self):
        self.name = 'SteveStrategy'
    left_ace = s.left_ace_is_L
    right_ace = s.default_right_ace
    bet_strategy = s.default_bet_strategy
    def choose_left_gap(self, left, middle, right):
        leftend, rightend, mid = s.srank(left,(left,right)), \
                                 s.srank(right,(left,right)), \
                                 s.srank(middle,(left,right))
        lgap, rgap  = abs(mid-leftend), abs(rightend-mid)
        if lgap in [0,1]:         
            return rgap <= 10
        if lgap in [2,3,4,5,6,7]: 
            return (rgap in [2,3,4,5,6,7]) and (lgap >= rgap)
        if lgap in [8,9,10]:      
            return (rgap in [2,3,4,5,6,7]) or ((rgap in [8,9,10]) and (lgap >= rgap))
        if lgap in [11,12]:       
            return (rgap <= 11) or ((lgap==12) and (rgap==12))
        if lgap in [13]:          
            return True
    def steve_choose_leftright(self, left, middle, right):
        left_gap = self.choose_left_gap(left, middle, right)
        nl       = left   if left_gap else middle
        nr       = middle if left_gap else right
        if nl=='A': 
            nl='L'
        if nr=='A': 
            nr='H'
        return nl, nr

class SteveExecution(GameExecution):
    def execute(self, deck) -> int:
        payouts, left, middle, right, deck, _ = ex.crinton_execute(self, deck)
        payout = 0
        if self.player.chips > 0 and self.pot > 0 and middle:
            nl, nr = self.strategy.steve_choose_leftright(left, middle, right)
            bet                    = self.choose_bet(left=nl, right=nr)
            payout, xmiddle, deck  = self.get_payout(bet, deck, left=nl, right=nr)
        if payout:
            for p in range(len(self.players)):
                if self.player==self.players[p]:
                    payouts[p] += payout
        return payouts, deck

    deal_leftright = ex.default_deal_leftright
    choose_bet = ex.default_choose_bet

    def get_payout(self, bet, deck, left, right):
        if bet == 0: 
            return 1, None, deck
        else:
            middle = s.crank(deck.pop())
            sl, sm, sr = s.srank(left, (left,right)), s.srank(middle, (left,right)), s.srank(right, (left,right))
            if middle == 'A':
                payout = -bet
                if sl=='L' and sr!='H':   
                    middle = 'H'
                elif sl=='H' and sr!='L': 
                    middle = 'L'
                elif sl not in ['H','L'] and sr not in ['H', 'L']:
                     llg, lrg, rlg, rrg = sl, sr, 13-sl, 13-sr
                     middle = 'L' if max(llg,lrg) >= max(rlg, rrg) else 'H'
            elif sm in [sl, sr]: 
                payout = -2 * bet
            elif sl < sm < sr:   
                payout = bet
            else:                
                payout = -bet
            return payout, middle, deck


'''
crinton	Number of games: 100000000	Ante: 4
Player 0  Strategies: default_strategy	Turns: 1212274237	Chips Won:  13198830	ROIt:    0.01089	Chips Won/g:    0.132   14.930
Player 1  Strategies: default_strategy	Turns: 1192117310	Chips Won:   6641883	ROIt:    0.00557	Chips Won/g:    0.066   14.824
Player 2  Strategies: default_strategy	Turns: 1172051867	Chips Won:   -438236	ROIt:   -0.00037	Chips Won/g:   -0.004   14.791
Player 3  Strategies: default_strategy	Turns: 1151952839	Chips Won:  -6530812	ROIt:   -0.00567	Chips Won/g:   -0.065   14.724
Player 4  Strategies: default_strategy	Turns: 1132160994	Chips Won: -12871665	ROIt:   -0.01137	Chips Won/g:   -0.129   14.631
gamblor	Number of games: 100000000	Ante: 4
Player 0  Strategies: default_strategy	Turns:  399177581	Chips Won:  12140635	ROIt:    0.03041	Chips Won/g:    0.121    7.086
Player 1  Strategies: default_strategy	Turns:  380248506	Chips Won:   9287388	ROIt:    0.02442	Chips Won/g:    0.093    6.939
Player 2  Strategies: default_strategy	Turns:  360924778	Chips Won:   1994567	ROIt:    0.00553	Chips Won/g:    0.020    6.792
Player 3  Strategies: default_strategy	Turns:  341723389	Chips Won:  -6883136	ROIt:   -0.02014	Chips Won/g:   -0.069    6.649
Player 4  Strategies: default_strategy	Turns:  320537055	Chips Won: -16539454	ROIt:   -0.05160	Chips Won/g:   -0.165    6.476
steve	Number of games: 100000000	Ante: 4
Player 0  Strategies: default_strategy	Turns:  371478958	Chips Won:  51365223	ROIt:    0.13827	Chips Won/g:    0.514    9.413
Player 1  Strategies: default_strategy	Turns:  351338669	Chips Won:  25775952	ROIt:    0.07336	Chips Won/g:    0.258    9.228
Player 2  Strategies: default_strategy	Turns:  331287884	Chips Won:    186870	ROIt:    0.00056	Chips Won/g:    0.002    9.033
Player 3  Strategies: default_strategy	Turns:  311038415	Chips Won: -25627346	ROIt:   -0.08239	Chips Won/g:   -0.256    8.824
Player 4  Strategies: default_strategy	Turns:  290991568	Chips Won: -51700699	ROIt:   -0.17767	Chips Won/g:   -0.517    8.609
'''
