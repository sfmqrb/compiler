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
    print("\n[")
    for idx, t in enumerate(lsot):
        print(r"{idx:3}: {t}".format(idx=idx, t=t))
    print("]")


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


def get_next_token(token_tuple, line_number):
    global active_row, symbol_row, no_bracket_function, scope, gl_line_number
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
            # pars table
            if token_tuple[0] == 'KEYWORD' and (token_tuple[1] == "int" or token_tuple[1] == "void"):
                symbol_row.type = token_tuple[1]
                active_row = True
                if last_state.nterminal_id == "Type-specifier":
                    symbol_row.category = "var"
                elif last_state.nterminal_id == "Params":
                    if symbol_row.category != "param":
                        symbol_row.category = "param"
                        symbol_table.inc_func_args()
                else:
                    symbol_row.category = "var"
            if last_state.nterminal_id == "Fun-declaration-prime":
                no_bracket_function = True
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
                symbol_table.set_last_args(int(token_tuple[1]), TempManager.get_instance().get_arr_temp(int(token_tuple[1])))
            if token_tuple[1] == ';':
                symbol_table.check_void_var()

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
