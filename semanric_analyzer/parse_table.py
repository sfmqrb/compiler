last_adr = 0


class ParsTable:
    scope_stack = []
    pars_table = []

    def add(self, row):
        self.pars_table.append(row)
        if row.category == "param":
            if self.pars_table[self.pars_table.__len__()-2].category == "var":
                self.pars_table[self.pars_table.__len__() - 2].category = "func"

    def set_last_args(self, args):
        self.pars_table[self.pars_table.__len__()-1].args_cells = args

    def set_line_category(self, line, c):
        for row in self.pars_table:
            if row.line == line:
                row.category = c



class ParsRow:
    lexeme = ""
    args_cells = 0
    type = ""
    scope = ""
    line = 0
    # func, var
    category = ""
