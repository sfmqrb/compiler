from DFA.states import STATE_SCANNER
import re
from DFA.states_trans import STATES_TRANS
from Tools.regex import RE

def get_token_type(raw_token_type, token):
    if raw_token_type == 'IDorKeywords':
        if re.match(RE.KEYWORDS, token):
            return 'KEYWORD'
        else:
            return 'ID'
    else:
        return raw_token_type

def get_next_state(this_state, this_char, idx):
    if this_state == STATE_SCANNER.START:
        next_state, log = STATES_TRANS.next_state_after_START(this_char)
        return next_state, log, idx + 1

    if this_state == STATE_SCANNER.NUM:
        next_state, log = STATES_TRANS.next_state_after_NUM(this_char)
        return next_state, log, idx + 1

    if this_state == STATE_SCANNER.IDandKEYWORDS:
        next_state, log = STATES_TRANS.next_state_after_IDandKEYWORDS(
            this_char)
        return next_state, log, idx + 1

    if this_state == STATE_SCANNER.EQU:
        next_state, log = STATES_TRANS.next_state_after_EQU(this_char)
        return next_state, log, idx + 1

    if this_state == STATE_SCANNER.WHITESPACE:
        next_state, log = STATES_TRANS.next_state_after_WHITESPACE(this_char)
        return next_state, log, idx + 1

    if this_state == STATE_SCANNER.COMBGN:
        next_state, log = STATES_TRANS.next_state_after_COMBGN(this_char)
        return next_state, log, idx + 1

    if this_state == STATE_SCANNER.ONELINECOM:
        next_state, log = STATES_TRANS.next_state_after_ONELINECOM(this_char)
        return next_state, log, idx + 1

    if this_state == STATE_SCANNER.TWOLINECOMBGN:
        next_state, log = STATES_TRANS.next_state_after_TWOLINECOMBGN(
            this_char)
        return next_state, log, idx + 1

    if this_state == STATE_SCANNER.TWOLINECOMEND:
        next_state, log = STATES_TRANS.next_state_after_TWOLINECOMEND(
            this_char)
        return next_state, log, idx + 1

    if this_state == STATE_SCANNER.STAR:
        next_state, log = STATES_TRANS.next_state_after_STAR(this_char)
        return next_state, log, idx + 1

    if this_state == STATE_SCANNER.ERROR:
        next_state, log = STATES_TRANS.next_state_after_ERROR(this_char)
        return next_state, log, idx

    if this_state == STATE_SCANNER.END:
        next_state, log = STATES_TRANS.next_state_after_END(this_char)
        return next_state, log, idx

    if this_state == STATE_SCANNER.ENDBACK:
        next_state, log = STATES_TRANS.next_state_after_ENDBACK(this_char)
        return next_state, log, idx - 1


# def get_next_token():
#     next_state, log, next_char_idx = get_next_state(this_state, this_char, this_char_idx)


def get_final_token(this_state, s, addition_str, start_token, line, token):
    if this_state == STATE_SCANNER.TWOLINECOMBGN or this_state == STATE_SCANNER.TWOLINECOMEND:
        end_token = len(s) - len(addition_str)
        if end_token - start_token < 8:
            token = s[start_token:end_token]
        else:
            token = s[start_token:start_token+7] + '...'
        return line, token, 'Unclosed comment', start_token, end_token
    else:
        return None, None, None, None, None


def print_letter_state(this_char_idx, this_state, this_char, next_state, log):
    if re.match(RE.MY_NEWLINE, this_char):
        print("{: >10} {: >20} {: >15} {: >20} {: >10}".format(
            *['NEWLINE', this_state, this_char_idx, next_state, log]))
    else:
        print("{: >10} {: >20} {: >15} {: >20} {: >10}".format(
            *[this_char, this_state, this_char_idx, next_state, log]))
