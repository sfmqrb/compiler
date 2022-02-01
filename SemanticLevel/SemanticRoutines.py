from gettext import find
from glob import glob

from matplotlib.pyplot import get
import stacks as sf
sss = sf.SnapshotStack()
frs = sf.FunctionRelatedStack()

semantic_stack = []
program_block = []
semantic_instance = None
EMPTY_PB = "( , , , )"
WORD_SIZE = 4
ARG_COUNT = 0


# should imported
def get_arg_count_last():
    pass


# should imported
def find_adrs():
    pass


def get_PB_next():
    return len(program_block)

####################### Main Routines #########################


# related to function call to handle SnapshotStack
def _save_snapshot(find_adr, get_temp, input_token):
    last_scope_addrs = find_adrs()
    for addr in last_scope_addrs:
        sss.push(addr, program_block)


def _restore_snapshot(find_adr, get_temp, input_token):
    last_scope_addrs = find_adrs()
    for addr in last_scope_addrs[::-1]:
        pop_addr = sss.pop(addr)
        program_block.append(f"(assign, {str(pop_addr)}, {str(addr)}, )")


# function call
def func_call_begin(find_adr, get_temp, input_token):
    global ARG_COUNT
    ARG_COUNT = 0
    _save_snapshot(find_adr, get_temp, input_token)


def func_call_add_args(find_adr, get_temp, input_token):
    global ARG_COUNT
    ARG_COUNT += 1
    # todo push to SemanticStack calling args
    arg = semantic_stack.pop()
    frs.push(arg)


def func_call_end(find_adr, get_temp, input_token):
    global ARG_COUNT
    # encountered JP operation so + 7 is needed
    return_adr = get_PB_next() + 7

    frs.push(ARG_COUNT, program_block)          # push arg_count
    frs.push(return_adr, program_block)         # push ra

    function_id = semantic_stack.pop()
    function_addr = find_adr(function_id)  # direct like line 6 or line 20

    program_block.append(f"(JP, {function_addr}, , )")
    _restore_snapshot(find_adr, get_temp, input_token)

    rv = frs.pop(program_block)
    frs.pop(program_block, _assign_=False)
    frs.pop(program_block, _assign_=False)
    # addr of return value stored in semantic_stack
    semantic_stack.append(rv)
    for _ in range(ARG_COUNT):
        frs.pop(program_block, _assign_=False)  # pop input args
    ARG_COUNT = 0


# function declaration
def func_declaration_after_header(find_adr, get_temp, input_token):
    arg_count = get_arg_count_last()

    for first_arg_offset in range(3, 2+arg_count):
        arg = semantic_stack.pop()
        t = frs.access_using_offset(first_arg_offset, program_block, get_temp)
        program_block.append(f"(ASSIGN, {str(t)}, {str(arg)}, )")


# function return
def func_declaration_after_return(find_adr, get_temp, input_token):
    rv = semantic_stack.pop()
    frs.push(rv, program_block)
    ra = frs.access_using_offset(2, program_block, get_temp)
    program_block.append(f"(JP, @{ra}, , )")


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
    semantic_stack.append(_to)


def func_push(find_adr, get_temp, input_token):
    semantic_stack.append(input_token)
    pass


def func_add_op(find_adr, get_temp, input_token, address_mode=False):
    addrTrue = "@" if address_mode else ""
    imdtTrue = "#" if address_mode else ""
    right = semantic_stack.pop()
    action = "ADD" if semantic_stack.pop() == "+" else "SUB"
    left = semantic_stack.pop()
    t = get_temp()
    program_block.append(
        f"({action}, {str(left)}, {imdtTrue}{str(right)}, {str(t)})")
    semantic_stack.append(f"{addrTrue}{str(t)}")


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


def func_label(find_adr, get_temp, input_token):
    i = get_PB_next()
    semantic_stack.append(i)


def func_until(find_adr, get_temp, input_token):
    left = semantic_stack.pop()
    right = semantic_stack.pop()
    program_block.append(f"(JPF, {str(left)}, {str(right)}, )")


def func_parr(find_adr, get_temp, input_token):
    arr_index = str(semantic_stack.pop())
    arr_id = str(semantic_stack.pop())

    # semantic_stack.append(arr_index)
    semantic_stack.append(f"@{arr_index}")
    semantic_stack.append(f"#{WORD_SIZE}")
    func_mult_op(find_adr, get_temp, None)

    semantic_stack.append("+")
    semantic_stack.append(arr_id)
    func_add_op(find_adr, get_temp, None, address_mode=True)


def func_pop(find_adr, get_temp, input_token):
    semantic_stack.pop()
