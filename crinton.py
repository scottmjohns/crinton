from random import shuffle

STRAT_RANKS = 'L23456789TJQKH'

def rank(card):
    return card[0]

def srank(cr, lr=None):
    if cr == 'A':
        if lr[0] in ['L','H']: return STRAT_RANKS.index(lr[0])
        if lr[1] in ['L','H']: return STRAT_RANKS.index(lr[1])
        return STRAT_RANKS.index('H')
    return STRAT_RANKS.index(cr)

class Player:
    def __init__(self, chips, strategy=None):
        self.chips = chips
        self.strategy = strategy or self.default_strategy
        self.turns = 0

    def default_strategy(self, card_tuple, remaining_deck):
        card_tuple = (srank(card_tuple[0]), srank(card_tuple[1]))
        left, right = card_tuple
        gap = abs(right-left)
        bet = 0
        if 2 <= gap <= 7: bet = 1
        if 8 <= gap <= 10: bet = 4
        if 11 <= gap <= 12: bet = 12
        if 13 <= gap <= 14: bet = 10000000
        return bet

    def left_ace(self, deck):
        return 'L'

    def right_ace(self, deck, left):
        return 'L' if left == 'H' else 'H'

class Game:
    def __init__(self, players, player_ante):
        self.players = players
        self.player_count = len(self.players)
        self.player_ante = player_ante
        self.starting_chips = [player.chips for player in self.players]
        self.turns = 0
        self.pot = self.player_ante * self.player_count # ante
        self.arg = None

        for player in self.players:
            player.chips -= self.player_ante

        cdeck = self.deal_cdeck()
        current_player = 0

        while self.pot > 0:
            self.turns += 1
            if self.players[current_player].chips > 0:
                self.players[current_player].turns += 1
                if len(cdeck) < 3: cdeck = self.deal_cdeck()

                left = rank(cdeck.pop())
                if left == 'A': left = self.players[current_player].left_ace(cdeck)
                right = rank(cdeck.pop())
                if right == 'A': right = self.players[current_player].right_ace(cdeck, left)
                if srank(left) > srank(right): right, left = left, right

                payout, cdeck = self.get_payout(current_player, cdeck, left, right)

                self.players[current_player].chips += payout
                self.pot -= payout

            current_player = (current_player+1) % self.player_count

    def deal_cdeck(self):
        cdeck = [r+s for r in '23456789TJQKA' for s in 'SCHD']
        shuffle(cdeck)
        if not self.arg:
            self.arg = cdeck.pop(), cdeck.pop(), cdeck.pop()
        return [e for e in cdeck if e not in self.arg]

    def get_payout(self, current_player, cdeck, left, right):
        if abs(srank(right)-srank(left)) < 2:
            bet, payout, middle = 0, 1, None
        else:
            bet = min(self.players[current_player].strategy((left,right), cdeck), self.pot)
            if bet > 0:
                middle = rank(cdeck.pop())
                if middle=='A' and ((srank(left)=='L' and srank(right)!='H') or (srank(left)=='H' and srank(right)!='L')): payout = -bet
                elif srank(middle, (left, right)) in [srank(left), srank(right)]: payout = -2 * bet
                elif srank(middle, (left, right)) < srank(right) and srank(middle, (left, right)) > srank(left): payout = bet
                else: payout = -bet
        return payout, cdeck

def main(g=1):
    turns = [0,0,0,0,0]
    chips_won = [0,0,0,0,0]
    for _ in range(g):
        p0 = Player(160)
        p1 = Player(160)
        p2 = Player(160)
        p3 = Player(160)
        p4 = Player(160)
        game = Game([p0, p1, p2, p3, p4], 4)
        turns = [turns[i]+game.players[i].turns for i in range(len(turns))]
        chips_won = [chips_won[i]+game.players[i].chips-game.starting_chips[i] for i in range(len(chips_won))]

    roi = [chips_won[i]/turns[i] for i in range(len(turns))]
    print(f"Number of games: {g}\tAnte: {game.player_ante}")
    for p in range(5):
        print(f"Player {p}  Strategy: {game.players[p].strategy.__name__}\tTurns: {turns[p]}\tChips Won: {chips_won[p]:>9}\tROI: {roi[p]:0.5f}")

if __name__ == "__main__":
    main(1000)

'''
Number of games: 100000000	Ante: 4
Player 0  Strategy: default_strategy	Turns: 1672718881	Chips Won:   7504406	ROI: 0.00449
Player 1  Strategy: default_strategy	Turns: 1652585963	Chips Won:   3704821	ROI: 0.00224
Player 2  Strategy: default_strategy	Turns: 1632496349	Chips Won:    127239	ROI: 0.00008
Player 3  Strategy: default_strategy	Turns: 1612417376	Chips Won:  -4058634	ROI: -0.00252
Player 4  Strategy: default_strategy	Turns: 1592631943	Chips Won:  -7277832	ROI: -0.00457
'''
