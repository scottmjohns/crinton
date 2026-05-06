import protocols as p

class Player:
    def __init__(self, \
                 chips: int, \
                 strategy: p.Strategy) -> None:
        self.chips: int           = chips
        self.strategy: p.Strategy = strategy
        self.turns: int           = 0
        self.payouts: list[int]   = []
