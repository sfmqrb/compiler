from Semanric import SemanticRoutins


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
    name_function_dict = {}
    parse_table = None
    temp_manager = None

    def __init__(self, pars_table):
        self.parse_table = pars_table
        self.temp_manager = TempManager(500, 4)

    def run(self, func_name, input_token):
        print(func_name, input_token, SemanticRoutins.semantic_stack)
        func_name = func_name[1 : len(func_name)]
        getattr(SemanticRoutins, "func_" + func_name)(
            self.parse_table.get_adr, self.temp_manager.get_temp, input_token
        )
