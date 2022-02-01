from gettext import find
from glob import glob

import SemanticLevel.Semantic
from SemanticLevel.SymbolTable import SymbolTableClass
from SemanticLevel.ErrorType import ErrorTypeEnum
from matplotlib.pyplot import get
import SemanticLevel.stacks as sf

semantic_stack = []
program_block = []
ru_stack = []
semantic_instance = None
EMPTY_PB = "( , , , )"
WORD_SIZE = 4
ARG_COUNT = 0
FIRST_FUNC = False

st = SymbolTableClass.get_instance()
semantic = SemanticLevel.Semantic.Semantic.get_instance()
sss = sf.SnapshotStack(program_block)
frs = sf.FunctionRelatedStack(program_block)


def get_PB_next():
    return len(program_block)


####################### Main Routines #########################


# related to function call to handle SnapshotStack
def _save_snapshot(get_temp, input_token):
    last_scope_addrs = st.find_adrs()
    for addr in last_scope_addrs:
        sss.push(addr, program_block)


def _restore_snapshot(get_temp, input_token):
    last_scope_addrs = st.find_adrs()
    for addr in last_scope_addrs[::-1]:
        pop_addr = sss.pop(program_block)
        program_block.append(f"(ASSIGN, {str(pop_addr)}, {str(addr)}, )")


def func_set_starting_line(get_temp, input_token):
    # TODO:
    return st.set_starting_line(program_block.__len__())
    pass


# function call


def func_call_begin(get_temp, input_token):
    global ARG_COUNT
    ARG_COUNT = 0
    _save_snapshot(get_temp, input_token)


def func_call_add_args(get_temp, input_token):
    global ARG_COUNT
    ARG_COUNT += 1
    # todo push to SemanticStack calling args
    arg = semantic_stack.pop()
    # print(arg)
    frs.push(arg, program_block)


def func_call_end(get_temp, input_token):
    global ARG_COUNT
    # encountered JP operation so +5 is needed
    return_adr = get_PB_next() + 5

    frs.push(f"#{ARG_COUNT}", program_block)  # push arg_count
    frs.push(f"#{return_adr}", program_block)  # push ra

    function_id = semantic_stack.pop()
    # function_addr = find_adr(function_id)  # direct like line 6 or line 20
    function_addr = st.get_starting_line(
        function_id)  # direct like line 6 or line 20

    program_block.append(f"(JP, {function_addr}, , )")
    _restore_snapshot(get_temp, input_token)

    rv = frs.pop(program_block)
    frs.pop(program_block, _assign_=False)
    frs.pop(program_block, _assign_=False)
    # addr of return value stored in semantic_stack
    semantic_stack.append(rv)
    for _ in range(ARG_COUNT):
        frs.pop(program_block, _assign_=False)  # pop input args
    ARG_COUNT = 0


# function declaration
def func_declaration_after_header(get_temp, input_token):
    arg_count = st.get_func_args()
    for first_arg_offset in range(3, 3 + arg_count):
        arg = semantic_stack.pop()
        t = frs.access_using_offset(first_arg_offset, program_block, get_temp)
        program_block.append(f"(ASSIGN, {str(t)}, {str(st.get_adr(arg))}, )")


def func_push_zero(get_temp, input_token):
    semantic_stack.append("#0")

# function return


def func_declaration_after_return(get_temp, input_token):
    rv = semantic_stack.pop()
    print("rv", rv)
    addr_rv = st.get_adr(rv)
    frs.push(addr_rv, program_block)
    ra = frs.access_using_offset(2, program_block, get_temp)
    program_block.append(f"(JP, @{ra}, , )")


def func_pid(get_temp, input_token):
    p = st.get_adr(input_token)
    if p is None:
        semantic.error(ErrorTypeEnum.scoping, input_token)
    semantic_stack.append(input_token)
    pass


def func_pnum(get_temp, input_token):
    semantic_stack.append("#" + input_token)
    pass


def func_assign(get_temp, input_token):
    _from = semantic_stack.pop()
    _to = semantic_stack.pop()
    program_block.append(f"(ASSIGN, {str(_from)}, {str(_to)}, )")
    semantic_stack.append(_to)


def func_push(get_temp, input_token):
    semantic_stack.append(input_token)
    pass


