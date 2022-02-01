last_adr = 100
symbol_table_instance = None


class SymbolTableClass:
    scope_stack = []
    pars_table = []

    @staticmethod
    def get_instance():
        global symbol_table_instance
        if symbol_table_instance is None:
            symbol_table_instance = SymbolTableClass()
        return symbol_table_instance

    def add(self, row):
        global last_adr
        row.address = last_adr
        last_adr += 4
        self.pars_table.append(row)
        # can handle zero input count function?? amir
        if row.category == "param":
            if self.pars_table[self.pars_table.__len__() - 2].category == "var":
                self.pars_table[self.pars_table.__len__() -
                                2].category = "func"

    def set_last_args(self, args, arr_temp):
        global last_adr
        self.pars_table[self.pars_table.__len__() - 1].args_cells = args
        self.pars_table[self.pars_table.__len__() - 1].temp_start_pos = arr_temp

    def set_line_category(self, line, c):
        for row in self.pars_table:
            if row.line == line:
                row.category = c

    def remove_scope(self, scope):
        length = self.pars_table.__len__()
        for i in range(length):
            if self.pars_table[length - 1 - i].scope == scope:
                self.pars_table.pop()
            else:
                return

    def inc_func_args(self):
        for i in range(self.pars_table.__len__()):
            if self.pars_table[self.pars_table.__len__() - 1 - i].category == "func":
                self.pars_table[self.pars_table.__len__() - 1 - i].args_cells += 1
                return

    def get_adr(self, lexeme):
        for i in range(self.pars_table.__len__()):
            if self.pars_table[self.pars_table.__len__() - 1 - i].lexeme == lexeme:
                return self.pars_table[self.pars_table.__len__() - 1 - i].address

    def get_arr_temp(self, lexeme):
        pass

    def set_starting_line(self, lexeme, line):
        for i in range(self.pars_table.__len__()):
            if self.pars_table[self.pars_table.__len__() - 1 - i].lexeme == lexeme:
                self.pars_table[self.pars_table.__len__() - 1 - i].starting_line = line

    def get_starting_line(self, lexeme):
        for i in range(self.pars_table.__len__()):
            if self.pars_table[self.pars_table.__len__() - 1 - i].lexeme == lexeme:
                return self.pars_table[self.pars_table.__len__() - 1 - i].starting_line

    def find_adrs(self):
        adrs = []
        last_scope = -1
        for i in range(self.pars_table.__len__()):
            if last_scope == -1:
                last_scope = self.pars_table[self.pars_table.__len__() - 1 - i].scope
            if last_scope != self.pars_table[self.pars_table.__len__() - 1 - i].scope:
                return adrs
            adrs.append(self.pars_table[self.pars_table.__len__() - 1 - i].address)
        return adrs

    def get_func_args(self, lexeme):
        for i in range(self.pars_table.__len__()):
            if self.pars_table[self.pars_table.__len__() - 1 - i].lexeme == lexeme:
                return self.pars_table[self.pars_table.__len__() - 1 - i].args_cells


class SymbolRow:
    address = 0
    lexeme = ""
    args_cells = 0
    type = ""
    scope = ""
    starting_line = 0
    line = 0
    temp_start_pos = 0
    # func, var
    category = ""

    def __str__(self):
        return "address: " + str(self.address) + " lexeme: " + self.lexeme + " scope: " + str(self.scope)
