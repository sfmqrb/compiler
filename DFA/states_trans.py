import re

from DFA.states import STATE_SCANNER
from Tools.regex import RE


class STATES_TRANS:
    def next_state_after_START(this_char):
        if re.match(RE.MY_DIGIT, this_char) != None:
            next_state = STATE_SCANNER.NUM
            return next_state, ""
        elif re.match(RE.MY_LETTER, this_char) != None:
            next_state = STATE_SCANNER.IDandKEYWORDS
            return next_state, ""
        elif re.match(RE.MY_EQ, this_char) != None:
            next_state = STATE_SCANNER.EQU
            return next_state, ""
        elif re.match(RE.MY_SYMB, this_char) != None:
            next_state = STATE_SCANNER.END
            return next_state, "SYMBOL"
        elif re.match(RE.MY_FORSLASH, this_char) != None:
            next_state = STATE_SCANNER.COMBGN
            return next_state, ""
        elif re.match(RE.MY_STAR, this_char) != None:
            next_state = STATE_SCANNER.STAR
            return next_state, ""
        elif re.match(RE.MY_WHITESPACE, this_char) != None:
            next_state = STATE_SCANNER.WHITESPACE
            return next_state, ""
        else:
            next_state = STATE_SCANNER.ERROR  # error
            return next_state, "Invalid input"

    def next_state_after_NUM(this_char):
        if re.match(RE.MY_DIGIT, this_char) != None:
            next_state = STATE_SCANNER.NUM
            return next_state, ""
        elif re.match(RE.MY_LETTER, this_char) != None:
            next_state = STATE_SCANNER.ERROR
            return next_state, "Invalid number"
        elif re.match(RE.MY_ALPHABET, this_char) != None:
            next_state = STATE_SCANNER.ENDBACK
            return next_state, "NUM"
        else:
            next_state = STATE_SCANNER.ERROR  # error
            return next_state, "Invalid input"

    def next_state_after_IDandKEYWORDS(this_char):
        if re.match(RE.MY_LETDIG, this_char) != None:
            next_state = STATE_SCANNER.IDandKEYWORDS
            return next_state, ""
        elif re.match(RE.MY_ALPHABET, this_char) != None:
            next_state = STATE_SCANNER.ENDBACK
            return next_state, "IDorKeywords"
        else:
            next_state = STATE_SCANNER.ERROR  # error
            return next_state, "Invalid input"

    def next_state_after_EQU(this_char):
        if re.match(RE.MY_EQ, this_char) != None:
            next_state = STATE_SCANNER.END
            return next_state, "SYMBOL"
        elif re.match(RE.MY_ALPHABET, this_char) != None:
            next_state = STATE_SCANNER.ENDBACK
            return next_state, "SYMBOL"
        else:
            next_state = STATE_SCANNER.ERROR
            return next_state, "Invalid input"

    def next_state_after_WHITESPACE(this_char):
        next_state = STATE_SCANNER.ENDBACK
        return next_state, "WHITESPACE"

    def next_state_after_COMBGN(this_char):
        if re.match(RE.MY_FORSLASH, this_char) != None:
            next_state = STATE_SCANNER.ONELINECOM
            return next_state, ""

        elif re.match(RE.MY_STAR, this_char) != None:
            next_state = STATE_SCANNER.TWOLINECOMBGN
            return next_state, ""
        else:
            next_state = STATE_SCANNER.ERROR
            return next_state, "Invalid input"

    def next_state_after_ONELINECOM(this_char):
        if re.match(RE.MY_NEWLINE, this_char) != None:
            next_state = STATE_SCANNER.ENDBACK
            return next_state, "COMMENT"
        else:
            next_state = STATE_SCANNER.ONELINECOM
            return next_state, ""

    def next_state_after_TWOLINECOMBGN(this_char):
        if re.match(RE.MY_STAR, this_char) != None:
            next_state = STATE_SCANNER.TWOLINECOMEND
            return next_state, ""
        else:
            next_state = STATE_SCANNER.TWOLINECOMBGN
            return next_state, ""

    def next_state_after_TWOLINECOMEND(this_char):
        if re.match(RE.MY_STAR, this_char) != None:
            next_state = STATE_SCANNER.TWOLINECOMEND
            return next_state, ""
        elif re.match(RE.MY_FORSLASH, this_char) != None:
            next_state = STATE_SCANNER.END
            return next_state, "COMMENT"
        else:
            next_state = STATE_SCANNER.TWOLINECOMBGN
            return next_state, ""

    def next_state_after_STAR(this_char):  # just for begining star
        if re.match(RE.MY_FORSLASH, this_char) != None:
            next_state = STATE_SCANNER.ERROR
            return next_state, "Unmatched comment"
        elif re.match(RE.MY_ALPHABET, this_char) != None:
            next_state = STATE_SCANNER.ENDBACK
            return next_state, "SYMBOL"
        else:
            next_state = STATE_SCANNER.ERROR
            return next_state, "Invalid input"

    def next_state_after_ERROR(this_char):
        next_state = STATE_SCANNER.START
        return next_state, ""

    def next_state_after_ENDBACK(this_char):
        next_state = STATE_SCANNER.END
        return next_state, ""

    def next_state_after_END(this_char):
        next_state = STATE_SCANNER.START
        return next_state, ""