def func_add_op(get_temp, input_token, address_mode=False):
    addrTrue = "@" if address_mode else ""
    imdtTrue = ""
    right = semantic_stack.pop()
    action = "ADD" if semantic_stack.pop() == "+" else "SUB"
    left = semantic_stack.pop()
    t = get_temp()
    program_block.append(
        f"({action}, {str(left)}, {imdtTrue}{str(right)}, {str(t)})")
    semantic_stack.append(f"{addrTrue}{str(t)}")


def func_mult_op(get_temp, input_token):
    first = semantic_stack.pop()
    action = "MULT"
    second = semantic_stack.pop()
    t = get_temp()
    program_block.append(f"({action}, {str(first)}, {str(second)}, {str(t)})")
    semantic_stack.append(t)


def func_comp_op(get_temp, input_token):
    right = semantic_stack.pop()
    action = "EQ" if semantic_stack.pop() == "==" else "LT"
    left = semantic_stack.pop()
    t = get_temp()
    program_block.append(f"({action}, {str(left)}, {str(right)}, {str(t)})")
    semantic_stack.append(t)


def func_save(get_temp, input_token):
    semantic_stack.append(get_PB_next())
    program_block.append(EMPTY_PB)


def func_jpf_save(get_temp, input_token):
    i = get_PB_next()
    PBAddr = semantic_stack.pop()
    expression = semantic_stack.pop()
    program_block[PBAddr] = f"(JPF, {str(expression)}, {str(i + 1)}, )"
    semantic_stack.append(i)
    program_block.append(EMPTY_PB)


def func_jp(get_temp, input_token):
    i = get_PB_next()
    PBAddr = semantic_stack.pop()
    # todo
    try:
        program_block[int(PBAddr)] = f"(JP, {str(i)}, , )"
    except:
        program_block.append(f"(JP err, {str(i)}, , )")


def func_jpf(get_temp, input_token):
    i = get_PB_next()
    PBAddr = semantic_stack.pop()
    expression = semantic_stack.pop()
    program_block[PBAddr] = f"(JPF, {str(expression)}, {str(i)}, )"


def func_label(get_temp, input_token):
    i = get_PB_next()
    semantic_stack.append(i)
    ru_stack.append(i)


def func_until(get_temp, input_token):
    left = semantic_stack.pop()
    right = semantic_stack.pop()
    program_block.append(f"(JPF, {str(left)}, {str(right)}, )")
    rep_pos = ru_stack.pop()
    for i in range(program_block.__len__()):
        if program_block.__len__() - 1 - i < rep_pos:
            break
        tac = program_block[program_block.__len__() - 1 - i]
        tac: str
        if tac[0] == 'b':
            tac = tac.replace("?", str(get_PB_next()))
            program_block[program_block.__len__() - 1 -
                          i] = tac.replace("b", "")


def func_break(get_temp, input_token):
    if ru_stack.__len__() > 0:
        program_block.append(f"b(JP, {'?'}, , )")
    else:
        semantic.error(ErrorTypeEnum.break_stmt, None)
        pass


def func_parr(get_temp, input_token):
    arr_index = str(semantic_stack.pop())
    arr_id = str(semantic_stack.pop())

    # semantic_stack.append(arr_index)
    semantic_stack.append(f"{arr_index}")
    semantic_stack.append(f"#{WORD_SIZE}")
    func_mult_op(get_temp, None)

    semantic_stack.append("+")
    semantic_stack.append(f"{arr_id}")
    func_add_op(get_temp, None, address_mode=True)


def func_pop(get_temp, input_token):
    semantic_stack.pop()


def func_set_tmp_addr(get_temp, input_token):
    arr_tmp_start, arr_addr = st.get_arr_temp()
    program_block.append(f"(ASSIGN, #{str(arr_tmp_start)}, {str(arr_addr)}, )")


def func_save_first_func(get_temp, input_token):
    global FIRST_FUNC
    if not FIRST_FUNC:
        FIRST_FUNC = (True, get_PB_next())
        print(FIRST_FUNC)
        program_block.append(EMPTY_PB)


def func_at_the_end(get_temp, input_token):
    global FIRST_FUNC
    if FIRST_FUNC:
        program_block[FIRST_FUNC[1]
                      ] = f"(JP, {str(st.get_starting_line('main'))}, , )"
