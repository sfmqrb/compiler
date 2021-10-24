from DFA.states import STATE
from Tools.regex import RE
import re

class STATES_TRANS():
    def next_state_after_START(this_char):
        if re.match(RE.MY_DIGIT, this_char) != None:
            next_state = STATE.NUM
            return next_state, ''
        elif re.match(RE.MY_LETTER, this_char) != None:
            next_state = STATE.IDandKEYWORDS
            return next_state, ''
        elif re.match(RE.MY_EQ, this_char) != None:
            next_state = STATE.EQU
            return next_state, ''
        elif re.match(RE.MY_SYMB, this_char) != None:
            next_state = STATE.END
            return next_state, 'SYMBOL'
        elif re.match(RE.MY_FORSLASH, this_char) != None:
            next_state = STATE.COMBGN
            return next_state, ''
        elif re.match(RE.MY_STAR, this_char) != None:
            next_state = STATE.STAR
            return next_state, ''
        elif re.match(RE.MY_WHITESPACE, this_char) != None:
            next_state = STATE.WHITESPACE
            return next_state, ''
        else:
            next_state = STATE.ERROR  # error
            return next_state, 'Invalid input'

    def next_state_after_NUM(this_char):
        if re.match(RE.MY_DIGIT, this_char) != None:
            next_state = STATE.NUM
            return next_state, ''
        elif re.match(RE.MY_LETTER, this_char) != None:
            next_state = STATE.ERROR
            return next_state, 'Invalid number'
        elif re.match(RE.MY_ALPHABET, this_char) != None:
            next_state = STATE.ENDBACK
            return next_state, 'NUM'
        else:
            next_state = STATE.ERROR  # error
            return next_state, 'Invalid input'

    def next_state_after_IDandKEYWORDS(this_char):
        if re.match(RE.MY_LETDIG, this_char) != None:
            next_state = STATE.IDandKEYWORDS
            return next_state, ''
        elif re.match(RE.MY_ALPHABET, this_char) != None:
            next_state = STATE.ENDBACK
            return next_state, 'IDorKeywords'
        else:
            next_state = STATE.ERROR  # error
            return next_state, 'Invalid input'

    def next_state_after_EQU(this_char):
        if re.match(RE.MY_EQ, this_char) != None:
            next_state = STATE.END
            return next_state, 'SYMBOL'
        elif re.match(RE.MY_ALPHABET, this_char) != None:
            next_state = STATE.ENDBACK
            return next_state, 'SYMBOL'
        else:
            next_state = STATE.ERROR
            return next_state, 'Invalid input'

    def next_state_after_WHITESPACE(this_char):
        next_state = STATE.ENDBACK
        return next_state, 'WHITESPACE'

    def next_state_after_COMBGN(this_char):
        if re.match(RE.MY_FORSLASH, this_char) != None:
            next_state = STATE.ONELINECOM
            return next_state, ''

        elif re.match(RE.MY_STAR, this_char) != None:
            next_state = STATE.TWOLINECOMBGN
            return next_state, ''
        else:
            next_state = STATE.ERROR
            return next_state, 'Invalid input'

    def next_state_after_ONELINECOM(this_char):
        if re.match(RE.MY_NEWLINE, this_char) != None:
            next_state = STATE.ENDBACK
            return next_state, 'COMMENT'
        else:
            next_state = STATE.ONELINECOM
            return next_state, ''

    def next_state_after_TWOLINECOMBGN(this_char):
        if re.match(RE.MY_STAR, this_char) != None:
            next_state = STATE.TWOLINECOMEND
            return next_state, ''
        else:
            next_state = STATE.TWOLINECOMBGN
            return next_state, ''

    def next_state_after_TWOLINECOMEND(this_char):
        if re.match(RE.MY_STAR, this_char) != None:
            next_state = STATE.TWOLINECOMEND
            return next_state, ''
        elif re.match(RE.MY_FORSLASH, this_char) != None:
            next_state = STATE.END
            return next_state, 'COMMENT'
        else:
            next_state = STATE.TWOLINECOMBGN
            return next_state, ''

    def next_state_after_STAR(this_char):  # just for begining star
        if re.match(RE.MY_FORSLASH, this_char) != None:
            next_state = STATE.ERROR
            return next_state, 'Unmatched comment'
        elif re.match(RE.MY_ALPHABET, this_char) != None:
            next_state = STATE.ENDBACK
            return next_state, 'SYMBOL'
        else:
            next_state = STATE.ERROR
            return next_state, 'Invalid input'

    def next_state_after_ERROR(this_char):
        next_state = STATE.START
        return next_state, ''

    def next_state_after_ENDBACK(this_char):
        next_state = STATE.END
        return next_state, ''

    def next_state_after_END(this_char):
        next_state = STATE.START
        return next_state, ''