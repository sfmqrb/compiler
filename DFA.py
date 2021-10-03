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
    STAR = 15


MY_DIGIT = re.compile(r'[0-9]')
MY_LETTER = re.compile(r'[a-zA-Z]')
MY_LETDIG = re.compile(r'[a-zA-Z0-9]')
MY_SYMB = re.compile(r'[\[\]\(\)\{\}\;\:\-\+\<\,]')
KEYWORDS = re.compile(
    r'^if$|^else$|^void$|^int$|^repeat$|^break$|^until$|^return$')
MY_WHITESPACE = re.compile(' |\t|\n|\r|\v|\f')
MY_FORSLASH = re.compile('\/')
MY_STAR = re.compile('\*')
MY_EQ = re.compile('\=')
MY_NEWLINE = re.compile('\n')
MY_ALPHABET = re.compile(
    r'[a-zA-Z0-9]|[\[\]\(\)\{\}\;\:\-\+\<\,\=\/\*]|[\s|\t|\n|\r|\v|\f]')


def get_token_type(raw_token_type, token):
    if raw_token_type == 'IDorKeywords':
        if re.match(KEYWORDS, token):
            return 'KEYWORD'
        else:
            return 'ID'
    else:
        return raw_token_type


class STATES_TRANS():
    def next_state_after_START(this_char):
        if re.match(MY_DIGIT, this_char) != None:
            next_state = STATE.NUM
            return next_state, ''
        elif re.match(MY_LETTER, this_char) != None:
            next_state = STATE.IDandKEYWORDS
            return next_state, ''
        elif re.match(MY_EQ, this_char) != None:
            next_state = STATE.EQU
            return next_state, ''
        elif re.match(MY_SYMB, this_char) != None:
            next_state = STATE.END
            return next_state, 'SYMBOL'
        elif re.match(MY_FORSLASH, this_char) != None:
            next_state = STATE.COMBGN
            return next_state, ''
        elif re.match(MY_STAR, this_char) != None:
            next_state = STATE.STAR
            return next_state, ''
        elif re.match(MY_WHITESPACE, this_char) != None:
            next_state = STATE.WHITESPACE
            return next_state, ''
        else:
            next_state = STATE.ERROR  # error
            return next_state, 'Invalid input'

    def next_state_after_NUM(this_char):
        if re.match(MY_DIGIT, this_char) != None:
            next_state = STATE.NUM
            return next_state, ''
        elif re.match(MY_LETTER, this_char) != None:
            next_state = STATE.ERROR
            return next_state, 'Invalid Number'
        elif re.match(MY_ALPHABET, this_char) != None:
            next_state = STATE.ENDBACK
            return next_state, 'NUM'
        else:
            next_state = STATE.ERROR  # error
            return next_state, 'Invalid input'

    def next_state_after_IDandKEYWORDS(this_char):
        if re.match(MY_LETDIG, this_char) != None:
            next_state = STATE.IDandKEYWORDS
            return next_state, ''
        elif re.match(MY_ALPHABET, this_char) != None:
            next_state = STATE.ENDBACK
            return next_state, 'IDorKeywords'
        else:
            next_state = STATE.ERROR  # error
            return next_state, 'Invalid input'

    def next_state_after_EQU(this_char):
        if re.match(MY_EQ, this_char) != None:
            next_state = STATE.END
            return next_state, 'SYMBOL'
        elif re.match(MY_ALPHABET, this_char) != None:
            next_state = STATE.ENDBACK
            return next_state, 'SYMBOL'
        else:
            next_state = STATE.ERROR
            return next_state, 'Invalid input'

    def next_state_after_WHITESPACE(this_char):
        # if re.match(MY_WHITESPACE, this_char) != None:
        #     next_state = STATE.WHITESPACE
        #     return next_state, ''
        # else:
        #     next_state = STATE.ENDBACK
        #     return next_state, 'WHITESPACE'
        next_state = STATE.ENDBACK
        return next_state, 'WHITESPACE'

    def next_state_after_COMBGN(this_char):
        if re.match(MY_FORSLASH, this_char) != None:
            next_state = STATE.ONELINECOM
            return next_state, ''
        elif re.match(MY_STAR, this_char) != None:
            next_state = STATE.TWOLINECOMBGN
            return next_state, ''
        else:
            next_state = STATE.ERROR
            return next_state, 'Unclosed comment'

    def next_state_after_ONELINECOM(this_char):
        if re.match(MY_NEWLINE, this_char) != None:
            next_state = STATE.ENDBACK
            return next_state, 'COMMENT'
        else:
            next_state = STATE.ONELINECOM
            return next_state, ''

    def next_state_after_TWOLINECOMBGN(this_char):
        if re.match(MY_STAR, this_char) != None:
            next_state = STATE.TWOLINECOMEND
            return next_state, ''
        else:
            next_state = STATE.TWOLINECOMBGN
            return next_state, ''

    def next_state_after_TWOLINECOMEND(this_char):
        if re.match(MY_STAR, this_char) != None:
            next_state = STATE.TWOLINECOMEND
            return next_state, ''
        elif re.match(MY_FORSLASH, this_char) != None:
            next_state = STATE.END
            return next_state, 'COMMENT'
        else:
            next_state = STATE.TWOLINECOMBGN
            return next_state, ''

    def next_state_after_STAR(this_char):  # just for begining star
        if re.match(MY_FORSLASH, this_char) != None:
            next_state = STATE.ERROR
            return next_state, 'Unmatched comment'
        elif re.match(MY_ALPHABET, this_char) != None:
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


