import sys
from lfun_parser import parser
from lfun_interpreter import LFunInterpreter

def get_lfun_type(val):
    if isinstance(val, bool): return "Bool"
    if isinstance(val, int): return "Int"
    if isinstance(val, float): return "Float"
    if isinstance(val, str) and val.startswith("<fun"): return "Function"
    return "Unknown"

def format_output(val):
    ltype = get_lfun_type(val)
    # Converter True/False para minúsculas
    if isinstance(val, bool):
        val = str(val).lower()
    return f"resultado: {val} tipo: {ltype}"

def main():
    interpreter = LFunInterpreter()
    # Se houver argumento, lê ficheiro, caso contrário lê terminal
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            data = f.read()
        result = parser.parse(data)
        if result is not None:
            outputs = interpreter.run(result)
            for res in outputs:
                if res is not None:
                    print(format_output(res))
    else:
        while True:
            try:
                s = input('LFun > ')
            except EOFError:
                break
            if not s: continue
            result = parser.parse(s)
            if result is not None:
                outputs = interpreter.run(result)
                for res in outputs:
                    if res is not None:
                        print(format_output(res))

if __name__ == "__main__":
    main()