# compiler project

## phase 1

### Scanner

A scanner is a program that takes a sequence of characters (the source file of the program) and produces a sequence of tokens that will be used to feed the compiler's parser.

A file called "input.txt" contains the raw code. Also, this file is in the same directory as `compiler.py`.

## phase 2

### Parser

A parser is a compiler or interpreter component that breaks data into smaller elements for easy translation into another language. In this project we implemented a recursive descent parser.A recursive descent parser is a kind of top-down parser built from a set of mutually recursive procedures (or a non-recursive equivalent) where each such procedure implements one of the nonterminals of the grammar.

- parse tree

- panic mode

## phase 3

### Code generator

Generate intermediate code which is relatively close to assembly language.

- handle recursive functions


## Run

```
pip install -r requirements.txt
make run
```


## Interpreter
put output.txt file in interpreter directory and run tester_<your_os>

## Debugging
For program to create symbol_table, lexical_errors, syntax_errors and pars_tree in file tools/Development.py set develop_mode = True. 
