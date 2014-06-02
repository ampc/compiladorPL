from mylexer import MyLexer
import ply.yacc as yacc
from mytac import If, While, Assign, BinOp, Variable, Int
from symbol_table import Symbol_Table
from registry import Registry 
#from file_output import File_Output 


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
       

    def p_command2(self, p):
        '''command2 : command_assign
                    | command_while
                    | command_if'''
        

    def p_command_assign(self, p):
        'command_assign : ID ASSIGN expression'
        self.symbol_table[p[1]] = p[3]
        variable = Variable(p[1],self)
        p[0]=Assign

    def p_command_while(self, p):
        'command_while : WHILE expression DO command DONE'
        

    def p_command_if(self, p):
        '''command_if : IF expression THEN BEGIN command
                        | IF expression THEN BEGIN command ELSE BEGIN command END'''
        

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
        t[0]=BinOp(t[1],t[2],t[3],self)
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
        p[0].value = -p[2].value
        

    def p_expression_group(self, p):
        'expression : LPAREN expression RPAREN'
        p[0]=p[2]

    def p_expression_real(self, p):
        'expression : REAL'
        

    def p_expression_int(self, p):
        'expression : INT'
        p[0]=Number(p[1],self)

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
