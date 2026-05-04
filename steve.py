from protocols import Strategy, GameExecution, Rank, crank, srank
from player import Player

class SteveStrategy(Strategy):
    def __init__(self):
        self.name = 'SteveStrategy'
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
    def choose_left_gap(self, left, middle, right):
        leftend, rightend, mid = srank(left,(left,right)), srank(right,(left,right)), srank(middle,(left,right))
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

''' STEVE
                    Deal L, R --- from above
                    ignore bet outcome from above
                    uses middle from above
                    determines which gap to bet
                    chooses bet size
                    processes payout
            '''

class SteveExecution(GameExecution):
    def __init__(self, current_player: Player, pot) -> int:
        self.player = current_player
        self.strategy = self.player.strategy
        self.pot = pot

    def execute(self, deck) -> int:
        left, right, deck = self.deal_leftright(deck)
        bet: int = self.choose_bet(left=left, right=right)
        payout, middle, deck = self.get_payout(bet, deck, left=left, right=right)
        if self.player.chips > 0 and self.pot > 0 and middle:
            nl, nr = self.strategy.steve_choose_leftright(left, middle, right)
            bet                    = self.choose_bet(left=nl, right=nr)
            payout, xmiddle, deck  = self.get_payout(bet, deck, left=nl, right=nr)
        return payout, deck

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
    def get_payout(self, bet, deck, left, right):
        if bet == 0: 
            return 1, None, deck
        else:
            middle = crank(deck.pop())
            sl, sm, sr = srank(left, (left,right)), srank(middle, (left,right)), srank(right, (left,right))
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
