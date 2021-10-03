import scanner


def file2str(filepath):
    f = open(filepath, 'r')
    ls_text = f.readlines()
    s = ""
    for txt in ls_text:
        s += txt
    return s

def main():
    addr = './pa_1/PA1_testcases1.2/T10/input.txt'
    s = file2str(addr,)
    scnr = scanner.scanner(s=s)
    while True:
        line, next_token, next_token_type = scnr.get_next_token()
        if next_token == None: break
        # print(line, next_token, next_token_type)

if __name__ == "__main__":
    main()