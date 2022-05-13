from enum import Enum


class Rule(Enum):
    """
    Class having all the allowed trick names.
    """
    NONE = 0
    SINGLES = 1
    PAIRS = 2
    TRIPLES = 4