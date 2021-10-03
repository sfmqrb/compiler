from DFA import get_final_token, get_token_type, get_next_state, print_letter_state
from states import STATE
import re
from regex import RE


class scanner():
    def __init__(self, slen: int, s: str) -> None:
        self.slen = slen
        self.s = s
        self.this_char_idx = 0
        self.start_token = 0
        self.raw_token_type = ''
        self.this_state = STATE.START
        self.errors = []
        self.line = 1
        self.addition_str = "\n  "  # has to begin with \n and be longer than 1
        self.s += self.addition_str
        self.empty_return = (None, None, None)

    def get_next_token(self,):
        # End of the file
        if self.slen <= self.this_char_idx:
            return self.empty_return

        while self.this_char_idx < len(self.s):
            if self.this_state == STATE.START:
                self.start_token = self.this_char_idx
            self.this_char = self.s[self.this_char_idx]
            self.next_state, self.log, self.next_char_idx = get_next_state(
                                self.this_state, self.this_char, self.this_char_idx)
            # print_letter_state(self.this_char_idx,self.this_state,
            # self.this_char, self.next_state, self.log)

            if (self.next_state == STATE.ENDBACK or self.next_state == STATE.END
                    or self.next_state == STATE.ERROR) and self.log:
                self.raw_token_type = self.log

            to_return = self.empty_return
            if self.this_state == STATE.END or self.this_state == STATE.ERROR:
                self.end_token = self.this_char_idx
                self.token = self.s[self.start_token:self.end_token]
                self.token_type = get_token_type(self.raw_token_type, self.token)

                if re.match(RE.MY_NEWLINE, self.token):
                    self.line += 1

                if re.match(RE.MY_WHITESPACE, self.token):
                    pass
                else:
                    # print("line {: >5} {: >20} {: >20} {: >10} {: >10}".format(
                    #     self.line, self.token, self.token_type, self.start_token, self.end_token))
                    to_return = (self.line, self.token, self.token_type)

            self.this_char_idx = self.next_char_idx
            self.this_state = self.next_state
            if to_return[0] != None:
                return to_return

        self.line, self.token, self.log, self.start_token, self.end_token = get_final_token(
            self.this_state, self.s, self.addition_str, self.start_token,
            self.line, self.token)
        if self.line != None:
            return (self.line, self.token, self.token_type)
        return self.empty_return