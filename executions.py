from strategies import crank, srank, Rank

def crinton_execute(self, deck: list[str]) \
    -> tuple[dict[int, int], Rank, Rank, Rank, list[str], int]:
    left: Rank
    right: Rank
    left, right, deck = self.deal_leftright(deck)
    bet: int = self.choose_bet(left=left, right=right)
    payout: int
    middle: Rank
    payout, middle, deck = self.get_payout(bet, deck, left=left, right=right)
    payouts: dict[int, int] = \
        {p: payout if self.players[p]==self.player else 0 for p in range(len(self.players))}
    return payouts, left, middle, right, deck, bet

def default_deal_leftright(self, deck) -> tuple[Rank, Rank, list[str]]:
    left:  Rank = crank(deck.pop())
    right: Rank = crank(deck.pop())
    if left  == 'A': 
        left = self.strategy.left_ace()
    if right == 'A': 
        right = self.strategy.right_ace(left=left)
    if srank(left) > srank(right): 
        right, left = left, right
    return left, right, deck

def default_choose_bet(self, left: Rank, right: Rank) -> int:
    return 0 if abs(srank(right,(left,right))-srank(left,(left,right))) < 2 \
                else min(self.strategy.bet_strategy(left,right), self.pot)

def get_standard_payout(self, bet: int, deck: list[str], left: Rank, right: Rank) \
    -> tuple[int, Rank|None, list[str]]:
    ''' Crinton payout '''
    if bet == 0: 
        return 1, None, deck
    else:
        middle: Rank = crank(deck.pop()) 
        sl: int = srank(left, (left,right))
        sr: int = srank(right, (left,right))
        sm: int = 0 if middle=='A' else srank(middle, (left,right))
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