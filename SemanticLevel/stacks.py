class SnapshotStack():
    def __init__(self, program_block: list, initial_sp=2004, WORD_SIZE=4, POP_ADDR=2000, sp_first_point_to=2008):
        self.sp = initial_sp
        program_block.append(f"(assign, #{sp_first_point_to}, {self.sp}, )")
        self.WORD_SIZE = WORD_SIZE
        self.POP_ADDR = POP_ADDR

    def __str__(self):
        return "SnapshotStack: sp=" + str(self.sp)

    def push(self, push_val, program_block):
        program_block.append(f"(assign, {push_val}, @{self.sp}, )")
        program_block.append(f"(ADD, {self.sp}, #{self.WORD_SIZE}, {self.sp})")

    def pop(self, program_block, _assign_=True):
        program_block.append(f"(SUB, {self.sp}, #{self.WORD_SIZE}, {self.sp})")
        if _assign_:
            program_block.append(f"(assign, @{self.sp}, {self.POP_ADDR}, )")
            return self.POP_ADDR
        return None


class FunctionRelatedStack():
    def __init__(self, program_block: list, initial_sp=4004, WORD_SIZE=4, POP_ADDR=4000, sp_first_point_to=4008):
        self.sp = initial_sp
        program_block.append(f"(assign, #{sp_first_point_to}, {self.sp}, )")
        self.WORD_SIZE = WORD_SIZE
        self.POP_ADDR = POP_ADDR

    def __str__(self):
        return "FunctionRelatedStack: sp=" + str(self.sp)

    def push(self, push_val, program_block):
        program_block.append(f"(assign, {push_val}, @{self.sp}, )")
        program_block.append(f"(ADD, {self.sp}, #{self.WORD_SIZE}, {self.sp})")

    def pop(self, program_block, _assign_=True):
        program_block.append(f"(SUB, {self.sp}, #{self.WORD_SIZE}, {self.sp})")
        if _assign_:
            program_block.append(f"(assign, @{self.sp}, {self.POP_ADDR}, )")
            return self.POP_ADDR
        return None
