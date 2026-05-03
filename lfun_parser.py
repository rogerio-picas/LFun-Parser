import ply.yacc as yacc
from lfun_lexer import tokens

precedence = (
    ('left', 'EQUAL', 'LESS', 'GREATER'),
    ('left', 'SUM', 'SUBTRACTION'),
    ('left', 'PRODUCT', 'BAR')
)

def p_programa(p):
    '''programa : instrucao
                | programa instrucao'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]

def p_instrucao(p):
    '''instrucao : let_statement SEMICOLON
                 | fun_statement SEMICOLON
                 | when_statement SEMICOLON
                 | expressao SEMICOLON'''
    p[0] = p[1]

# --- LET (Definição) ---
def p_let_statement(p):
    '''let_statement : LET ID COLON tipo ASSIGN expressao
                     | LET ID ASSIGN expressao'''
    pass

# --- FUNCTION (Assinatura) ---
def p_fun_statement(p):
    '''fun_statement : FUN ID COLON tipo ARROW tipo'''
    pass

# --- WHEN ---
def p_when_statement(p):
    '''when_statement : WHEN LPAREN expressao RPAREN IS cases END'''
    pass

def p_cases(p):
    '''cases : case
             | cases case'''
    pass

def p_case(p):
    '''case : pattern_list ARROW expressao SEMICOLON
            | UNDERSCORE ARROW expressao SEMICOLON'''
    if p[1] == '_':
        # Caso default: ('default', expressao)
        p[0] = ('default', p[3])
    else:
        # Caso comum: ('case', lista_padrões, expressao)
        p[0] = ('case', p[1], p[3])

def p_pattern_list(p):
    '''pattern_list : pattern
                    | pattern_list COMMA pattern'''
    pass

def p_pattern(p):
    '''pattern : INT
               | TRUE
               | FALSE
               | ID'''
    pass

# --- EXPRESSÕES ---
def p_expressao_binaria(p):
    '''expressao : expressao SUM expressao
                 | expressao SUBTRACTION expressao
                 | expressao PRODUCT expressao
                 | expressao BAR expressao
                 | expressao EQUAL expressao
                 | expressao LESS expressao
                 | expressao GREATER expressao'''
    if p[2] == '+': p[0] = p[1] + p[3]
    elif p[2] == '-': p[0] = p[1] - p[3]
    elif p[2] == '*': p[0] = p[1] * p[3]
    elif p[2] == '/': p[0] = p[1] / p[3]
    elif p[2] == '==': p[0] = p[1] == p[3]
    elif p[2] == '<': p[0] = p[1] < p[3]
    elif p[2] == '>': p[0] = p[1] > p[3]

def p_expressao_if(p):
    '''expressao : IF expressao THEN expressao ELSE expressao'''
    pass

def p_expressao_parenteses(p):
    '''expressao : LPAREN expressao RPAREN'''
    pass

def p_expressao_inteiro(p):
    '''expressao : INT'''
    p[0] = p[1]

def p_expressao_bool(p):
    '''expressao : TRUE
                 | FALSE'''
    pass

def p_expressao_chamada(p):
    '''expressao : ID LPAREN expressao RPAREN'''
    pass

def p_expressao_id(p):
    '''expressao : ID'''
    pass

def p_tipo(p):
    '''tipo : T_INT
           | T_BOOL'''
    pass

def p_expressao_unaria(p):
    '''expressao : SUBTRACTION expressao %prec PRODUCT'''
    pass

def p_error(p):
    if p:
        print(f"Erro de sintaxe na linha {p.lineno}", p.type)
    else:
        print("Erro de sintaxe no final")

parser = yacc.yacc()