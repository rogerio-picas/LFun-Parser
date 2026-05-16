import ply.lex as lex

# 1. Primeiro defines as palavras reservadas
reserved = {
    'let': 'LET',
    'fun': 'FUN',
    'if': 'IF',
    'then': 'THEN',
    'else': 'ELSE',
    'when': 'WHEN',
    'is': 'IS',
    'end': 'END',
    'Int': 'T_INT',
    'Bool': 'T_BOOL',
    'true': 'TRUE',
    'false': 'FALSE'
}

# 2. Agora já podes montar a lista de tokens
tokens = [
    'ID', 'INT',
    'SUM', 'SUBTRACTION', 'PRODUCT', 'BAR',
    'EQUAL', 'LESS', 'GREATER',
    'LPAREN', 'RPAREN', 'UNDERSCORE',
    'ASSIGN', 'COLON', 'SEMICOLON', 'ARROW', 'COMMA'
] + list(reserved.values())

# 3. Regras de Expressões Regulares para tokens simples
t_SUM         = r'\+'
t_SUBTRACTION = r'-'
t_PRODUCT     = r'\*'
t_BAR         = r'/'
t_EQUAL       = r'=='
t_LESS        = r'<'
t_GREATER     = r'>'
t_LPAREN      = r'\('
t_RPAREN      = r'\)'
t_UNDERSCORE  = r'_'
t_ASSIGN      = r'='
t_COLON       = r':'
t_SEMICOLON   = r';'
t_ARROW       = r'->'
t_COMMA       = r','

# 4. Comentários (Requisito da Secção 2.1-E)
def t_COMMENT_MULTI(t):
    r'\{-[\s\S]*?-\}'
    """Ignora comentários de bloco {- ... -} e actualiza o contador de linhas."""
    t.lexer.lineno += t.value.count('\n')
    pass

def t_COMMENT_SINGLE(t):
    r'--.*'
    """Ignora comentários de linha -- até ao fim da linha."""
    pass

# 5. Regras para tokens complexos (INT e ID)
def t_INT(t):
    r'\d+'
    """Reconhece literais inteiros e converte o valor de string para int Python."""
    t.value = int(t.value)
    return t

def t_ID(t):
    r'[a-zA-Z][a-zA-Z0-9_]*'
    """Reconhece identificadores e classifica-os como palavra reservada se aplicável."""
    t.type = reserved.get(t.value, 'ID')
    return t

# 6. Caracteres ignorados e tratamento de erros
t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    """Actualiza o contador de linhas ao encontrar uma ou mais quebras de linha."""
    t.lexer.lineno += len(t.value)

def t_error(t):
    """Reporta um caractere ilegal e avança o lexer para continuar a análise."""
    print(f"Caractere ilegal '{t.value[0]}' na linha {t.lexer.lineno}")
    t.lexer.skip(1)

# Construir o lexer
lexer = lex.lex()