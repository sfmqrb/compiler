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
            f.write('('+t[1]+', '+t[2]+') ')
        else:

            if this_el != -1:
                f.write('\n')
            this_el = t[0]
            f.write('{0:4}'.format(str(this_el)+'.'))
            f.write('(' + t[1] + ', ' + t[2] + ') ')


def main():
    addr = './pa_1/PA1_testcases1.2/T01/input.txt'
    s = file2str(addr,)
    scnr = scanner.scanner(s=s)
    while True:
        line, next_token, next_token_type = scnr.get_next_token()
        if next_token == None: break
        # print("{: >3}{: >20}{: >20}".format(*[line, next_token, next_token_type]))

    print(scnr.lexemes)
    save_tuple2file_based_on_1element("lexical_errors.txt", scnr.errors)
    save_tuple2file_based_on_1element("tokens.txt", scnr.tokens)
    # print(scanner)
if __name__ == "__main__":
    main()