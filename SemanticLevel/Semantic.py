import enum

from SemanticLevel import SemanticRoutines

instance = None
SemanticRoutines.semantic_instance = instance


class ErrorType(enum.Enum):
    scoping = 1
    void_type = 2
    number_mathing = 3
    break_stmt = 4
    type_mismatch = 5
    type_matching = 6


class TempManager:
    current_temp = 0
    increase_amount = 0

    def __init__(self, current_temp, increase_amount):
        self.current_temp = current_temp
        self.increase_amount = increase_amount

    def get_temp(self):
        self.current_temp += self.increase_amount
        return self.current_temp


class Semantic:
    name_function_dict = {
    }
    parse_table = None
    temp_manager = None
    errors = []

    def __init__(self, pars_table):
        self.parse_table = pars_table
        self.temp_manager = TempManager(500, 4)
        instance = self

    def run(self, func_name, input_token):
        func_name = func_name[1:len(func_name)]
        try:
            getattr(SemanticRoutines, "func_" + func_name)(self.parse_table.get_adr, self.temp_manager.get_temp, input_token)
        except:
            pass

    def error(self, err_type, line_number, id, expected, illegal, arg):
        line_number = str(line_number)
        if err_type == ErrorType.scoping:
            err = "#" + line_number + ": SemanticLevel Error! '" + id + "' is not defined"
        elif err_type == ErrorType.void_type:
            err = "#" + line_number + ": SemanticLevel Error! Illegal type of void for '" + id + "'"
        elif err_type == ErrorType.number_mathing:
            err = "#" + line_number + ":semantic error! Mismatch in numbers of arguments of '" + id + "'"
        elif err_type == ErrorType.break_stmt:
            err = "#" + line_number + ": SemanticLevel Error! No 'while' or 'switch' found for 'break'"
        elif err_type == ErrorType.type_mismatch:
            err = "#" + line_number + ": SemanticLevel Error! Type mismatch in operands, Got '" + illegal + "' instead of '" + expected + "'"
        elif err_type == ErrorType.type_matching:
            err = "#" + line_number + ": SemanticLevel Error!Mismatch in type of argument " + arg + " for '" + id + "'. Expected '" + expected + "' but got '" + illegal + "' instead "
        self.errors.append(err)
