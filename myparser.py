from mylexer import MyLexer
import ply.yacc as yacc


class MyParser:
    precedence = (
        ('left', 'EQUALS', 'NEQUALS'),
        ('left', 'LESSER', 'GREATER', 'GREATEREQUAL', 'LESSEREQUAL'),
        ('left', 'PLUS', 'MINUS'),
        ('left', 'MULT', 'DIV'),
        ('right', 'UMINUS')
    )

    symbol_table = {}

    def __init__(self):
        self.lexer = MyLexer()
        self.lexer.build()
        self.tokens = self.lexer.tokens
        self.parser = yacc.yacc(module=self)

    def parse(self, text):
        return self.parser.parse(input=text, debug=True)

    def p_command(self, t):
        '''command : command2 SEMI command
                   | empty'''

    def p_command2(self, t):
        '''command2 : command_assign
                    | command_while
                    | command_if'''

    def p_command_assign(self, t):
        'command_assign : ID ASSIGN expression'
        self.symbol_table[t[1]] = t[3]

    def p_command_while(self, t):
        'command_while : WHILE expression DO command DONE'

    def p_command_if(self, t):
        '''command_if : IF expression THEN BEGIN command
                        | IF expression THEN BEGIN command ELSE BEGIN command END'''

    def p_expression_binary(self, t):
        '''expression : expression PLUS expression
                        | expression MINUS expression
                        | expression MULT expression
                        | expression DIV expression
                        | expression EQUALS expression
                        | expression NEQUALS expression
                        | expression GREATER expression
                        | expression GREATEREQUAL expression
                        | expression LESSER expression
                        | expression LESSEREQUAL expression'''
        if t[2] == '+':
            t[0] = t[1] + t[3]
        elif t[2] == '-':
            t[0] = t[1] - t[3]
        elif t[2] == '*':
            t[0] = t[1] * t[3]
        elif t[2] == '/':
            t[0] = t[1] / t[3]
        elif t[2] == '==':
            t[0] = t[1] == t[3]
        elif t[2] == '/=':
            t[0] = t[1] != t[3]
        elif t[2] == '>':
            t[0] = t[1] > t[3]
        elif t[2] == '>=':
            t[0] = t[1] >= t[3]
        elif t[2] == '<':
            t[0] = t[1] < t[3]
        elif t[2] == '<':
            t[0] = t[1] <= t[3]

    def p_expression_uminus(self, t):
        'expression : MINUS expression %prec UMINUS'
        t[0] = -t[2]

    def p_expression_group(self, t):
        'expression : LPAREN expression RPAREN'
        t[0] = t[2]

    def p_expression_real(self, t):
        'expression : REAL'
        t[0] = t[1]

    def p_expression_int(self, t):
        'expression : INT'
        t[0] = t[1]

    def p_expression_id(self, t):
        'expression : ID'
        try:
            t[0] = self.symbol_table[t[1]]
        except LookupError:
            print("Undefined name '%s'" % t[1])
            t[0] = 0

    def p_empty(self, t):
        'empty :'
        pass

    def p_error(self, t):
        print("Syntax error at '%s'" % t.value)
