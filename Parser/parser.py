# For test
from SemanticLevel.SemanticRoutines import program_block
from SemanticLevel import SymbolTable, Semantic
from SemanticLevel.Semantic import TempManager
import jsonpickle
import json
from Parser import DFA
from Parser.grammer_to_transition import fill_nterminal_id_dict
from Parser.grammer_to_transition import rule_to_states


def pp_list_of_tuples(lsot):
    f = open("output.txt", "w")
    s = ""
    print("\n[")
    for idx, t in enumerate(lsot):
        s += f"{idx}\t{t}\n"
        print(r"{idx:3}: {t}".format(idx=idx, t=t))
    print("]")
    f.write(s)


# Main imports

errors = []
f = open("grammer.txt", "r")
# f = open("c-minus_001 (1).txt", "r")
# f = open("test_grammer", "r")
line_counter = 1
grammar = f.read()
fill_nterminal_id_dict(grammar)
for line in grammar.split("\n"):
    rule_to_states(DFA.State, line)
# save transitions in json
DFA.save_states()
# DFA.load_state()

f = open("input.txt", "r")
for line in f:
    line_counter += 1
DFA.states_stack.append(DFA.nterminal_first_state['Program'])
# DFA.states_stack.append(DFA.nterminal_first_state['P'])
symbol_row = SymbolTable.SymbolRow()
symbol_table = SymbolTable.SymbolTableClass.get_instance()
semantic = Semantic.Semantic.get_instance()
active_row = False
# (started, ended, function dependent)
brackets = list()
no_bracket_function = False
scope = 0
gl_line_number = 0
func_declare_started = False

func_in_call = False
call_params = []
parameter_counted = False
count_params = 0
function_row = None


def get_next_token(token_tuple, line_number):
    global active_row, symbol_row, no_bracket_function, scope, gl_line_number, func_in_call, count_params, parameter_counted, call_params, func_declare_started, function_row
    gl_line_number = line_number
    next_token = False
    if token_tuple != "$":
        if token_tuple[1] == "{":
            brackets.append(no_bracket_function)
            if no_bracket_function:
                # scope += 1
                no_bracket_function = False
        if token_tuple[1] == "}":
            bracket = brackets.pop()
            if bracket:
                symbol_table.check_void_var()
                symbol_table.remove_scope(scope)
                scope -= 1
    while not next_token:
        last_state_id = DFA.states_stack[DFA.states_stack.__len__() - 1]
        last_state = DFA.id_state_dict[last_state_id]
        if token_tuple == '$':
            next_token, e = last_state.next_state(
                '$', '$', line_counter, semantic)
            # break
        else:
            # error-check

            # function parameter number error check
            if token_tuple[0] == 'ID' and last_state.nterminal_id == "Expression":
                row = symbol_table.get_row(token_tuple[1])
                if row.category == "func":
                    function_row = row
                    func_in_call = True
            elif token_tuple[0] == 'ID' and func_in_call:
                param_row: SymbolTable.SymbolRow
                param_row = symbol_table.get_row(token_tuple[1])
                if param_row.category == "var" and not parameter_counted:
                    call_params.append(param_row)
                    parameter_counted = True
                    count_params += 1
            elif token_tuple[0] == 'NUM' and func_in_call:
                param_row = SymbolTable.SymbolRow()
                param_row.args_cells = 0
                param_row.lexeme = str(token_tuple[1])
                param_row.category = "var"
                param_row.type = "int"
                if not parameter_counted:
                    call_params.append(param_row)
                    parameter_counted = True
                    count_params += 1
            if token_tuple[1] == ',' and func_in_call:
                parameter_counted = False
            if token_tuple[1] == ')' and last_state.nterminal_id == "Arg-list-prime" and func_in_call:
                # finish func call
                # check for errors
                if call_params.__len__() == function_row.params_type.__len__():
                    pass
                    for i in range(call_params.__len__()):
                        if call_params[i].is_arr != function_row.params_type[i].is_arr:
                            expected = "array" if function_row.params_type[i].is_arr else "int"
                            illegal = "array" if call_params[i].is_arr else "int"
                            Semantic.Semantic.get_instance().error(SymbolTable.ErrorTypeEnum.type_matching,
                                                                   function_row.lexeme, illegal=illegal, arg=i + 1,
                                                                   expected=expected)
                else:
                    Semantic.Semantic.get_instance().error(SymbolTable.ErrorTypeEnum.number_mathing,
                                                           function_row.lexeme, )
                func_in_call = False
                call_params.clear()

            # pars table
            if token_tuple[0] == 'KEYWORD' and (token_tuple[1] == "int" or token_tuple[1] == "void"):
                if last_state.nterminal_id == "Params" and token_tuple[1] == "void":
                    # todo fosh?
                    pass
                else:
                    symbol_row.type = token_tuple[1]
                    active_row = True
                    if last_state.nterminal_id == "Type-specifier":
                        if symbol_row.category != "param":
                            symbol_row.category = "var"
                    elif last_state.nterminal_id == "Params" or func_declare_started:
                        func_declare_started = True
                        if symbol_row.category != "param":
                            symbol_row.category = "param"
                            symbol_table.inc_func_args(symbol_row)

            if last_state.nterminal_id == "Fun-declaration-prime":
                no_bracket_function = True
                func_declare_started = False
                symbol_table.set_line_category(line_number, "func")
                scope += 1
            if token_tuple[0] == 'ID' and active_row:
                symbol_row.lexeme = token_tuple[1]
                symbol_row.line = line_number
                symbol_row.scope = scope
                symbol_table.add(symbol_row)
                symbol_row = SymbolTable.SymbolRow()
                active_row = False
            if token_tuple[0] == 'NUM' and last_state.nterminal_id == "Var-declaration-prime":
                symbol_table.set_last_args(int(token_tuple[1]),
                                           TempManager.get_instance().get_arr_temp(int(token_tuple[1])))
            if token_tuple[1] == ';':
                symbol_table.check_void_var()
            if token_tuple[1] == ']' and func_declare_started:
                symbol_table.set_last_args(0, 0)
            if token_tuple[1] == ')':
                func_declare_started = False

            if token_tuple[0] == 'KEYWORD' or token_tuple[0] == 'SYMBOL':
                token = token_tuple[1]
            else:
                token = token_tuple[0]
            next_token, e = last_state.next_state(
                token, token_tuple, line_number, semantic)
        if e is not None:
            errors.append(e)


def draw_tree():
    # print(pars_table.pars_table)

    x = Semantic.Semantic.errors
    print("semantic errors: ")
    print(x)
    pp_list_of_tuples(program_block)

    a = ""
    for pre, fill, node in DFA.RenderTree(DFA.first_node):
        p = ("%s%s" % (pre, node.name))
        x = "'"
        p = p.replace(x, "")
        a += p + "\n"
    return a[0:a.__len__() - 1]


def get_pars_errors():
    return errors
