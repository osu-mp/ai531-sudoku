counter = 0


class RuleTracker():

    def __init__(self):
        self.naked_singles = 0
        self.hidden_singles = 0

        self.naked_pairs = 0
        self.hidden_pairs = 0

        self.naked_triples = 0
        self.hidden_triples = 0

    def reset(self):
        self.__init__()

    def __repr__(self):
        print(f'ns = {self.naked_singles}, hs = {self.hidden_singles}'
              f'np = {self.naked_pairs}, hp = {self.hidden_pairs}'
              f'nt = {self.naked_singles}, hp = {self.naked_triples}')


rule_tracker = RuleTracker()
