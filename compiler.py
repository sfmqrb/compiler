import scanner
from Parser import parser
from SemanticLevel import ErrorType


# amir mohammad mohammadi 97107126
# sajad faghfur maghreby 97106187


def file2str(filepath):
    f = open(filepath, "r")
    ls_text = f.readlines()
    s = ""
    for txt in ls_text:
        s += txt
    return s


def save_tuple2file_based_on_1element(file_name, tl):
    f = open(file_name, mode="w")
    this_el = -1
    for t in tl:
        # resolve \n error
        if "\n" in t[1]:
            t = (t[0] - 1, t[1].replace("\n", ""), t[2])
            # t[0] = int(t[0]) - 1
            # t[1].replace("\n", "")
        if t[0] == this_el:
            f.write("(" + t[1] + ", " + t[2] + ") ")
        else:

            if this_el != -1:
                f.write("\n")
            this_el = t[0]
            f.write(str(this_el) + "." + "	")
            # f.write('{0:4}'.format(str(this_el)+'.'))
            f.write(("(" + t[1] + ", " + t[2] + ") "))
            # f.write('(' + repr(t[1]) + ', ' + repr(t[2]) + ') ')


def empty_error_file(file_name):
    f = open(file_name, mode="w")
    f.write("There is no lexical error.")


def save_list2file(file_name, l):
    f = open(file_name, mode="w")
    for i, t in enumerate(l):
        f.write("{0:4}".format(str(i + 1) + "."))
        f.write(t + "\n")


def main():
    # addr = './pa_1/PA1_testcases1.2/T01/input1.txt'
    # addr = './pa_1/PA1_testcases1.2/test/input1.txt'
    addr = "input.txt"
    s = file2str(
        addr,
    )
    scnr = scanner.scanner(s=s)
    while True:
        line, next_token_type, next_token = scnr.get_next_token()
        ErrorType.gl_line_number = line
        if next_token_type is None:
            parser.get_next_token("$", line)
            break
        else:
            parser.get_next_token(
                (str(next_token_type), str(next_token)), line)
        # print("{: >3}{: >20}{: >20}".format(*[line, next_token, next_token_type]))

    if scnr.errors.__len__() == 0:
        empty_error_file("lexical_errors.txt")
    else:
        save_tuple2file_based_on_1element("lexical_errors.txt", scnr.errors)
    save_tuple2file_based_on_1element("tokens.txt", scnr.tokens)
    save_list2file("symbol_table.txt", scnr.lexemes)
    save_tree("parse_tree.txt")
    save_syntax_errors("syntax_errors.txt")
    save_semantic_errors("semantic_errors.txt")


def save_tree(addr):
    tree = parser.draw_tree()
    # print(tree)
    f = open(addr, "w", encoding="utf-8")
    f.write(tree)
    f.close()


def save_syntax_errors(addr):
    errors = parser.get_pars_errors()
    if errors.__len__() == 0:
        f = open(addr, "w", encoding="utf-8")
        f.write("There is no syntax error.")
        f.close()
    else:
        f = open("syntax_errors.txt", "w", encoding="utf-8")
        for e in errors:
            f.write(e + "\n")
        f.close()


def save_semantic_errors(addr):
    errors = ErrorType.semantic_errors
    if errors.__len__() == 0:
        f = open(addr, "w", encoding="utf-8")
        f.write("The input program is semantically correct.")
        f.close()
    else:
        f = open(addr, "w", encoding="utf-8")
        for e in errors:
            e = e.replace("'", '')
            f.write(e + "\n")
        f.close()


if __name__ == "__main__":
    # try:
    main()
    # except:
    #     print("an unexpected error occurred")