def get_next_state(this_state, this_char, idx):
    if this_state == STATE.START:
        next_state, log = STATES_TRANS.next_state_after_START(this_char)
        return next_state, log, idx + 1

    if this_state == STATE.NUM:
        next_state, log = STATES_TRANS.next_state_after_NUM(this_char)
        return next_state, log, idx + 1

    if this_state == STATE.IDandKEYWORDS:
        next_state, log = STATES_TRANS.next_state_after_IDandKEYWORDS(
            this_char)
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
        next_state, log = STATES_TRANS.next_state_after_TWOLINECOMBGN(
            this_char)
        return next_state, log, idx + 1

    if this_state == STATE.TWOLINECOMEND:
        next_state, log = STATES_TRANS.next_state_after_TWOLINECOMEND(
            this_char)
        return next_state, log, idx + 1

    if this_state == STATE.STAR:
        next_state, log = STATES_TRANS.next_state_after_STAR(this_char)
        return next_state, log, idx + 1

    if this_state == STATE.ERROR:
        next_state, log = STATES_TRANS.next_state_after_ERROR(this_char)
        return next_state, log, idx

    if this_state == STATE.END:
        next_state, log = STATES_TRANS.next_state_after_END(this_char)
        return next_state, log, idx

    if this_state == STATE.ENDBACK:
        next_state, log = STATES_TRANS.next_state_after_ENDBACK(this_char)
        return next_state, log, idx - 1


# def get_next_token():
#     next_state, log, next_char_idx = get_next_state(this_state, this_char, this_char_idx)


def get_final_token(this_state, s, addition_str, start_token, line, token):
    if this_state == STATE.TWOLINECOMBGN or this_state == STATE.TWOLINECOMEND:
        end_token = len(s) - len(addition_str)
        token = s[start_token:end_token]
        return line, token, 'Unclosed comment', start_token, end_token
    else:
        return None, None, None, None, None


def print_letter_state(this_char_idx, this_state, this_char, next_state, log):
    if re.match(MY_NEWLINE, this_char):
        print("{: >10} {: >20} {: >15} {: >20} {: >10}".format(
            *['NEWLINE', this_state, this_char_idx, next_state, log]))
    else:
        print("{: >10} {: >20} {: >15} {: >20} {: >10}".format(
            *[this_char, this_state, this_char_idx, next_state, log]))


if __name__ == "__main__":
    # s = "void main ( void ) {\n \n\n   int a = 0;\n    // comment1\n    a = 2 + 2;\n    a = a - 3;\n    cde = a;\n    if (b /* comment2 */ == 3d) {\n        a = 3;\n        cd!e = 7;\n    }\n    else */\n    {\n        b = a < cde;\n        {cde = @2;\n    }}\n    return;/* comment 3}"
    # s = "void main(void) {"
    # s = 'ifif  dfs '
    # s = "void main*/\nreturn;/* comment 3}*/\ns=10; s=s+1;//#$@#$#@%^$#%$"
    # s = "@sajad@ hello  -1 == 10;"
    # s = "d3d = 10}; 100\nx=10 // a = 10  \n /* dsfds */"

    f = open('./pa_1/PA1_testcases1.2/T02/input.txt', 'r')
    ls_text = f.readlines()
    s = ""
    for txt in ls_text:
        s += txt

    addition_str = "\n  "  # has to begin with \n and be longer than 1
    s += addition_str
    this_char_idx = 0
    this_state = STATE.START
    start_token = 0
    raw_token_type = ''
    line = 1

    while this_char_idx < len(s):
        if this_state == STATE.START:
            start_token = this_char_idx
        this_char = s[this_char_idx]
        next_state, log, next_char_idx = get_next_state(
            this_state, this_char, this_char_idx)

        # print_letter_state(this_char_idx, this_state, this_char, next_state, log)

        if (next_state == STATE.ENDBACK or next_state == STATE.END
                or next_state == STATE.ERROR) and log:
            raw_token_type = log

        if this_state == STATE.END or this_state == STATE.ERROR:
            end_token = this_char_idx
            token = s[start_token:end_token]
            token_type = get_token_type(raw_token_type, token)

            if re.match(MY_NEWLINE, token):
                line += 1

            if re.match(MY_WHITESPACE, token):
                pass
                # print("line {: >5} {: >20} {: >20} {: >10} {: >10}".format(
                #     line, 'WS', token_type, start_token, end_token))
            else:
                print("line {: >5} {: >20} {: >20} {: >10} {: >10}".format(
                    line, token, token_type, start_token, end_token))

        this_char_idx = next_char_idx
        this_state = next_state

    line, token, log, start_token, end_token = get_final_token(
        this_state, s, addition_str, start_token, line, token)
    if line != None:
        print("line {: >5} {: >20} {: >20} {: >10} {: >10}".format(
            line, token, log, start_token, end_token))
