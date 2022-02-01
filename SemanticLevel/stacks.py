class SnapshotStack():
    def __init__(self, initial_sp=2004, WORD_SIZE=4, POP_ADDR=2000):
        self.sp = initial_sp
        self.WORD_SIZE = WORD_SIZE
        self.POP_ADDR = POP_ADDR

    def __str__(self):
        return "SnapshotStack: sp=" + str(self.sp)

    def push(self, push_val, program_block):
        program_block.append(f"(assign, {push_val}, @{self.sp}, )")
        self.sp += self.WORD_SIZE

    def pop(self, program_block):
        self.sp -= self.WORD_SIZE
        program_block.append(f"(assign, @{self.sp}, {self.POP_ADDR}, )")
        return self.POP_ADDR


class FunctionRelatedStack():
    def __init__(self, initial_sp=4004, WORD_SIZE=4, POP_ADDR=4000):
        self.sp = initial_sp
        self.WORD_SIZE = WORD_SIZE
        self.POP_ADDR = POP_ADDR

    def __str__(self):
        return "FunctionRelatedStack: sp=" + str(self.sp)

    def push(self, push_val, program_block):
        program_block.append(f"(assign, {push_val}, @{self.sp}, )")
        self.sp += self.WORD_SIZE

    def pop(self, program_block, _assign_=True):
        self.sp -= self.WORD_SIZE
        if _assign_:
            program_block.append(f"(assign, @{self.sp}, {self.POP_ADDR}, )")
        return self.POP_ADDR
