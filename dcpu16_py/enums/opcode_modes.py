from enum import Enum

class OpcodeMode(Enum):
    REG = 0
    DEREF = 1
    DEREF_OFF = 2
    SPECIAL = 3
