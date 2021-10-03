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
MY_NEWLINE = re.compile('\n+')


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
        if re.match(MY_NEWLINE, this_char) != None:
            next_state = STATE.ENDBACK
            return next_state, 'valid'
        else:
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

    def next_state_after_ERROR(this_char):
        next_state = STATE.START
        return next_state, 'ERROR'

    def next_state_after_ENDBACK(this_char):
        next_state = STATE.END
        return next_state, 'valid'

    def next_state_after_END(this_char):
        next_state = STATE.START
        return next_state, 'valid'


def get_next_state(this_state, this_char, idx):
    if this_state == STATE.START:
        next_state, log = STATES_TRANS.next_state_after_START(this_char)
        return next_state, log, idx+1

    if this_state == STATE.NUM:
        next_state, log = STATES_TRANS.next_state_after_NUM(this_char)
        return next_state, log, idx+1

    if this_state == STATE.IDandKEYWORDS:
        next_state, log = STATES_TRANS.next_state_after_IDandKEYWORDS(this_char)
        return next_state, log, idx + 1

    if this_state == STATE.EQU:
        next_state, log = STATES_TRANS.next_state_after_EQU(this_char)
        return next_state, log, idx + 1

    if this_state == STATE.WHITESPACE:
        next_state, log = STATES_TRANS.next_state_after_WHITESPACE(this_char)
        return next_state, log, idx + 1

    if this_state == STATE.COMBGN:
        next_state, log = STATES_TRANS.next_state_after_COMBGN(this_char)
        return next_state, log, idx + 1

    if this_state == STATE.ONELINECOM:
        next_state, log = STATES_TRANS.next_state_after_ONELINECOM(this_char)
        return next_state, log, idx + 1

    if this_state == STATE.TWOLINECOMBGN:
        next_state, log = STATES_TRANS.next_state_after_TWOLINECOMBGN(this_char)
        return next_state, log, idx + 1


    if this_state == STATE.TWOLINECOMEND:
        next_state, log = STATES_TRANS.next_state_after_TWOLINECOMEND(this_char)
        return next_state, log, idx + 1

    if this_state == STATE.ERROR:
        next_state, log = STATES_TRANS.next_state_after_ERROR(this_char)
        return next_state, log, idx + 1

    if this_state == STATE.END:
        next_state, log = STATES_TRANS.next_state_after_END(this_char)
        return next_state, log, idx

    if this_state == STATE.ENDBACK:
        next_state, log = STATES_TRANS.next_state_after_ENDBACK(this_char)
        return next_state, log, idx - 1

def get_next_token():
    pass

if __name__ == "__main__":
    # s = "void main ( void ) {\n    int a = 0;\n    // comment1\n    a = 2 + 2;\n    a = a - 3;\n    cde = a;\n    if (b /* comment2 */ == 3d) {\n        a = 3;\n        cd!e = 7;\n    }\n    else */\n    {\n        b = a < cde;\n        {cde = @2;\n    }}\n    return;/* comment 3}"
    s = "/* comment 3}*/ sajad == 10  \n if (sajjad99-12) == 223 \n printf('sajad')"
    this_char_idx = 0
    this_state = STATE.START

    print("{: >10} {: >20} {: >15} {: >20}".format(*['this_char', 'this_state', 'this_char_idx', 'next_state']))
    while this_char_idx < len(s):
        this_char = s[this_char_idx]
        next_state, log, next_char_idx = get_next_state(this_state, this_char, this_char_idx)
        if re.match(MY_NEWLINE, this_char):
            print("{: >10} {: >20} {: >15} {: >20}".format(*['NEWLINE', this_state, this_char_idx, next_state]))
        else:    
            print("{: >10} {: >20} {: >15} {: >20}".format(*[this_char, this_state, this_char_idx, next_state]))
        this_char_idx = next_char_idx
        this_state = next_state
