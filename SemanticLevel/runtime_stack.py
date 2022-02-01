class RuntimeStack():
    def __init__(self, initial_sp=2000, WORD_SIZE=4, POP_ADDR=4000):
        self.sp = initial_sp
        self.WORD_SIZE = WORD_SIZE
        self.POP_ADDR = POP_ADDR

    def __str__(self):
        return "RuntimeStack: sp=" + str(self.sp)

    def push(self, toPushVariable, program_block):
        program_block.append(f"(assign, {toPushVariable}, @{self.sp}, )")
        self.sp += self.WORD_SIZE

    def pop(self, program_block):
        self.sp -= self.WORD_SIZE
        program_block.append(f"(assign, @{self.sp}, {self.POP_ADDR}, )")
