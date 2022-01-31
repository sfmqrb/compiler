
semantic_stack = []
program_block = []
semantic_instance = None
EMPTY_PB = "( , , , )"


def get_PB_next():
    return len(program_block)

####################### Test Routines #########################


def test():
    print("xxx")


def func_test_pid(find_adr, get_temp, input_token):
    p = find_adr(input_token)
    semantic_stack.append(p)


def func_test_assign(find_adr, get_temp, input_token):
    program_block.append(
        "(ASSIGN," + str(semantic_stack.pop()) +
        "," + str(semantic_stack.pop()) + ",)"
    )


def func_test_add(find_adr, get_temp, input_token):
    t = get_temp()
    program_block.append(
        "(ADD,"
        + str(semantic_stack.pop())
        + ","
        + str(semantic_stack.pop())
        + ","
        + str(t)
        + ")"
    )
    semantic_stack.append(t)


def func_test_mult(find_adr, get_temp, input_token):
    t = get_temp()
    program_block.append(
        "(MULT,"
        + str(semantic_stack.pop())
        + ","
        + str(semantic_stack.pop())
        + ","
        + str(t)
        + ")"
    )
    semantic_stack.append(t)


####################### Main Routines #########################
def func_pid(find_adr, get_temp, input_token):
    p = find_adr(input_token)
    semantic_stack.append(p)
    pass


def func_pnum(find_adr, get_temp, input_token):
    semantic_stack.append("#" + input_token)
    pass


def func_assign(find_adr, get_temp, input_token):
    _from = semantic_stack.pop()
    _to = semantic_stack.pop()
    program_block.append(f"(ASSIGN, {str(_from)}, {str(_to)}, )")
    pass


def func_push(find_adr, get_temp, input_token):
    semantic_stack.append(input_token)
    pass


def func_add_op(find_adr, get_temp, input_token):
    right = semantic_stack.pop()
    action = "ADD" if semantic_stack.pop() == "+" else "SUB"
    left = semantic_stack.pop()
    t = get_temp()
    program_block.append(f"({action}, {str(left)}, {str(right)}, {str(t)})")
    semantic_stack.append(t)


def func_mult_op(find_adr, get_temp, input_token):
    first = semantic_stack.pop()
    action = "MULT"
    second = semantic_stack.pop()
    t = get_temp()
    program_block.append(f"({action}, {str(first)}, {str(second)}, {str(t)})")
    semantic_stack.append(t)


def func_comp_op(find_adr, get_temp, input_token):
    right = semantic_stack.pop()
    action = "EQ" if semantic_stack.pop() == "==" else "LT"
    left = semantic_stack.pop()
    t = get_temp()
    program_block.append(f"({action}, {str(left)}, {str(right)}, {str(t)})")
    semantic_stack.append(t)


def func_save(find_adr, get_temp, input_token):
    semantic_stack.append(get_PB_next())
    program_block.append(EMPTY_PB)


def func_jpf_save(find_adr, get_temp, input_token):
    i = get_PB_next()
    PBAddr = semantic_stack.pop()
    expression = semantic_stack.pop()
    program_block[PBAddr] = f"(JPF, {str(expression)}, {str(i+1)}, )"
    semantic_stack.append(i)
    program_block.append(EMPTY_PB)


def func_jp(find_adr, get_temp, input_token):
    i = get_PB_next()
    PBAddr = semantic_stack.pop()
    program_block[PBAddr] = f"(JP, {str(i)}, , )"


def func_jpf(find_adr, get_temp, input_token):
    i = get_PB_next()
    PBAddr = semantic_stack.pop()
    expression = semantic_stack.pop()
    program_block[PBAddr] = f"(JPF, {str(expression)}, {str(i)}, )"
