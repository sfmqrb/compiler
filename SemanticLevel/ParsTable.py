last_adr = 100


class ParsTable:
    scope_stack = []
    pars_table = []

    def add(self, row):
        global last_adr
        row.address = last_adr
        last_adr += 4
        self.pars_table.append(row)
        if row.category == "param":
            if self.pars_table[self.pars_table.__len__() - 2].category == "var":
                self.pars_table[self.pars_table.__len__() - 2].category = "func"

    def set_last_args(self, args):
        global last_adr
        self.pars_table[self.pars_table.__len__() - 1].args_cells = args
        last_adr += (args - 1) * 4

    def set_line_category(self, line, c):
        for row in self.pars_table:
            if row.line == line:
                row.category = c

    def get_adr(self, lexeme):
        for i in range(self.pars_table.__len__()):
            if self.pars_table[self.pars_table.__len__() - 1 - i].lexeme == lexeme:
                return self.pars_table[self.pars_table.__len__() - 1 - i].address


class ParsRow:
    address = 0
    lexeme = ""
    args_cells = 0
    type = ""
    scope = ""
    line = 0
    # func, var
    category = ""

    def __str__(self):
        return "address: " + str(self.address) + " lexeme: " + self.lexeme + " scope: " + str(self.scope)
