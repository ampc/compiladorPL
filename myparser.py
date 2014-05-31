from mylexer import MyLexer
import ply.yacc as yacc
from mytac import Node
from symbol_table import Symbol_Table
from registry import Registry
from file_output import File_Output


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

    # def parse(self, text):
        # return self.parser.parse(input=text, debug=True)

    def p_command(self, p):
        '''command : command2 SEMI command
                   | empty'''
        if len(p) > 2:
            p[0] = Node("command", [p[1], p[3]])
        else:
            p[0] = Node("command")

    def p_command2(self, p):
        '''command2 : command_assign
                    | command_while
                    | command_if'''
        p[0] = Node("command2", [p[1]])

    def p_command_assign(self, p):
        'command_assign : ID ASSIGN expression'
        self.symbol_table[p[1]] = p[3]
        p[0] = Node("command_assign", [p[1], p[3]], p[2])

    def p_command_while(self, p):
        'command_while : WHILE expression DO command DONE'
        p[0] = Node("command_while", [p[3], p[5]])

    def p_command_if(self, p):
        '''command_if : IF expression THEN BEGIN command
                        | IF expression THEN BEGIN command ELSE BEGIN command END'''
        if(len(p) > 6):
            p[0] = Node("command_if", [p[3], p[5], p[9]])
        else:
            p[0] = Node("command_if", [p[3], p[5]])

    def p_expression_binary(self, p):
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
        p[0] = Node("expression_binary", [p[1], p[3]], p[2])
        '''if p[2] == '+':
            p[0] = p[1] + p[3]
        elif p[2] == '-':
            p[0] = p[1] - p[3]
        elif p[2] == '*':
            p[0] = p[1] * p[3]
        elif p[2] == '/':
            p[0] = p[1] / p[3]
        elif p[2] == '==':
            p[0] = p[1] == p[3]
        elif p[2] == '/=':
            p[0] = p[1] != p[3]
        elif p[2] == '>':
            p[0] = p[1] > p[3]
        elif p[2] == '>=':
            p[0] = p[1] >= p[3]
        elif p[2] == '<':
            p[0] = p[1] < p[3]
        elif p[2] == '<':
            p[0] = p[1] <= p[3]
            '''

    def p_expression_uminus(self, p):
        'expression : MINUS expression %prec UMINUS'
        # p[0] = -p[2]
        p[0] = Node("expression_uminus", [p[2]], p[1])

    def p_expression_group(self, p):
        'expression : LPAREN expression RPAREN'
        p[0] = Node("expression_group", [p[2]])

    def p_expression_real(self, p):
        'expression : REAL'
        p[0] = Node("expression_real", [], p[1])

    def p_expression_int(self, p):
        'expression : INT'
        p[0] = Node("expression_int", [], p[1])

    def p_expression_id(self, p):
        'expression : ID'
        try:
            p[0] = self.symbol_table[p[1]]
        except LookupError:
            print("Undefined name '%s'" % p[1])
            p[0] = 0

    def p_empty(self, p):
        'empty :'
        pass

    def p_error(self, p):
        print("Syntax error at '%s'" % p.value)
