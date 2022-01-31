from Semantic import instance

semantic_stack = []
program_block = []


def test():
    print("xxx")


def func_calc(find_adr, get_temp, input_token):
    find_adr('')
    get_temp()
    pass


def func_add(find_adr, get_temp, input_token):
    pass


def func_test_pid(find_adr, get_temp, input_token):
    p = find_adr(input_token)
    semantic_stack.append(p)


def func_test_assign(find_adr, get_temp, input_token):
    program_block.append("(ASSIGN," + str(semantic_stack.pop()) + "," + str(semantic_stack.pop()) + ",)")


def func_test_add(find_adr, get_temp, input_token):
    t = get_temp()
    program_block.append("(ADD," + str(semantic_stack.pop()) + "," + str(semantic_stack.pop()) + "," + str(t) + ")")
    semantic_stack.append(t)


def func_test_mult(find_adr, get_temp, input_token):
    t = get_temp()
    program_block.append("(MULT," + str(semantic_stack.pop()) + "," + str(semantic_stack.pop()) + "," + str(t) + ")")
    semantic_stack.append(t)
