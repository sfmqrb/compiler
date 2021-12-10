import re
from dataclasses import dataclass

@dataclass
class RE:
    MY_DIGIT = re.compile(r'[0-9]')
    MY_LETTER = re.compile(r'[a-zA-Z]')
    MY_LETDIG = re.compile(r'[a-zA-Z0-9]')
    MY_SYMB = re.compile(r'[\[\]\(\)\{\}\;\:\-\+\<\,]')
    KEYWORDS = re.compile(
        r'^if$|^else$|^void$|^int$|^repeat$|^break$|^until$|^return$|^endif$')
    MY_WHITESPACE = re.compile(' |\t|\n|\r|\v|\f')
    MY_FORSLASH = re.compile('\/')
    MY_STAR = re.compile('\*')
    MY_EQ = re.compile('\=')
    MY_NEWLINE = re.compile('\n')
    MY_ALPHABET = re.compile(
        r'[a-zA-Z0-9]|[\[\]\(\)\{\}\;\:\-\+\<\,\=\/\*]|[\s|\t|\n|\r|\v|\f]')
