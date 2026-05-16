import sys
from lfun_parser import parser
from lfun_interpreter import LFunInterpreter

def get_lfun_type(val):
    """Devolve o tipo LFun de um valor Python como string ('Int', 'Bool', 'Function')."""
    if isinstance(val, bool): return "Bool"
    if isinstance(val, int): return "Int"
    if isinstance(val, float): return "Float"
    if isinstance(val, str) and val.startswith("<fun"): return "Function"
    return "Unknown"

def format_output(val):
    """Formata um resultado da AST para exibição: 'resultado: <val> tipo: <tipo>'."""
    ltype = get_lfun_type(val)
    # Converter True/False para minúsculas
    if isinstance(val, bool):
        val = str(val).lower()
    return f"resultado: {val} tipo: {ltype}"

def print_outputs(outputs, errors):
    for res in outputs:
        if res is not None and not (isinstance(res, str) and res.startswith('<fun')):
            print(format_output(res))
    for err in errors:
        print(f"[Erro] {err}")

def main():
    """Ponto de entrada: corre em modo ficheiro (argv[1]) ou REPL interativo."""
    interpreter = LFunInterpreter()
    # Se houver argumento, lê ficheiro, caso contrário lê terminal
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            data = f.read()
        result = parser.parse(data)
        if result is not None:
            outputs, errors = interpreter.run(result)
            print_outputs(outputs, errors)
    else:
        while True:
            try:
                s = input('LFun > ')
            except EOFError:
                break
            if not s: continue
            result = parser.parse(s)
            if result is not None:
                outputs, errors = interpreter.run(result)
                print_outputs(outputs, errors)

if __name__ == "__main__":
    main()