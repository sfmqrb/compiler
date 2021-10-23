import scanner


def file2str(filepath):
    f = open(filepath, 'r')
    ls_text = f.readlines()
    s = ""
    for txt in ls_text:
        s += txt
    return s


def save_tuple2file_based_on_1element(file_name, tl):
    f = open(file_name, mode='w')
    this_el = -1
    for t in tl:
        if t[0] == this_el:
            f.write('(' + t[1] + ', ' + t[2] + ') ')
        else:

            if this_el != -1:
                f.write('\n')
            this_el = t[0]
            f.write(str(this_el) + '.' + '	')
            # f.write('{0:4}'.format(str(this_el)+'.'))
            f.write(('(' + t[1] + ', ' + t[2] + ') ').replace("\n", ""))
            # f.write('(' + repr(t[1]) + ', ' + repr(t[2]) + ') ')


def empty_error_file(file_name):
    f = open(file_name, mode='w')
    f.write("There is no lexical error.")


def save_list2file(file_name, l):
    f = open(file_name, mode='w')
    for i, t in enumerate(l):
        f.write('{0:4}'.format(str(i + 1) + '.'))
        f.write(t + '\n')


def main():
    # addr = './pa_1/PA1_testcases1.2/T01/input.txt'
    # addr = './pa_1/PA1_testcases1.2/test/input.txt'
    addr = 'input.txt'
    s = file2str(addr, )
    scnr = scanner.scanner(s=s)
    while True:
        line, next_token, next_token_type = scnr.get_next_token()
        if next_token == None: break
        # print("{: >3}{: >20}{: >20}".format(*[line, next_token, next_token_type]))

    if scnr.errors.__len__() == 0:
        empty_error_file("lexical_errors.txt")
    else:
        save_tuple2file_based_on_1element("lexical_errors.txt", scnr.errors)
    save_tuple2file_based_on_1element("tokens.txt", scnr.tokens)
    save_list2file('symbol_table.txt', scnr.lexemes)


if __name__ == "__main__":
    try:
        main()
    except:
        print("an unexpected error occurred")
