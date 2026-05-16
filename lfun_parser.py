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
    """Regra raiz da gramática: um programa é uma lista de uma ou mais instruções."""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_instrucao(p):
    '''instrucao : let_statement SEMICOLON
                 | fun_statement SEMICOLON
                 | expressao SEMICOLON'''
    """Uma instrução é um let, fun ou expressão terminados por ponto-e-vírgula."""
    p[0] = p[1]

# --- LET (Definição) ---
def p_let_statement(p):
    '''let_statement : LET ID COLON tipo ASSIGN expressao
                 | LET ID ID ASSIGN expressao
                 | LET ID ASSIGN expressao'''
    """Declaração de variável com tipo opcional ou definição de função com parâmetro."""
    if len(p) == 7:
        # LET ID COLON tipo ASSIGN expressao
        p[0] = ('let', p[2], p[4], p[6])
    elif len(p) == 6:
        # LET ID ID ASSIGN expressao
        p[0] = ('fun_def', p[2], p[3], p[5])
    else:
        # LET ID ASSIGN expressao (sem tipo)
        p[0] = ('let', p[2], None, p[4])

# --- FUNCTION (Assinatura) ---
def p_fun_statement(p):
    '''fun_statement : FUN ID COLON tipo ARROW tipo'''
    """Declaração da assinatura de uma função: tipo do argumento e tipo de retorno."""
    p[0] = ('fun_sig', p[2], p[4], p[6])

# --- WHEN (Expressão) ---
def p_expressao_when(p):
    '''expressao : WHEN LPAREN expressao RPAREN IS cases END
             | WHEN expressao IS cases END'''
             
    if len(p) == 8:
        # WHEN LPAREN expressao RPAREN IS cases END
        """Expressão de pattern matching: avalia a expressão e selecciona o caso correspondente."""
    p[0] = ('when', p[3], p[6])
    else:
        # WHEN expressao IS cases END
        p[0] = ('when', p[2], p[4])

def p_cases(p):
    '''cases : case
             | cases case'''
    """Acumula a lista de casos de um bloco when numa lista Python."""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_case(p):
    '''case : pattern_list ARROW expressao SEMICOLON
            | UNDERSCORE ARROW expressao SEMICOLON'''
    """Um caso individual: padrão(s) ou wildcard _ seguido da expressão resultado."""
    if p[1] == '_':
        p[0] = ('default', p[3])
    else:
        p[0] = ('case', p[1], p[3])

def p_pattern_list(p):
    '''pattern_list : pattern
                    | pattern_list COMMA pattern'''
    """Lista de padrões separados por vírgula que partilham a mesma expressão resultado."""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_pattern(p):
    '''pattern : INT
               | SUBTRACTION INT
               | TRUE
               | FALSE
               | ID'''
    if len(p) == 3:           # SUBTRACTION INT → inteiro negativo
        p[0] = -p[2]
    elif p[1] == 'true':      # TRUE → bool Python
        p[0] = True
    elif p[1] == 'false':     # FALSE → bool Python
        p[0] = False
    else:
        p[0] = p[1]           # INT ou ID: valor literal

# --- EXPRESSÕES ---
def p_expressao_binaria(p):
    '''expressao : expressao SUM expressao
                 | expressao SUBTRACTION expressao
                 | expressao PRODUCT expressao
                 | expressao BAR expressao
                 | expressao EQUAL expressao
                 | expressao LESS expressao
                 | expressao GREATER expressao'''
    
    # if p[2] == '/' and p[3] == 0:
    #     raise Exception("Erro de Sintaxe: Divisão por zero.")
    
    # if p[2] == '/' and p[1]%2==0 and p[3]%2==0:
    #     p[1]=float(p[1])
    #     p[3]=float(p[3])

    p[0] = ('binop', p[2], p[1], p[3])

def p_expressao_if(p):
    '''expressao : IF expressao THEN expressao ELSE expressao'''
    """Condicional: avalia a condição e devolve o ramo then ou else."""
    p[0] = ('if', p[2], p[4], p[6])

def p_expressao_parenteses(p):
    '''expressao : LPAREN expressao RPAREN'''
    """Expressão entre parênteses; usado para forçar precedência ou passar argumentos."""
    p[0] = p[2]

def p_expressao_inteiro(p):
    '''expressao : INT'''
    """Literal inteiro como nó folha da AST."""
    p[0] = ('int', p[1])

def p_expressao_bool(p):
    '''expressao : TRUE
                 | FALSE'''
    """Literal booleano (true/false) como nó folha da AST."""
    p[0] = ('bool', p[1])

def p_expressao_chamada(p):
    '''expressao : ID LPAREN expressao RPAREN'''
    """Chamada de função: nome da função e expressão argumento."""
    p[0] = ('call', p[1], p[3])

def p_expressao_id(p):
    '''expressao : ID'''
    """Referência a uma variável ou função definida no ambiente."""
    p[0] = ('var', p[1])

def p_tipo(p):
    '''tipo : T_INT
           | T_BOOL'''
    """Tipo primitivo da linguagem: Int ou Bool."""
    p[0] = p[1]

def p_expressao_unaria(p):
    '''expressao : SUBTRACTION expressao %prec PRODUCT'''
    """Negação unária de uma expressão inteira."""
    p[0] = ('unop', '-', p[2])

def p_error(p):
    """Reporta um erro de sintaxe com a linha e o token problemático."""
    if p:
        print(f"Erro de sintaxe na linha {p.lineno}", p.type)
    else:
        print("Erro de sintaxe no final")

parser = yacc.yacc()