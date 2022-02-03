temps_list = []

class SnapshotStack():
    def __init__(self, program_block: list, initial_sp=4004, WORD_SIZE=4, POP_ADDR=4000, sp_first_point_to=4008):
        self.sp = initial_sp
        program_block.append(f"(ASSIGN, #{sp_first_point_to}, {self.sp}, )")
        self.WORD_SIZE = WORD_SIZE
        self.POP_ADDR = POP_ADDR

    def __str__(self):
        return "SnapshotStack: sp=" + str(self.sp)

    def push(self, push_val, program_block):
        push_val = str(push_val)
        program_block.append(f"(ASSIGN, {push_val}, @{self.sp}, )")
        program_block.append(f"(ADD, {self.sp}, #{self.WORD_SIZE}, {self.sp})")

    def pop(self, program_block, get_temp, _assign_=True):
        program_block.append(f"(SUB, {self.sp}, #{self.WORD_SIZE}, {self.sp})")
        if _assign_:
            tmp_addr = get_temp()
            temps_list.append(tmp_addr)
            program_block.append(f"(ASSIGN, @{self.sp}, {tmp_addr}, )")
            return tmp_addr
        return None

    def access_using_offset(self, offset, program_block, get_temp):
        t1 = get_temp()
        t2 = get_temp()
        temps_list.append(t2)
        temps_list.append(t1)
        program_block.append(
            f"(SUB, {self.sp}, #{offset*self.WORD_SIZE}, {t1})")
        program_block.append(f"(ASSIGN, @{t1}, {t2}, )")
        return t2


class FunctionRelatedStack():
    def __init__(self, program_block: list, initial_sp=8004, WORD_SIZE=4, POP_ADDR=8000, sp_first_point_to=8008):
        self.sp = initial_sp
        program_block.append(f"(ASSIGN, #{sp_first_point_to}, {self.sp}, )")
        self.WORD_SIZE = WORD_SIZE
        self.POP_ADDR = POP_ADDR

    def __str__(self):
        return "FunctionRelatedStack: sp=" + str(self.sp)

    def push(self, push_val, program_block):
        push_val = str(push_val)
        program_block.append(f"(ASSIGN, {push_val}, @{self.sp}, )")
        program_block.append(f"(ADD, {self.sp}, #{self.WORD_SIZE}, {self.sp})")

    def pop(self, program_block, get_temp, _assign_=True):
        program_block.append(f"(SUB, {self.sp}, #{self.WORD_SIZE}, {self.sp})")
        if _assign_:
            tmp_addr = get_temp()
            temps_list.append(tmp_addr)
            program_block.append(f"(ASSIGN, @{self.sp}, {tmp_addr}, )")
            return tmp_addr
        return None

    def access_using_offset(self, offset, program_block, get_temp):
        t1 = get_temp()
        t2 = get_temp()
        temps_list.append(t2)
        temps_list.append(t1)
        program_block.append(
            f"(SUB, {self.sp}, #{offset*self.WORD_SIZE}, {t1})")
        program_block.append(f"(ASSIGN, @{t1}, {t2}, )")
        return t2
