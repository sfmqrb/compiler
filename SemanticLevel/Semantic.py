from SemanticLevel import SemanticRoutines
from SemanticLevel.ErrorType import ErrorType
from SemanticLevel import ErrorType

semantic_instance = None
temp_instance = None


class TempManager:
    current_temp = 0
    increase_amount = 0

    @staticmethod
    def get_instance():
        return temp_instance

    def __init__(self, current_temp, increase_amount):
        global temp_instance
        self.current_temp = current_temp
        self.increase_amount = increase_amount
        temp_instance = self

    def get_temp(self):
        self.current_temp += self.increase_amount
        return self.current_temp

    def get_arr_temp(self, arr_len):
        self.current_temp += self.increase_amount
        start_point = self.current_temp
        self.current_temp += self.increase_amount * (arr_len - 1)
        return start_point


class Semantic:
    name_function_dict = {
    }
    parse_table = None
    temp_manager = None
    errors = []

    @staticmethod
    def get_instance():
        return semantic_instance

    def __init__(self, pars_table):
        global semantic_instance
        self.parse_table = pars_table
        self.temp_manager = TempManager(500, 4)
        semantic_instance = self
        print(r"    {:15} {:15} {}".format(
            "func_name", "input_token", "Semantic Stack"))

    def run(self, func_name, input_token):
        print(
            r"==> {func_name:15} {input_token:15} {SemanticRoutines}".
                format(func_name=func_name[1:], input_token=input_token,
                       SemanticRoutines=SemanticRoutines.semantic_stack))
        func_name = func_name[1:len(func_name)]
        try:
            getattr(SemanticRoutines, "func_" + func_name)(self.parse_table.get_adr,
                                                           self.temp_manager.get_temp, input_token)
        except:
            pass

    def error(self, err_type, id, expected, illegal, arg):
        line_number = str(ErrorType.gl_line_number)
        t = err_type == ErrorType.scoping
        if t:
            err = "#" + line_number + ": SemanticLevel Error! '" + id + "' is not defined"
        elif err_type == ErrorType.void_type:
            err = "#" + line_number + ": SemanticLevel Error! Illegal type of void for '" + id + "'"
        elif err_type == ErrorType.number_mathing:
            err = "#" + line_number + \
                  ":semantic error! Mismatch in numbers of arguments of '" + id + "'"
        elif err_type == ErrorType.break_stmt:
            err = "#" + line_number + \
                  ": SemanticLevel Error! No 'while' or 'switch' found for 'break'"
        elif err_type == ErrorType.type_mismatch:
            err = "#" + line_number + ": SemanticLevel Error! Type mismatch in operands, Got '" + \
                  illegal + "' instead of '" + expected + "'"
        elif err_type == ErrorType.type_matching:
            err = "#" + line_number + ": SemanticLevel Error!Mismatch in type of argument " + arg + \
                  " for '" + id + "'. Expected '" + expected + \
                  "' but got '" + illegal + "' instead "
        self.errors.append(err)
