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


def error(err_type, id, expected=None, illegal=None, arg=None):
    line_number = str(gl_line_number)
    id = str(id)
    if err_type == ErrorTypeEnum.scoping:
        err = "#" + line_number + ": SemanticLevel Error! '" + id + "' is not defined"
    elif err_type == ErrorTypeEnum.void_type:
        err = "#" + line_number + ": SemanticLevel Error! Illegal type of void for '" + id + "'"
    elif err_type == ErrorTypeEnum.number_mathing:
        err = "#" + line_number + \
              ":semantic error! Mismatch in numbers of arguments of '" + id + "'"
    elif err_type == ErrorTypeEnum.break_stmt:
        err = "#" + line_number + \
              ": Semantic Error! No 'repeat ... until' found for 'break'."
    elif err_type == ErrorTypeEnum.type_mismatch:
        err = "#" + line_number + ": SemanticLevel Error! Type mismatch in operands, Got '" + \
              illegal + "' instead of '" + expected + "'"
    elif err_type == ErrorTypeEnum.type_matching:
        err = "#" + line_number + ": SemanticLevel Error!Mismatch in type of argument " + str(arg) + \
              " for '" + id + "'. Expected '" + expected + \
              "' but got '" + illegal + "' instead "
    semantic_errors.append(err)
