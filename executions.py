from strategies import crank, srank, Rank

def crinton_execute(self, deck):
    left, right, deck = self.deal_leftright(deck)
    bet: int = self.choose_bet(left=left, right=right)
    payout, middle, deck = self.get_payout(bet, deck, left=left, right=right)
    payouts = {p: payout if self.players[p]==self.player else 0 for p in range(len(self.players))}
    return payouts, left, middle, right, deck, bet

def default_deal_leftright(self, deck) -> tuple[Rank, Rank]:
    left, right = crank(deck.pop()), crank(deck.pop())
    if left  == 'A': 
        left = self.strategy.left_ace()
    if right == 'A': 
        right = self.strategy.right_ace(left=left)
    if srank(left) > srank(right): 
        right, left = left, right
    return left, right, deck

def default_choose_bet(self, left, right):
    return 0 if abs(srank(right,(left,right))-srank(left,(left,right))) < 2 \
                else min(self.strategy.bet_strategy(left,right), self.pot)
