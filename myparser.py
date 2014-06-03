# -*- coding: utf-8 -*-
from collections import namedtuple
from mylexer import MyLexer
import ply.yacc as yacc
from mytac import If, While, Assign, BinOp, Variable, Int, Minus
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

    def __init__(self):
        self.lexer = MyLexer()
        self.lexer.build()
        self.tokens = self.lexer.tokens
        self.parser = yacc.yacc(module=self)
        self.st = Symbol_Table()

        '''
        Namedtuples funcionam da seguinte forma:
            - Para criar um novo, fazes "self.table_entry(tipo, valor)";
            - Para aceder a um dos atributos (coisas dentro dos parenteses retos),
            fazes "st[nome_var].type" ou "st[nome_var].value"
            
        Ja agora, o prof. disse categoricamente que uma tabela de simbolos nao deve
        guardar o valor duma variável, mas sim a sua posição de memória e tipo. No
        meu programa, ela guarda o tipo e o registo em que se encontra o seu valor.
        '''
        # novo
        self.current_label = 'Label 1'
        self.labels = []
        self.label_count = 1
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
        var = Variable(p[1], self)
        p[0] = Assign(var, p[3], self)
        print(self.st.get_keys())
        print(self.st.get_value(var.name))

    def p_command_while(self, p):
        'command_while : WHILE expression DO command DONE'

    def p_command_if(self, p):
        '''command_if : IF new_label expression THEN BEGIN new_if command END
                        | IF new_label expression THEN BEGIN new_if command END ELSE else_expr BEGIN command END'''
        p[0] = p[6]
        p[6].end_if_statement()

    def p_new_if(self, p):
        'new_if :'
        p[0] = If(p[-3], self)
        p[0].producer()

    def p_else_expr(self, p):
        'else_expr :'
        p[-4].branch_op_else()

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
        p[0] = BinOp(p[1], p[2], p[3], self)
		

    def p_expression_uminus(self, p):
        'expression : MINUS expression %prec UMINUS'
        # ISTO NÃO É ASSIM TÃO SIMPLES. VÊ A VERSÃO MAIS RECENTE DO MEU CÓDIGO.
        # BASICAMENTE, QUANDO SE TRATA DUMA VARIÁVEL, É PRECISO NEGAR O SEU VALOR.
        # ISSO IMPLICA UMA INSTRUÇÃO MIPS "neg x, y"
        p[0] = Minus(p[2],self)
		

    def p_expression_group(self, p):
        'expression : LPAREN expression RPAREN'
        p[0] = p[2]

    def p_expression_real(self, p):
        'expression : FLOAT'
        p[0]= FLOAT(p[1],self)

    def p_expression_int(self, p):
        'expression : INT'
        p[0] = Int(p[1], self)
		

    def p_expression_id(self, p):
        'expression : ID'
        try:
            val = self.st.get_value(p[1])
            if(isinstance(val, (int, long))):
                p[0] = Int(val, self)
        except LookupError:
            return ("Undefined name '%s'" % p[1])

    def p_empty(self, p):
        'empty :'
        pass

    def p_error(self, p):
        print("Syntax error at '%s'" % p.value)

     # novo branches/ifs/ciclos
    def new_label(self):
        self.label_count += 1
        return 'Label ' + str(self.label_count)

    def switch_current_label(self):
        self.labels.append(self.current_label)
        self.current_label = self.new_label()
