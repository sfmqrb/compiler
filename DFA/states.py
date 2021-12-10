from enum import Enum


class STATE_SCANNER(Enum):
    START = 0
    ENDBACK = 200
    END = 100
    NUM = 1
    IDandKEYWORDS = 3
    EQU = 5
    WHITESPACE = 14
    COMBGN = 8
    ONELINECOM = 9
    TWOLINECOMBGN = 11
    TWOLINECOMEND = 12
    ERROR = -1
    STAR = 15
