import enum

gl_line_number = 0

semantic_errors = []
class ErrorTypeEnum(enum.Enum):
    scoping = 1
    void_type = 2
    number_mathing = 3
    break_stmt = 4
    type_mismatch = 5
    type_matching = 6
