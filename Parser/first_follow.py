first = {
    'Program': {'$', 'void', 'int'},
    'Declaration-list': {'', 'void', 'int'},
    'Declaration': {'void', 'int'},
    'Declaration-initial': {'void', 'int'},
    'Declaration-prime': {'(', ';', '['},
    'Var-declaration-prime': {';', '['},
    'Fun-declaration-prime': {'('},
    'Type-specifier': {'void', 'int'},
    'Params': {'int', 'void'},
    'Param-list': {'', ','},
    'Param': {'void', 'int'},
    'Param-prime': {'[', ''},
    'Compound-stmt': {'{'},
    'Statement-list': {
        '', '{',
        ';', 'break',
        'if', 'repeat',
        'return', 'ID',
        '(', 'NUM'
    },
    'Statement': {
        '{', ';',
        'break', 'if',
        'repeat', 'return',
        'ID', '(',
        'NUM'
    },
    'Expression-stmt': {';', 'break', 'ID', '(', 'NUM'},
    'Selection-stmt': {'if'},
    'Else-stmt': {'else', 'endif'},
    'Iteration-stmt': {'repeat'},
    'Return-stmt': {'return'},
    'Return-stmt-prime': {';', 'ID', '(', 'NUM'},
    'Expression': {'ID', '(', 'NUM'},
    'B': {
        '[', '=', '(',
        '*', '+', '-',
        '<', '==', ''
    },
    'H': {
        '=', '*', '',
        '+', '-', '<',
        '=='
    },
    'Simple-expression-zegond': {'(', 'NUM'},
    'Simple-expression-prime': {
        '(', '*', '+',
        '-', '<', '==',
        ''
    },
    'C': {'', '<', '=='},
    'Relop': {'<', '=='},
    'Additive-expression': {'(', 'ID', 'NUM'},
    'Additive-expression-prime': {'(', '*', '+', '-', ''},
    'Additive-expression-zegond': {'(', 'NUM'},
    'D': {'', '+', '-'},
    'Addop': {'+', '-'},
    'Term': {'(', 'ID', 'NUM'},
    'Term-prime': {'(', '*', ''},
    'Term-zegond': {'(', 'NUM'},
    'G': {'*', ''},
    'Factor': {'(', 'ID', 'NUM'},
    'Var-call-prime': {'(', '[', ''},
    'Var-prime': {'[', ''},
    'Factor-prime': {'(', ''},
    'Factor-zegond': {'(', 'NUM'},
    'Args': {'', 'ID', '(', 'NUM'},
    'Arg-list': {'ID', '(', 'NUM'},
    'Arg-list-prime': {'', ','}
}

follow = {
    'Program': {''},
    'Declaration-list': {
        '$', '{',
        ';', 'break',
        'if', 'repeat',
        'return', 'ID',
        '(', 'NUM',
        '}'
    },
    'Declaration': {
        'void', 'int',
        '$', '{',
        ';', 'break',
        'if', 'repeat',
        'return', 'ID',
        '(', 'NUM',
        '}'
    },
    'Declaration-initial': {'(', ';', '[', ',', ')'},
    'Declaration-prime': {
        'void', 'int',
        '$', '{',
        ';', 'break',
        'if', 'repeat',
        'return', 'ID',
        '(', 'NUM',
        '}'
    },
    'Var-declaration-prime': {
        'void', 'int',
        '$', '{',
        ';', 'break',
        'if', 'repeat',
        'return', 'ID',
        '(', 'NUM',
        '}'
    },
    'Fun-declaration-prime': {
        'void', 'int',
        '$', '{',
        ';', 'break',
        'if', 'repeat',
        'return', 'ID',
        '(', 'NUM',
        '}'
    },
    'Type-specifier': {'ID'},
    'Params': {')'},
    'Param-list': {')'},
    'Param': {',', ')'},
    'Param-prime': {',', ')'},
    'Compound-stmt': {
        'void', 'int', '$',
        '{', ';', 'break',
        'if', 'repeat', 'return',
        'ID', '(', 'NUM',
        '}', 'else', 'endif',
        'until'
    },
    'Statement-list': {'}'},
    'Statement': {
        '{', ';',
        'break', 'if',
        'repeat', 'return',
        'ID', '(',
        'NUM', '}',
        'else', 'endif',
        'until'
    },
    'Expression-stmt': {
        '{', ';',
        'break', 'if',
        'repeat', 'return',
        'ID', '(',
        'NUM', '}',
        'else', 'endif',
        'until'
    },
    'Selection-stmt': {
        '{', ';',
        'break', 'if',
        'repeat', 'return',
        'ID', '(',
        'NUM', '}',
        'else', 'endif',
        'until'
    },
    'Else-stmt': {
        '{', ';',
        'break', 'if',
        'repeat', 'return',
        'ID', '(',
        'NUM', '}',
        'else', 'endif',
        'until'
    },
    'Iteration-stmt': {
        '{', ';',
        'break', 'if',
        'repeat', 'return',
        'ID', '(',
        'NUM', '}',
        'else', 'endif',
        'until'
    },
    'Return-stmt': {
        '{', ';',
        'break', 'if',
        'repeat', 'return',
        'ID', '(',
        'NUM', '}',
        'else', 'endif',
        'until'
    },
    'Return-stmt-prime': {
        '{', ';',
        'break', 'if',
        'repeat', 'return',
        'ID', '(',
        'NUM', '}',
        'else', 'endif',
        'until'
    },
    'Expression': {';', ')', ']', ','},
    'B': {';', ')', ']', ','},
    'H': {';', ')', ']', ','},
    'Simple-expression-zegond': {';', ')', ']', ','},
    'Simple-expression-prime': {';', ')', ']', ','},
    'C': {';', ')', ']', ','},
    'Relop': {'(', 'ID', 'NUM'},
    'Additive-expression': {';', ')', ']', ','},
    'Additive-expression-prime': {'<', '==', ';', ')', ']', ','},
    'Additive-expression-zegond': {'<', '==', ';', ')', ']', ','},
    'D': {'<', '==', ';', ')', ']', ','},
    'Addop': {'(', 'ID', 'NUM'},
    'Term': {
        '+', '-', ';',
        ')', '<', '==',
        ']', ','
    },
    'Term-prime': {
        '+', '-', '<',
        '==', ';', ')',
        ']', ','
    },
    'Term-zegond': {
        '+', '-', '<',
        '==', ';', ')',
        ']', ','
    },
    'G': {
        '+', '-', '<',
        '==', ';', ')',
        ']', ','
    },
    'Factor': {
        '*', '+', '-',
        ';', ')', '<',
        '==', ']', ','
    },
    'Var-call-prime': {
        '*', '+', '-',
        ';', ')', '<',
        '==', ']', ','
    },
    'Var-prime': {
        '*', '+', '-',
        ';', ')', '<',
        '==', ']', ','
    },
    'Factor-prime': {
        '*', '+', '-',
        '<', '==', ';',
        ')', ']', ','
    },
    'Factor-zegond': {
        '*', '+', '-',
        '<', '==', ';',
        ')', ']', ','
    },
    'Args': {')'},
    'Arg-list': {')'},
    'Arg-list-prime': {')'}
}
