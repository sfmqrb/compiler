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
grammar = \
    "Program -> Declaration-list #at_the_end $@Declaration-list -> Declaration Declaration-list | EPSILON@Declaration -> Declaration-initial Declaration-prime@Declaration-initial ->  Type-specifier #pid ID@Declaration-prime -> #save_first_func Fun-declaration-prime | Var-declaration-prime @Var-declaration-prime -> #set_tmp_value ; | [ NUM ] #set_tmp_addr #pop ;@Fun-declaration-prime ->  #set_starting_line ( Params ) #declaration_after_header Compound-stmt #push_zero #declaration_after_return #after_func_declaration@Type-specifier -> int | void@Params -> int #pid ID Param-prime Param-list | void@Param-list -> , Param Param-list | EPSILON@Param -> Declaration-initial Param-prime@Param-prime -> [  ] | EPSILON@Compound-stmt -> { Declaration-list Statement-list }@Statement-list -> Statement Statement-list | EPSILON@Statement -> Expression-stmt | Compound-stmt | Selection-stmt | Iteration-stmt | Return-stmt | output ( Expression #output ) ;@Expression-stmt -> Expression ; #pop | #break break ; | ;@Selection-stmt -> if ( Expression ) #save Statement Else-stmt@Else-stmt -> endif #jpf | else #jpf_save Statement endif #jp@Iteration-stmt -> repeat #label Statement until ( Expression ) #until@Return-stmt -> return Return-stmt-prime @Return-stmt-prime -> #push_zero #declaration_after_return ; | Expression #declaration_after_return ;@Expression -> Simple-expression-zegond | #pid ID B@B -> = Expression #assign | [ Expression #parr ] H | Simple-expression-prime@H -> = Expression #assign | G D C@Simple-expression-zegond -> Additive-expression-zegond C@Simple-expression-prime -> Additive-expression-prime C@C -> #push Relop Additive-expression #comp_op | EPSILON@Relop -> < | ==@Additive-expression -> Term D@Additive-expression-prime -> Term-prime D@Additive-expression-zegond -> Term-zegond D@D ->  #push Addop Term #add_op D | EPSILON@Addop -> + | -@Term -> Factor G@Term-prime -> Factor-prime G@Term-zegond -> Factor-zegond G@G -> * Factor #mult_op G | EPSILON@Factor -> ( Expression ) | #pid ID Var-call-prime | #pnum NUM@Var-call-prime -> ( #call_begin Args #call_end ) | Var-prime@Var-prime -> [ Expression #parr ] | EPSILON@Factor-prime -> ( #call_begin Args #call_end ) | EPSILON@Factor-zegond -> ( Expression ) | #pnum NUM@Args -> Arg-list | EPSILON@Arg-list -> Expression #call_add_args Arg-list-prime@Arg-list-prime -> , Expression #call_add_args Arg-list-prime | EPSILON"

fill_nterminal_id_dict(grammar)
for line in grammar.split("@"):
    rule_to_states(DFA.State, line)


f = open("input.txt", "r")
for line in f:
    line_counter += 1
DFA.states_stack.append(DFA.nterminal_first_state['Program'])
# DFA.states_stack.append(DFA.nterminal_first_state['P'])
symbol_row = SymbolTable.SymbolRow()
symbol_table = SymbolTable.SymbolTableClass.get_instance()
semantic = Semantic.Semantic.get_instance()
active_row = False

brackets = list()
no_bracket_function = False
scope = 0
gl_line_number = 0
func_declare_started = False
func_call_table_list = []
func_in_call = False

arrays_stack = []


def get_next_token(token_tuple, line_number):
    global active_row, symbol_row, no_bracket_function, scope, gl_line_number, func_in_call, count_params, parameter_counted, call_params, func_declare_started, function_row, arrays_stack
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
        # check for type missmatch error
        if token_tuple[0] == 'ID':
            id_row = symbol_table.get_row(token_tuple[1])
            if id_row is not None and id_row.is_arr and id_row.category == "var":
                arrays_stack.append(id_row)
        if token_tuple[1] == ']':
            if arrays_stack.__len__() > 0:
                arrays_stack.pop()
        if token_tuple[1] == ';' or token_tuple[1] == ')':
            if arrays_stack.__len__() > 0:
                Semantic.Semantic.get_instance().error(SymbolTable.ErrorTypeEnum.type_mismatch, arrays_stack[0].lexeme,
                                                       illegal="array", expected="int")
                arrays_stack.pop()
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
            if token_tuple[0] == 'ID' and last_state.terminal_trans.keys().__contains__("#pid") and token_tuple[
                1] != "output":
                row = symbol_table.get_row(token_tuple[1])
                if row is not None and row.category == "func":
                    fcb = SymbolTable.FuncCallBlock(row)
                    func_call_table_list.append(fcb)
                    a = 1
            elif token_tuple[0] == 'ID' and func_call_table_list.__len__() > 0 and token_tuple[1] != "output":
                param_row: SymbolTable.SymbolRow
                param_row = symbol_table.get_row(token_tuple[1])
                if func_call_table_list[-1].start_param:
                    if param_row in arrays_stack:
                        arrays_stack.remove(param_row)
                    func_call_table_list[func_call_table_list.__len__() - 1].add_param_row(param_row)
            elif token_tuple[0] == 'NUM' and func_call_table_list.__len__() > 0 and token_tuple[1] != "output":
                param_row = SymbolTable.SymbolRow()
                param_row.args_cells = 0
                param_row.lexeme = str(token_tuple[1])
                param_row.category = "var"
                param_row.type = "int"
                func_call_table_list[func_call_table_list.__len__() - 1].add_param_row(param_row)
            if token_tuple[1] == ',' and func_call_table_list.__len__() > 0:
                func_call_table_list[func_call_table_list.__len__() - 1].next_param()
            if token_tuple[1] == '(' and func_call_table_list.__len__() > 0:
                func_call_table_list[func_call_table_list.__len__() - 1].start_param = True
            if token_tuple[1] == ')' \
                    and last_state.nterminal_id == "Arg-list-prime" and func_call_table_list.__len__() > 0:
                # finish func call
                # check for errors
                func_call_table = func_call_table_list.pop()
                if func_call_table.call_params.__len__() == func_call_table.function_row.params_type.__len__():
                    for i in range(func_call_table.call_params.__len__()):
                        if func_call_table.call_params[i].is_arr != func_call_table.function_row.params_type[i].is_arr:
                            expected = "array" if func_call_table.function_row.params_type[i].is_arr else "int"
                            illegal = "array" if func_call_table.call_params[i].is_arr else "int"
                            Semantic.Semantic.get_instance().error(SymbolTable.ErrorTypeEnum.type_matching,
                                                                   func_call_table.function_row.lexeme, illegal=illegal,
                                                                   arg=i + 1,
                                                                   expected=expected)
                else:
                    Semantic.Semantic.get_instance().error(SymbolTable.ErrorTypeEnum.number_mathing,
                                                           func_call_table.function_row.lexeme, )

            # pars table
            if token_tuple[0] == 'KEYWORD' and (token_tuple[1] == "int" or token_tuple[1] == "void"):
                if last_state.nterminal_id == "Params" and token_tuple[1] == "void":
                    # void in function input
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
            if token_tuple[1] == "output":
                token = "output"
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
