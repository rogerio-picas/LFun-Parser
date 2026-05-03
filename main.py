import sys
from lfun_parser import parser

def main():
    # Se houver argumento, lê ficheiro, caso contrário lê terminal
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    result = parser.parse(line)
                    if result is not None:
                        print(f"DEBUG: {line} => {result}")
    else:
        while True:
            try:
                s = input('LFun > ')
            except EOFError:
                break
            if not s: continue
            result = parser.parse(s)
            if result is not None:
                print(f"Resultado: {result}")

if __name__ == "__main__":
    main()