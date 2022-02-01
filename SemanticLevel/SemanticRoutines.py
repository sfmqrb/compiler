from gettext import find
from glob import glob
import stacks as sf
sss = sf.SnapshotStack()
frs = sf.FunctionRelatedStack()

semantic_stack = []
program_block = []
semantic_instance = None
EMPTY_PB = "( , , , )"
WORD_SIZE = 4
ARG_COUNT = 0


def get_PB_next():
    return len(program_block)

####################### Main Routines #########################


# related to function call handling SnapshotStack
def _save_snapshot(find_adr, get_temp, input_token, find_adrs=None):
    last_scope_addrs = find_adrs()
    for addr in last_scope_addrs:
        sss.push(addr, program_block)


def _restore_snapshot(find_adr, get_temp, input_token, find_adrs=None):
    last_scope_addrs = find_adrs()
    for addr in last_scope_addrs[::-1]:
        pop_addr = sss.pop(addr)
        program_block.append(f"(assign, {str(pop_addr)}, {str(addr)}, )")


# function call
def func_call_begin(find_adr, get_temp, input_token, find_adrs=None):
    global ARG_COUNT
    _save_snapshot(find_adr, get_temp, input_token, find_adrs)
    ARG_COUNT = 0


def func_call_add_args(find_adr, get_temp, input_token):
    global ARG_COUNT
    ARG_COUNT += 1
    arg = semantic_stack.pop()
    frs.push(arg)


def func_call_end(find_adr, get_temp, input_token, find_adrs=None):
    global ARG_COUNT
    # encountered JP operation so + 1 is needed
    return_adr = get_PB_next() + 1

    frs.push("#0", program_block)               # push rv
    frs.push(return_adr, program_block)         # push ra
    frs.push(ARG_COUNT, program_block)          # push arg_count

    function_id = semantic_stack.pop()
    function_addr = find_adr(function_id)  # direct like line 6 or line 20

    program_block.append(f"(JP, {function_addr}, , )")
    _restore_snapshot(find_adr, get_temp, input_token, find_adrs)
    # pop arg_count
    frs.pop(program_block, _assign_=False)
    # pop ra
    frs.pop(program_block, _assign_=False)
    # pop rv
    pop_addr = frs.pop(program_block)
    # addr of return value stored in semantic_stack
    semantic_stack.append(pop_addr)
    for _ in range(ARG_COUNT):
        frs.pop(program_block, _assign_=False)  # pop input args
    ARG_COUNT = 0


# TODO function declaration
def func_declaration_start(find_adr, get_temp, input_token):
    arg_count = arg

# TODO function return


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
