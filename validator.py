# Simple example of parsing
# Bartosz Sawicki, 2014-03-13

#from scanner import *
from myparser import *
from lexer import *

f = open("compose.yaml", "r")
input_string = f.read()
f.close()
print(input_string)
lexer = Lexer(input_string)

parser = Parser(lexer)
parser.start()
