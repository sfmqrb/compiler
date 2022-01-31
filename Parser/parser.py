# For test
def pp_list_of_tuples(lsot):
    print("\n[")
    for t in lsot:
        print(r" {t}".format(t=t))
    print("]")


# Main imports
from Parser.grammer_to_transition import rule_to_states
from Parser.grammer_to_transition import fill_nterminal_id_dict
from Parser import DFA
import json
import jsonpickle
from SemanticLevel import ParsTable, Semantic
from SemanticLevel.SemanticRoutines import program_block

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

f = open("input1.txt", "r")
for line in f:
    line_counter += 1

# string = [('KEYWORD', 'void'), ('ID', 'main'), ('SYMBOL', '('), ('KEYWORD', 'void'), ('SYMBOL', ')'), ('SYMBOL', '{')
#     , ('KEYWORD', 'int'), ('ID', 'a'), ('SYMBOL', ';'),
#           ('KEYWORD', 'int'), ('ID', 'b'), ('SYMBOL', ';'),
#           ('ID', 'a'), ('SYMBOL', '='), ('ID', 'b'), ('SYMBOL', '+'), ('NUM', '1'), ('SYMBOL', ';'),
#           ('SYMBOL', '}'),'$']
# string = ['void', 'ID', '(', 'void', ')', '{', 'int', 'ID', ';', 'int', 'ID', ';', 'ID', '=', 'ID', '+', 'NUM', ';',
#           '}', '$']
DFA.states_stack.append(DFA.nterminal_first_state['Program'])
# DFA.states_stack.append(DFA.nterminal_first_state['P'])
pars_row = ParsTable.ParsRow()
pars_table = ParsTable.ParsTable()
semantic = Semantic.Semantic(pars_table)
active_row = False
# (started, ended, function dependent)
brackets = list()
no_bracket_function = False
scope = 0


def get_next_token(token_tuple, line_number):
    global active_row, pars_row, no_bracket_function, scope
    next_token = False
    while not next_token:
        last_state_id = DFA.states_stack[DFA.states_stack.__len__() - 1]
        last_state = DFA.id_state_dict[last_state_id]
        if token_tuple == '$':
            next_token, e = last_state.next_state('$', '$', line_counter, semantic)
            # break
        else:
            # pars table
            if token_tuple[0] == 'KEYWORD' and (token_tuple[1] == "int" or token_tuple[1] == "void"):
                pars_row.type = token_tuple[1]
                active_row = True
                if last_state.nterminal_id == "Type-specifier":
                    pars_row.category = "var"
                elif last_state.nterminal_id == "Params":
                    pars_row.category = "param"
                else:
                    pars_row.category = "var"
            if token_tuple[1] == "(":
                pars_table.set_line_category(line_number, "func")
            if token_tuple[0] == 'ID' and active_row:
                pars_row.lexeme = token_tuple[1]
                pars_row.line = line_number
                pars_row.scope = scope
                pars_table.add(pars_row)
                pars_row = ParsTable.ParsRow()
                active_row = False
            if token_tuple[0] == 'NUM' and last_state_id == 17:
                pars_table.set_last_args(int(token_tuple[1]))
            if token_tuple[1] == "{":
                brackets.append(no_bracket_function)
                if no_bracket_function:
                    scope += 1
                    no_bracket_function = False
            if token_tuple[1] == "}":
                pass
                # bracket = brackets.pop()
                # if bracket:
                #     scope -= 1
            if token_tuple[0] == 'KEYWORD' or token_tuple[0] == 'SYMBOL':
                token = token_tuple[1]
            else:
                token = token_tuple[0]
            next_token, e = last_state.next_state(token, token_tuple, line_number, semantic)
        if e is not None:
            errors.append(e)


def draw_tree():
    # print(pars_table.pars_table)

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
