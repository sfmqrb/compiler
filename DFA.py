from enum import Enum
import re

class STATE(Enum):
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
        

MY_DIGIT = re.compile(r'[0-9]')
MY_LETTER = re.compile(r'[a-zA-Z]')
MY_LETDIG = re.compile(r'[a-zA-Z0-9]')
MY_SYMB = re.compile(r'[\[\]\(\)\{\}\;\:\-\+\*\<\,]')
KEYWORDS = re.compile(r'if|else|void|int|repeat|break|until|return')
MY_WHITESPACE = re.compile('\s+|\t+|\n+|\r+|\v+|\f+')
MY_FORSLASH = re.compile('\/')
MY_STAR = re.compile('\*')
MY_EQ = re.compile('\=')


class STATES_TRANS():
    def next_state_after_START(this_char):
        if re.match(MY_DIGIT, this_char) != None:
            next_state = STATE.NUM
            return next_state, 'valid'
        elif re.match(MY_LETTER, this_char) != None:
            next_state = STATE.IDandKEYWORDS
            return next_state, 'valid'
        elif re.match(MY_EQ, this_char) != None:
            next_state = STATE.EQU
            return next_state, 'valid'
        elif re.match(MY_SYMB, this_char) != None:
            next_state = STATE.END
            return next_state, 'valid'
        elif re.match(MY_FORSLASH, this_char) != None:
            next_state = STATE.COMBGN
            return next_state, 'valid'
        elif re.match(MY_WHITESPACE, this_char) != None:
            next_state = STATE.WHITESPACE
            return next_state, 'valid'
        else:
            next_state = STATE.ERROR # error
            return next_state, 'Invalid input'

    def next_state_after_NUM(this_char):
        if re.match(MY_DIGIT, this_char) != None:
            next_state = STATE.NUM
            return next_state, 'valid'
        elif re.match(MY_LETTER, this_char) != None:
            next_state = STATE.ERROR
            return next_state, 'Invalid Number'
        else:
            next_state = STATE.ENDBACK
            return next_state, 'valid'

    def next_state_after_IDandKEYWORDS(this_char):
        if re.match(MY_LETDIG, this_char) != None:
            next_state = STATE.IDandKEYWORDS
            return next_state, 'valid'
        else:
            next_state = STATE.ENDBACK
            return next_state, 'valid'

    def next_state_after_EQU(this_char):
        if re.match(MY_EQ, this_char) != None:
            next_state = STATE.END
            return next_state, 'end'
        else:
            next_state = STATE.ENDBACK
            return next_state, 'valid'

    def next_state_after_WHITESPACE(this_char):
        if re.match(MY_WHITESPACE, this_char) != None:
            next_state = STATE.WHITESPACE
            return next_state, 'valid'
        else:
            next_state = STATE.ENDBACK
            return next_state, 'valid'

    def next_state_after_COMBGN(this_char):
        if re.match(MY_FORSLASH, this_char) != None:
            next_state = STATE.ONELINECOM
            return next_state, 'valid'
        elif re.match(MY_STAR, this_char) != None:
            next_state = STATE.TWOLINECOMBGN
            return next_state, 'valid'
        else:
            next_state = STATE.ERROR
            return next_state, 'Unclosed comment'

    def next_state_after_ONELINECOM(this_char):
        if re.match(r'\n', this_char) != None:
            next_state = STATE.ENDBACK
            return next_state, 'valid'
        elif re.match(MY_STAR, this_char) != None:
            next_state = STATE.ONELINECOM
            return next_state, 'valid'

    def next_state_after_TWOLINECOMBGN(this_char):
        if re.match(MY_STAR, this_char) != None:
            next_state = STATE.TWOLINECOMEND
            return next_state, 'valid'
        else:
            next_state = STATE.TWOLINECOMBGN
            return next_state, 'valid'

    def next_state_after_TWOLINECOMEND(this_char):
        if re.match(MY_STAR, this_char) != None:
            next_state = STATE.TWOLINECOMEND
            return next_state, 'valid'
        elif re.match(MY_FORSLASH, this_char) != None:
            next_state = STATE.END
            return next_state, 'valid'
        else:
            next_state = STATE.TWOLINECOMBGN
            return next_state, 'valid'


def get_next_state(this_state, this_char):
    if this_state == STATE.START:
        next_state, log = STATES.next_state_after_START(this_char)
        return next_state, log
        
    if this_state == STATE.NUM:
        next_state, log = STATES.next_state_after_NUM(this_char)
        return next_state, log

    if this_state == STATE.IDandKEYWORDS:
        next_state, log = STATES.next_state_after_IDandKEYWORDS(this_char)
        return next_state, log
    
    if this_state == STATE.EQU:
        next_state, log = STATES.next_state_after_EQU(this_char)
        return next_state, log

    if this_state == STATE.WHITESPACE:
        next_state, log = STATES.next_state_after_WHITESPACE(this_char)
        return next_state, log


    if this_state == STATE.COMBGN:
        next_state, log = STATES.next_state_after_COMBGN(this_char)
        return next_state, log

    if this_state == STATE.ONELINECOM:
        next_state, log = STATES.next_state_after_ONELINECOM(this_char)
        return next_state, log

    if this_state == STATE.TWOLINECOMBGN:
        next_state, log = STATES.next_state_after_TWOLINECOMBGN(this_char)
        return next_state, log


    if this_state == STATE.TWOLINECOMEND:
        next_state, log = STATES.next_state_after_TWOLINECOMEND(this_char)
        return next_state, log

    else : 
        return this_state     
        ERROR = -1


if __name__ == "__main__":
    # print(MY_DIGIT)
    print(STATES_TRANS.next_state_after_START('1'))