from Parser import DFA

nterminal_id_dict = dict()
last_nterminal = ""
# State = DFA.State
rule = "Statement -> Expression-stmt | Compound-stmt | Selection-stmt | Iteration-stmt | Return-stmt"
grammar = "Program -> Declaration-list $@Declaration-list -> Declaration Declaration-list | EPSILON @Declaration -> Declaration-initial Declaration-prime@Declaration-initial ->  Type-specifier ID@Declaration-prime -> Fun-declaration-prime | Var-declaration-prime@Var-declaration-prime -> ; | [ NUM ] ; @Fun-declaration-prime ->  ( Params ) Compound-stmt@Type-specifier -> int | void@Params -> int ID Param-prime Param-list | void@Param-list -> , Param Param-list | EPSILON@Param -> Declaration-initial Param-prime@Param-prime -> [  ] | EPSILON@Compound-stmt -> { Declaration-list Statement-list }@Statement-list -> Statement Statement-list | EPSILON@Statement -> Expression-stmt | Compound-stmt | Selection-stmt | Iteration-stmt | Return-stmt@Expression-stmt -> Expression ; | break ; | ;@Selection-stmt -> if ( Expression ) Statement Else-stmt@Else-stmt -> endif | else Statement endif@Iteration-stmt -> repeat Statement until ( Expression ) @Return-stmt -> return Return-stmt-prime@Return-stmt-prime -> ; | Expression ;@Expression -> Simple-expression-zegond | ID B@B -> = Expression | [ Expression ] H | Simple-expression-prime@H -> = Expression | G D C@Simple-expression-zegond -> Additive-expression-zegond C@Simple-expression-prime -> Additive-expression-prime C@C -> Relop Additive-expression | EPSILON@Relop -> < | ==@Additive-expression -> Term D@Additive-expression-prime -> Term-prime D@Additive-expression-zegond -> Term-zegond D@D -> Addop Term D | EPSILON@Addop -> + | -@Term -> Factor G@Term-prime -> Factor-prime G@Term-zegond -> Factor-zegond G@G -> * Factor G | EPSILON@Factor -> ( Expression ) | ID Var-call-prime | NUM@Var-call-prime -> ( Args ) | Var-prime@Var-prime -> [ Expression ] | EPSILON@Factor-prime -> ( Args ) | EPSILON@Factor-zegond -> ( Expression ) | NUM@Args -> Arg-list | EPSILON@Arg-list -> Expression Arg-list-prime@Arg-list-prime -> , Expression Arg-list-prime | EPSILON"
# line = (f.readline())
i = 0
for line in grammar.split("@"):
    nterminal_id_dict[line.split()[0]] = i
    i += 1


def is_terminal(element):
    global last_nterminal
    if nterminal_id_dict.__contains__(element):
        last_nterminal = element
        return nterminal_id_dict[element]
    return -1


state_id_index = 0


def rule_to_states(State, rule):
    global state_id_index
    rule_list = rule.split(' ->')
    main_nterminal = rule_list[0]
    # main_nterminal_id = nterminal_id_dict[main_nterminal]
    first_state_id = state_id_index + 1
    state_id_index += 1
    DFA.nterminal_first_state[main_nterminal] = first_state_id
    final_state_id = state_id_index + 1
    state_id_index += 1
    State(final_state_id, 0, dict(), {}, True)
    first_state_terminal_trans = dict()
    first_state_nterminal_trans = set()
    righties = rule_list[1].split("|")
    for righty in righties:
        # state_id = state_id_index + 1
        # state_id_index += 1
        righty_list = righty.split()
        for i in range(len(righty_list)):
            if righty_list[i] == 'EPSILON':
                righty_list[i] = ''
            if i == 0:
                state_id = first_state_id
            else:
                state_id = state_id_index + 1
                state_id_index += 1
            if i == len(righty_list) - 1:
                next_state_id = final_state_id
            else:
                next_state_id = state_id_index + 1
                # state_id_index += 1

            nterminal_id = is_terminal(righty_list[i])
            state_terminal_trans = dict()
            state_nterminal_trans = set()
            if i == 0:
                state_terminal_trans = first_state_terminal_trans
                state_nterminal_trans = first_state_nterminal_trans
            if nterminal_id == -1:
                state_terminal_trans[righty_list[i]] = next_state_id
            else:
                state_nterminal_trans.add((righty_list[i], next_state_id))
                # DFA.state_id_nterminal_dict[state_id] = righty_list[i]
            if i != 0:
                State(state_id, last_nterminal, state_terminal_trans, state_nterminal_trans, False)
    State(first_state_id, main_nterminal, first_state_terminal_trans, first_state_nterminal_trans, False)
