import protocols as p

class Player:
    def __init__(self, \
                 chips: int, \
                 strategy: p.Strategy):
        self.chips = chips
        self.strategy = strategy
        self.turns = 0
        self.payouts = []
