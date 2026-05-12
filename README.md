# LFun — Interpretador de Linguagem Funcional

Trabalho Prático de Processamento de Linguagens — IPCA 2026  
Implementado em Python com a biblioteca [PLY](https://www.dabeaz.com/ply/).

---

## Índice

1. [Visão Geral](#visão-geral)
2. [Arquitectura e Pipeline](#arquitectura-e-pipeline)
3. [Como Executar](#como-executar)
4. [Tabela de Tokens](#tabela-de-tokens)
5. [Tabela de Tipos](#tabela-de-tipos)
6. [Tabela de Nós da AST](#tabela-de-nós-da-ast)
7. [Tabela de Instruções LFun](#tabela-de-instruções-lfun)
8. [Caso Prático Passo a Passo](#caso-prático-passo-a-passo)
9. [Dependências](#dependências)

---

## Visão Geral

**LFun** é uma linguagem de programação funcional minimalista com:

- Tipos primitivos `Int` e `Bool`
- Declarações de variáveis e funções com `let`
- Assinaturas de tipo com `fun`
- Condicional `if / then / else`
- Pattern matching com `when / is / end`
- Operadores aritméticos e de comparação
- Comentários de linha `--` e de bloco `{- ... -}`

---

## Arquitectura e Pipeline

```
Ficheiro .lf  (texto puro)
      │
      ▼
┌─────────────┐
│  lfun_lexer │  Análise Léxica — converte o texto em tokens
└──────┬──────┘
       │  lista de tokens
       ▼
┌──────────────┐
│ lfun_parser  │  Análise Sintática — valida a gramática e constrói a AST
└──────┬───────┘
       │  AST (tuplos Python)
       ▼
┌─────────────────────┐
│  lfun_interpreter   │  Interpretação — percorre a AST e executa as instruções
└──────┬──────────────┘
       │  valores Python (int, bool, closure)
       ▼
┌─────────┐
│  main   │  Formatação e impressão: "resultado: X tipo: Y"
└─────────┘
```

### Responsabilidade de cada ficheiro

| Ficheiro | Fase | Entrada | Saída |
|---|---|---|---|
| `lfun_lexer.py` | Léxica | Texto (string) | Lista de tokens |
| `lfun_parser.py` | Sintática | Lista de tokens | AST (tuplos) |
| `lfun_interpreter.py` | Semântica / Execução | AST | Valores Python |
| `main.py` | Interface | Ficheiro / REPL | Output formatado |

---

## Como Executar

```bash
# Criar e activar ambiente virtual (recomendado)
python3 -m venv .venv
source .venv/bin/activate   # macOS / Linux
# .venv\Scripts\activate    # Windows

# Instalar dependências
pip install -r requirements.txt

# Correr um ficheiro .lf
python main.py entrada.lf

# Modo interactivo (REPL)
python main.py
LFun > let x = 3 + 4;
resultado: 7 tipo: Int
```

---

## Tabela de Tokens

Definidos em `lfun_lexer.py`. Cada token é a unidade mínima reconhecida pelo lexer.

| Token | Símbolo / Padrão | Exemplo |
|---|---|---|
| `LET` | `let` | `let x = 5` |
| `FUN` | `fun` | `fun f : Int -> Bool` |
| `IF` | `if` | `if x > 0` |
| `THEN` | `then` | `then true` |
| `ELSE` | `else` | `else false` |
| `WHEN` | `when` | `when (x) is` |
| `IS` | `is` | `when (x) is` |
| `END` | `end` | `end` |
| `T_INT` | `Int` | `: Int` |
| `T_BOOL` | `Bool` | `: Bool` |
| `TRUE` | `true` | `true` |
| `FALSE` | `false` | `false` |
| `INT` | `\d+` | `42` |
| `ID` | `[a-zA-Z][a-zA-Z0-9_]*` | `avalia`, `x` |
| `SUM` | `+` | `3 + 4` |
| `SUBTRACTION` | `-` | `x - 1` |
| `PRODUCT` | `*` | `2 * 3` |
| `BAR` | `/` | `10 / 2` |
| `EQUAL` | `==` | `x == 0` |
| `LESS` | `<` | `x < 5` |
| `GREATER` | `>` | `x > 5` |
| `ASSIGN` | `=` | `let x = 5` |
| `COLON` | `:` | `: Int` |
| `SEMICOLON` | `;` | fim de instrução |
| `ARROW` | `->` | `Int -> Bool` |
| `COMMA` | `,` | `-1, 1 -> true` |
| `LPAREN` | `(` | `avalia(x)` |
| `RPAREN` | `)` | `avalia(x)` |
| `UNDERSCORE` | `_` | wildcard em `when` |

---

## Tabela de Tipos

| Tipo LFun | Tipo Python equivalente | Exemplo de valor |
|---|---|---|
| `Int` | `int` | `0`, `-1`, `42` |
| `Bool` | `bool` | `true` → `True`, `false` → `False` |
| `Function` | `tuple` (`'closure'`) | `<fun avalia>` |

---

## Tabela de Nós da AST

Cada instrução ou expressão é representada como um **tuplo Python** com uma etiqueta (`tag`) na primeira posição.

| Tag | Estrutura do tuplo | Descrição |
|---|---|---|
| `'int'` | `('int', valor)` | Literal inteiro |
| `'bool'` | `('bool', 'true'/'false')` | Literal booleano |
| `'var'` | `('var', nome)` | Referência a variável |
| `'unop'` | `('unop', '-', expr)` | Negação unária |
| `'binop'` | `('binop', op, esq, dir)` | Operação binária |
| `'if'` | `('if', cond, then, else)` | Condicional |
| `'let'` | `('let', nome, tipo, expr)` | Declaração de variável |
| `'fun_sig'` | `('fun_sig', nome, t_arg, t_ret)` | Assinatura de função |
| `'fun_def'` | `('fun_def', nome, param, corpo)` | Definição de função |
| `'call'` | `('call', nome, arg)` | Chamada de função |
| `'when'` | `('when', expr, [casos])` | Pattern matching |
| `'case'` | `('case', [padrões], expr)` | Caso específico do when |
| `'default'` | `('default', expr)` | Caso wildcard `_` do when |

---

## Tabela de Instruções LFun

| Instrução | Sintaxe | Exemplo |
|---|---|---|
| Declarar variável com tipo | `let nome : Tipo = expr;` | `let x : Int = 10;` |
| Declarar variável sem tipo | `let nome = expr;` | `let y = true;` |
| Declarar assinatura de função | `fun nome : TArg -> TRet;` | `fun f : Int -> Bool;` |
| Definir função | `let nome param = expr;` | `let f x = x + 1;` |
| Chamar função | `nome(expr)` | `f(5)` |
| Condicional | `if expr then expr else expr` | `if x > 0 then true else false` |
| Pattern matching | `when (expr) is casos end` | ver exemplo abaixo |
| Comentário de linha | `-- texto` | `-- isto é ignorado` |
| Comentário de bloco | `{- texto -}` | `{- bloco ignorado -}` |

---

## Caso Prático Passo a Passo

Usando o ficheiro `entrada.lf`:

```
fun avalia : Int -> Bool;
let avalia x =
  when ( x ) is
    -1, 1 -> true ;
    0     -> false ;
    _     -> true ;
  end;

let r1 = avalia(-1);
let r2 = avalia(0);
```

---

### Fase 1 — Lexer (`lfun_lexer.py`)

O texto é convertido numa sequência de tokens. Função `t_ID` distingue palavras reservadas de identificadores; `t_INT` converte dígitos para `int`.

**Instrução:** `fun avalia : Int -> Bool;`

| Token | Tipo |
|---|---|
| `fun` | `FUN` |
| `avalia` | `ID` |
| `:` | `COLON` |
| `Int` | `T_INT` |
| `->` | `ARROW` |
| `Bool` | `T_BOOL` |
| `;` | `SEMICOLON` |

**Instrução:** `let r1 = avalia(-1);`

| Token | Tipo |
|---|---|
| `let` | `LET` |
| `r1` | `ID` |
| `=` | `ASSIGN` |
| `avalia` | `ID` |
| `(` | `LPAREN` |
| `-` | `SUBTRACTION` |
| `1` | `INT` |
| `)` | `RPAREN` |
| `;` | `SEMICOLON` |

---

### Fase 2 — Parser (`lfun_parser.py`)

Os tokens são organizados segundo as regras gramaticais e transformados em nós da AST (tuplos).

**`fun avalia : Int -> Bool;`** → regra `p_fun_statement`
```python
('fun_sig', 'avalia', 'Int', 'Bool')
```

**`let avalia x = when (x) is ...`** → regra `p_let_statement` (3 elementos: nome + param + corpo)
```python
('fun_def', 'avalia', 'x',
  ('when', ('var', 'x'), [
    ('case', [-1, 1], ('bool', 'true')),
    ('case', [0],     ('bool', 'false')),
    ('default',       ('bool', 'true'))
  ])
)
```

**`let r1 = avalia(-1);`** → regras `p_let_statement` + `p_expressao_chamada` + `p_expressao_unaria`
```python
('let', 'r1', None,
  ('call', 'avalia',
    ('unop', '-', ('int', 1))
  )
)
```

---

### Fase 3 — Interpretador (`lfun_interpreter.py`)

O método `evaluate` percorre a AST recursivamente. O método `run` itera sobre todas as instruções.

#### Instrução: `('fun_sig', 'avalia', 'Int', 'Bool')`
```
tag = 'fun_sig'
→ self.signatures['avalia'] = ('Int', 'Bool')
→ devolve None  (sem output)
```

#### Instrução: `('fun_def', 'avalia', 'x', <corpo when>)`
```
tag = 'fun_def'
→ self.env['avalia'] = ('closure', 'x', <corpo when>)
→ devolve "<fun avalia>"
```

#### Instrução: `('let', 'r1', None, ('call', 'avalia', ('unop', '-', ('int', 1))))`

O interpretador avalia de dentro para fora:

```
1. tag = 'int'      → devolve 1
2. tag = 'unop'     → devolve -1
3. tag = 'call'     → procura 'avalia' em self.env
                      cria contexto local: {'x': -1}
                      avalia o corpo 'when' com x = -1
4. tag = 'when'     → avalia ('var', 'x') → -1
                      percorre casos:
                        caso [-1, 1]: -1 está na lista → avalia ('bool', 'true') → True
5. tag = 'let'      → self.env['r1'] = True
                      devolve True
```

---

### Fase 4 — Main (`main.py`)

O resultado `True` passa por `get_lfun_type` e `format_output`:

```
get_lfun_type(True)  → "Bool"
format_output(True)  → "resultado: true tipo: Bool"
```

**Output final no terminal:**
```
resultado: true tipo: Bool
resultado: false tipo: Bool
```

---

## Dependências

| Pacote | Uso |
|---|---|
| `ply` | Biblioteca de análise léxica e sintática (Lexer + Parser) |
| `pytest` | Execução de testes automáticos |
| `graphviz` | Visualização gráfica da AST (opcional) |

```bash
python3 -m venv .venv
source .venv/bin/activate   # macOS / Linux
# .venv\Scripts\activate    # Windows
pip install -r requirements.txt
```
