import SemanticLevel.SymbolTable
from SemanticLevel import SemanticRoutines
from SemanticLevel.ErrorType import ErrorTypeEnum
from SemanticLevel import ErrorType
import SemanticLevel.ErrorType

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
        global semantic_instance
        if semantic_instance is None:
            semantic_instance = Semantic(
                SemanticLevel.SymbolTable.SymbolTableClass.get_instance())
        return semantic_instance

    def __init__(self, pars_table):
        global semantic_instance
        self.parse_table = pars_table
        self.temp_manager = TempManager(500, 4)
        semantic_instance = self
        print(r"    {:30} {:15} {}".format("func_name", "input_token", "Semantic Stack"))

    def run(self, func_name, input_token):
        print(
            r"==> {func_name:30} {input_token:15} {SemanticRoutines}".
            format(func_name=func_name[1:], input_token=input_token,
                   SemanticRoutines=SemanticRoutines.semantic_stack))
        func_name = func_name[1:len(func_name)]
        getattr(SemanticRoutines, "func_" +
                func_name)(self.temp_manager.get_temp, input_token)

    def error(self, err_type, id, expected=None, illegal=None, arg=None):
        line_number = str(ErrorType.gl_line_number)
        id = str(id)
        if err_type == ErrorTypeEnum.scoping:
            err = "#" + line_number + ": SemanticLevel Error! '" + id + "' is not defined"
        elif err_type == ErrorTypeEnum.void_type:
            err = "#" + line_number + ": SemanticLevel Error! Illegal type of void for '" + id + "'"
        elif err_type == ErrorTypeEnum.number_mathing:
            err = "#" + line_number + \
                  ":semantic error! Mismatch in numbers of arguments of '" + id + "'"
        elif err_type == ErrorTypeEnum.break_stmt:
            err = "#" + line_number + \
                  ": Semantic Error! No 'repeat ... until' found for 'break'."
        elif err_type == ErrorTypeEnum.type_mismatch:
            err = "#" + line_number + ": SemanticLevel Error! Type mismatch in operands, Got '" + \
                  illegal + "' instead of '" + expected + "'"
        elif err_type == ErrorTypeEnum.type_matching:
            err = "#" + line_number + ": SemanticLevel Error!Mismatch in type of argument " + str(arg) + \
                  " for '" + id + "'. Expected '" + expected + \
                  "' but got '" + illegal + "' instead "
        self.errors.append(err)
