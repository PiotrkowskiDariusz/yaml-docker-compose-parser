# wypisywanie linii w informacji o bledzie
# na 29.03
class Parser:

    ##### Parser header #####
    def __init__(self, scanner):
        self.next_token = scanner.next_token
        self.token = self.next_token()

    def take_token(self, token_type):
        if self.token.type != token_type:
            self.error("Unexpected token: " + self.token_type)
        if token_type != 'EOF':
            self.token = self.next_token()

    def error(self, msg):
        raise RuntimeError('Parser error, %s' % msg)

    ##### Parser body #####

    # Starting symbol
    def start(self):
        # start -> program EOF
        if self.token.type == 'EOF' or self.token.type == 'version' or self.token.type == 'services' or self.token.type == 'volumes' or self.token.type == 'networks':
            self.program()
            self.take_token('EOF')
        else:
            self.error("Epsilon not allowed")

    def program(self):
        # program -> newline program
        if self.token.type == 'NEWLINE':
            self.take_token('NEWLINE')
            self.program()
        # program -> top_element
        elif self.token.type == 'version' or self.token.type == 'services' or self.token.type == 'volumes' or self.token.type == 'networks':
            self.top_element()
            self.program()
        else:
            pass

    def top_element(self):
        # top_element -> version
        if self.token.type == 'version':
            self.take_token('version')
            self.take_token('ASSIGN')
            self.take_token('ID')
            self.take_token('NEWLINE')
            self.top_element()
            print('Top element OK (version)')
        elif self.token.type == 'services':
            self.token.type('services')
            self.token.type('ASSIGN')
            self.token.type('NEWLINE')
            self.token.type('INDENTATION')
            self.service_element()
        elif self.token.type == 'volumes':
            self.token.type('volumes')
            self.token.type('ASSIGN')
            self.token.type('NEWLINE')
            self.volumes_element


    def statement(self):
        # statement -> print_stmt
        if self.token.type == 'PRINT':
            self.print_stmt()
        # statement -> assign_stmt
        elif self.token.type == 'ID':
            self.assign_stmt()
        # statement -> if_stmt
        elif self.token.type == 'IF':
            self.if_stmt()
        else:
            self.error("Epsilon not allowed")

    # print_stmt -> PRINT value END
    def print_stmt(self):
        if self.token.type == 'PRINT':
            self.take_token('PRINT')
            self.value()
            self.take_token('END')
            print("print_stmt OK")
        else:
            self.error("Epsilon not allowed")

    # assign_stmt -> ID ASSIGN value END
    def assign_stmt(self):
        if self.token.type == 'ID':
            self.take_token('ID')
            self.take_token('ASSIGN')
            self.value()
            self.take_token('END')
            print("assign_stmt OK")
        else:
            self.error("Epsilon not allowed")

    def value(self):
        # value -> NUMBER
        if self.token.type == 'NUMBER':
            self.take_token('NUMBER')
        # value -> ID
        elif self.token.type == 'ID':
            self.take_token('ID')
        else:
            self.error("Epsilon not allowed")

    def if_stmt(self):
        # if_stmt -> IF ID THEN program ENDIF END
        if self.token.type == 'IF':
            self.take_token('IF')
            self.take_token('ID')
            self.take_token('THEN')
            self.program()
            self.take_token('ENDIF')
            self.take_token('END')
            print("if_stmt OK")
        else:
            self.error("Epsilon not allowed")
