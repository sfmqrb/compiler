<h1 align="center">Welcome to my compiler project 👋</h1>

<h2 style="color: #ccc">
    Description of the project's different phases:
</h2>

<div style="margin: 20px">
    <h2> phase 1 </h2>

<h3 style="margin-top:20px"> 
    Scanner
</h3>

<div style="margin: 20px">

A scanner is a program that takes a sequence of characters (the source file of the program) and produces a sequence of tokens that will be used to feed the compiler's parser.

A file called "input.txt" contains the raw code. Also, this file is in the same directory as `compiler.py`.

</div>
<div>
    <h2> phase 2 </h2>
</div>

<h3 style="margin-top:20px"> 
    Parser
</h3>

A parser is a compiler or interpreter component that breaks data into smaller elements for easy translation into another language. In this project we implemented a recursive descent parser.A recursive descent parser is a kind of top-down parser built from a set of mutually recursive procedures (or a non-recursive equivalent) where each such procedure implements one of the nonterminals of the grammar.

- parse tree

- panic mode

<div>
    <h2> phase 3 </h2>
</div>

<h3 style="margin-top:20px">
    Code Generator
</h3>

Generate intermediate code which is relatively close to assembly language.

- handle recursive functions

</div>


## Run

```
pip install -r requirements.txt
make run
```


##    Interpreter

Put output.txt file in interpreter directory and run `./tester_<YOUR_OPERATING_SYSTEM>`

## Debugging
    
For program to create symbol_table, lexical_errors, syntax_errors and pars_tree in file tools/Development.py set develop_mode = True.

## Code Contributors
Project's code is written by
<a href="https://github.com/sfmqrb/compiler/graphs/contributors"> contributors </a>
