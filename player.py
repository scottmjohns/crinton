import crinton as cr

class Player:
    def __init__(self, \
                 chips: int, \
                 strategy: cr.Strategy, \
                 second_strategy: cr.Strategy | None = None):
        self.chips = chips
        self.strategy = strategy
        self.second_strategy = second_strategy
        self.turns = 0
        self.payouts = []
