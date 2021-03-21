from lexer import *
from myparser import *

# input_string = '''
# x := 5;
# y := x;
# PRINT 64;
# '''

input_string = '''
 PRINT x;
    IF quantity THEN
        total := total;
        tax := 0.05;
    ENDIF;
'''

print(input_string)
lexer = Lexer(input_string)
print(lexer.tokens)

parser = Parser(lexer)
parser.start()
