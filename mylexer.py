import ply.lex as lex


class MyLexer:

    # List of keywords
    keywords = {
        'if': 'IF',
        'then': 'THEN',
        'else': 'ELSE',
        'begin': 'BEGIN',
        'end': 'END',
        'while': 'WHILE',
        'do': 'DO',
        'done': 'DONE'
    }
    # List of tokens
    tokens = [
        'INT',
        'REAL',
        'ID',
        'PLUS',
        'MINUS',
        'MULT',
        'DIV',
        'EQUALS',
        'LPAREN',
        'RPAREN',
        'NEQUALS',
        'LESSER',
        'GREATER',
        'LESSEREQUAL',
        'GREATEREQUAL',
        'ASSIGN',
        'SEMI'
    ] + list(keywords.values())

    # Regular Expressions for simple tokens
    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_MULT = r'\*'
    t_DIV = r'/'
    t_EQUALS = r'=='
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_NEQUALS = r'/='
    t_LESSER = r'<'
    t_GREATER = r'>'
    t_LESSEREQUAL = r'<='
    t_GREATEREQUAL = r'>='
    t_ASSIGN = r'<-'
    t_SEMI = r';'

    t_ignore = ' \t\n\r'

    def build(self, **kwargs):
        self.lexer = lex.lex(object=self, **kwargs)

    def t_REAL(self, t):
        r'-?\d+\.\d*(e-?\d+)?'
        t.value = float(t.value)
        return t

    def t_INT(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_ID(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = self.keywords.get(t.value, 'ID')

        if t.type != 'ID':
            print "Variable name used is reserved!"
            t.lexer.skip
        else:
            return t

    def t_comment(self, t):
        r'\#.*'
        pass

    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    def test(self, data):
        self.lexer.input(data)
        while True:
            tok = lex.token()
            if not tok:
                break
            print tok

#teste
l = MyLexer()
l.build()
l.test("a<-4.0-4")
