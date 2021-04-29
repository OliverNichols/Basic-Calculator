import math, operator, ply.lex, ply.yacc, re
from decimal import Decimal

OPERATORS = {
    '+': operator.add,
    '-': operator.sub, 
    '*': operator.mul, 
    '/': operator.truediv, 
    '**': math.pow, 
    '^': math.pow
}

COMPARATORS = {
    '>': operator.gt, 
    '<': operator.lt, 
    '>=': operator.ge, 
    '<=': operator.le,
    '==': operator.eq, 
    '!=': operator.ne
}

tokens = [
    'INT',
    'FLOAT',
    'NAME',
    'PLUS',
    'MINUS',
    'DIVIDE',
    'MULTIPLY',
    'POWER',
    'LPAREN',
    'RPAREN',
    'EQUALS',
    'EQUIV',
    'NEQ',
    'GT',
    'LT',
    'GTEQ',
    'LTEQ',
    'SQRT',
    'EXP',
    'LOG'
    ]

t_PLUS = r'\+'
t_MINUS = r'\-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'\/'
t_POWER = r'\*\*'

t_LPAREN = r'\('
t_RPAREN = r'\)'

t_EQUIV = r'=='
t_NEQ = r'!='
t_EQUALS = r'='

t_GTEQ = r'>='
t_GT = r'>'
t_LTEQ = r'<='
t_LT = r'<'

t_ignore = r' '
t_ignore_COMMENT = r'\#.*'
    
def t_FLOAT(t):
    r'-?\d+\.\d+'
    t.value = Decimal(t.value)
    return t

def t_INT(t):
    r'-?\d+'
    t.value = int(t.value)
    return t

def t_SQRT(t):
    r'sqrt'
    return t

def t_EXP(t):
    r'exp'
    return t

def t_LOG(t):
    r'log'
    return t

def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z_]*'
    t.type = 'NAME'
    return t

def t_error(t):
    raise ValueError("invalid input")

    t.lexer.skip(1)

lexer = ply.lex.lex()

precedence = (
    
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULTIPLY', 'DIVIDE'),
    ('left', 'POWER'),
    ('left', 'LPAREN', 'RPAREN'),
    ('left', 'EQUIV','NEQ','GT','GTEQ','LT','LTEQ'),
    ('left', 'SQRT', 'EXP', 'LOG')

    )

def p_calc(p):
    '''
    calc : expression
         | func
         | comparison
         | var_assign
         | empty
    '''
    value = run(p[1])
    
    p[0] = value

def p_expr_func(p):
    '''
    expression : func
    '''
    p[0] = p[1]

def p_func(p):
    '''
    func : SQRT LPAREN expression RPAREN
         | EXP LPAREN expression RPAREN
         | LOG LPAREN expression RPAREN
    '''
    p[0] = (p[1], p[3])

def p_factor_expr(p):
    '''
    expression : LPAREN expression RPAREN
    '''
    p[0] = p[2]

def p_var_assign(p):
    '''
    var_assign : NAME EQUALS expression
    var_assign : NAME EQUALS comparison
    '''
    p[0] = ('=', p[1], p[3])

def p_comparison(p):
    '''
    comparison : expression EQUIV expression
               | expression NEQ expression
               | expression GTEQ expression
               | expression GT expression
               | expression LTEQ expression
               | expression LT expression
    '''
    p[0] = (p[2], p[1], p[3])

def p_expression(p):
    '''
    expression : expression POWER expression
               | expression MULTIPLY expression
               | expression DIVIDE expression
               | expression PLUS expression
               | expression MINUS expression
    '''
    p[0] = (p[2], p[1], p[3])

def p_factor_expr_mul(p):
    '''
    expression : INT NAME
               | FLOAT NAME
    '''
    p[0] = ('*', p[1], ('var', p[2]))

def p_expression_int_float(p):
    '''
    expression : INT
               | FLOAT
    '''
    p[0] = p[1]

def p_expression_var(p):
    '''
    expression : NAME
    '''
    p[0] = ('var', p[1])

def p_standard_form(p):
    '''
    func : INT NAME INT
         | FLOAT NAME INT
    '''
    if p[2] == 'e': p[0] = ('*', p[1], ('**', 10, p[3]))

def p_error(p):
    print("SyntaxError")#; raise SyntaxError("invalid syntax")

def p_empty(p):
    '''
    empty :
    '''
    p[0] = None

parser = ply.yacc.yacc()

env = {}

def run(p):
    if isinstance(p, tuple):
        if p[0] == '=': env[current_id][p[1]] = (v:=run(p[2])); return f"Set variable `{p[1]}` to `{v}`"
        elif (op := OPERATORS.get(p[0])): return op (run(p[1]), run(p[2]))
        elif (cp := COMPARATORS.get(p[0])): return cp (run(p[1]), run(p[2]))
        elif p[0] == 'var':
            try: return env[current_id][p[1]]
            except: raise ValueError(f"`{p[1]}` has no value set")
        else:
            if p[0] == 'sqrt': return operator.pow(run(p[1]), 1/2)
            elif p[0] == 'exp': return math.exp(run(p[1]))
            elif p[0] == 'log': return math.log(run(p[1]))
            
            else: return p

    else: return p

def set_user(id):
    global current_id
    current_id = id

    if id not in env: env[id] = {'k':1000, 'm':1000000, 'id':id}

def parse(s, user=None):
    set_user(user)
    s = re.subn('[0-9]-[0-9]',lambda x:x.group().replace('-','+-'), s)[0].replace('^','**')
    
    value = parser.parse(s)
    if type(value) not in [str,bool]: value = Decimal('{:f}'.format(value)) if 1 < abs(value) < 10**6 else value
    return value


if __name__ == '__main__':
    
    set_user(None)

    while True:
        try: s = input('>> ')
        except EOFError: break

        s = re.subn('[0-9]-[0-9]',lambda x:x.group().replace('-','+-'), s)[0].replace('^','**')
        
        try:
            value = parser.parse(s, debug=0)
            if type(value) not in [str,bool]: value = '{:f}'.format(value) if 1 < abs(value) < 10**6 else value
            print(value)

        except ValueError as e: print(str(e))
