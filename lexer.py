from ply import lex


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


tokens = [
    'INT',
    'REAL',
    'ID',
    'PLUS',
    'MINUS',
    'TIMES',
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


def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_REAL(t):
    r'\d+.\d+'
    t.value = float(t.value)
    return t


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = keywords.get(t.value, 'ID')
    if t.type != 'ID':
        print "Variable name is reserved."
        t.lexer.skip
    else:
        return t

#	def t_COMMENT(t):
# r'\#.*'
#    	pass
    # No return value. Token discarded


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
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

t_ignore = '\t\n\r'


lex.lex()
lex.input("1+1==2")
while 1:
    tok = lex.token()
    if not tok:
        break
    print tok
