from Parser.grammer_to_transition import rule_to_states
from Parser import DFA
import json
import jsonpickle
from Semanric import parse_table

errors = []
# f = open("c-minus_001 (1).txt", "r")
line_counter = 1
grammar = "Program -> Declaration-list $@Declaration-list -> Declaration Declaration-list | EPSILON @Declaration -> Declaration-initial Declaration-prime@Declaration-initial ->  Type-specifier ID@Declaration-prime -> Fun-declaration-prime | Var-declaration-prime@Var-declaration-prime -> ; | [ NUM ] ; @Fun-declaration-prime ->  ( Params ) Compound-stmt@Type-specifier -> int | void@Params -> int ID Param-prime Param-list | void@Param-list -> , Param Param-list | EPSILON@Param -> Declaration-initial Param-prime@Param-prime -> [  ] | EPSILON@Compound-stmt -> { Declaration-list Statement-list }@Statement-list -> Statement Statement-list | EPSILON@Statement -> Expression-stmt | Compound-stmt | Selection-stmt | Iteration-stmt | Return-stmt@Expression-stmt -> Expression ; | break ; | ;@Selection-stmt -> if ( Expression ) Statement Else-stmt@Else-stmt -> endif | else Statement endif@Iteration-stmt -> repeat Statement until ( Expression ) @Return-stmt -> return Return-stmt-prime@Return-stmt-prime -> ; | Expression ;@Expression -> Simple-expression-zegond | ID B@B -> = Expression | [ Expression ] H | Simple-expression-prime@H -> = Expression | G D C@Simple-expression-zegond -> Additive-expression-zegond C@Simple-expression-prime -> Additive-expression-prime C@C -> Relop Additive-expression | EPSILON@Relop -> < | ==@Additive-expression -> Term D@Additive-expression-prime -> Term-prime D@Additive-expression-zegond -> Term-zegond D@D -> Addop Term D | EPSILON@Addop -> + | -@Term -> Factor G@Term-prime -> Factor-prime G@Term-zegond -> Factor-zegond G@G -> * Factor G #mult| EPSILON@Factor -> ( Expression ) | ID Var-call-prime | NUM@Var-call-prime -> ( Args ) | Var-prime@Var-prime -> [ Expression ] | EPSILON@Factor-prime -> ( Args ) | EPSILON@Factor-zegond -> ( Expression ) | NUM@Args -> Arg-list | EPSILON@Arg-list -> Expression Arg-list-prime@Arg-list-prime -> , Expression Arg-list-prime | EPSILON"

for line in grammar.split("@"):
    rule_to_states(DFA.State, line)
# save transitions in json
DFA.save_states()
# DFA.load_state()

f = open("input.txt", "r")
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
pars_row = parse_table.ParsRow()
pars_table = parse_table.ParsTable()
active_row = False

def get_next_token(token_tuple, line_number):
    global active_row, pars_row
    next_token = False
    while not next_token:
        last_state_id = DFA.states_stack[DFA.states_stack.__len__() - 1]
        last_state = DFA.id_state_dict[last_state_id]
        if token_tuple == '$':
            next_token, e = last_state.next_state('$', '$', line_counter)
            # break
        else:
            # pars table
            if token_tuple[0] == 'KEYWORD' and (token_tuple[1] == "int" or token_tuple[1] == "void"):
                pars_row.type = token_tuple[1]
                active_row = True
                if last_state_id == 25:
                    pars_row.category = "var"
                elif last_state_id == 27:
                    pars_row.category = "param"
                else:
                    pars_row.category = "var"
            if token_tuple[1] == "(":
                pars_table.set_line_category(line_number, "func")
            if token_tuple[0] == 'ID' and active_row:
                pars_row.lexeme = token_tuple[1]
                pars_row.line = line_number
                pars_table.add(pars_row)
                pars_row = parse_table.ParsRow()
                active_row = False
            if token_tuple[0] == 'NUM' and last_state_id == 17:
                pars_table.set_last_args(int(token_tuple[1]))
            if token_tuple[0] == 'KEYWORD' or token_tuple[0] == 'SYMBOL':
                token = token_tuple[1]
            else:
                token = token_tuple[0]
            next_token, e = last_state.next_state(token, token_tuple, line_number)
        if e is not None:
            errors.append(e)


def draw_tree():
    print(pars_table.pars_table)
    a = ""
    for pre, fill, node in DFA.RenderTree(DFA.first_node):
        p = ("%s%s" % (pre, node.name))
        x = "'"
        p = p.replace(x, "")
        a += p + "\n"
    return a[0:a.__len__() - 1]


def get_pars_errors():
    return errors
