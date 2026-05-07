def get_lfun_type(val):
    if isinstance(val, bool): return "Bool"
    if isinstance(val, int): return "Int"
    if isinstance(val, str) and val.startswith("<fun"): return "Function"
    if isinstance(val, tuple) and len(val) > 0 and val[0] == 'closure': return "Function"
    return "Unknown"

class LFunInterpreter:
    def __init__(self):
        # Tabela de Símbolos Global: nome -> valor
        self.env = {}
        # Assinaturas: nome -> (tipo_arg, tipo_ret)
        self.signatures = {}

    def evaluate(self, node, local_env=None):
        if local_env is None:
            local_env = {}

        # Se o nó não for um tuplo, pode ser um valor literal (como o UNDERSCORE ou ID simples em patterns)
        if not isinstance(node, tuple):
            return node

        tag = node[0]

        # --- Literais ---
        if tag == 'int':
            return node[1]
        
        if tag == 'bool':
            return True if node[1] == 'true' else False

        # --- Variáveis ---
        if tag == 'var':
            name = node[1]
            if name in local_env: return local_env[name]
            if name in self.env: return self.env[name]
            raise Exception(f"Erro Semântico: Variável '{name}' não definida.")

        # --- Operações Binárias ---
        if tag == 'binop':
            op = node[1]
            left = self.evaluate(node[2], local_env)
            right = self.evaluate(node[3], local_env)
            
            type_left = get_lfun_type(left)
            type_right = get_lfun_type(right)
            
            if op in ('+', '-', '*', '/'):
                if type_left != 'Int' or type_right != 'Int':
                    raise Exception(f"Erro de Tipos: Operação '{op}' requer operandos do tipo 'Int', mas recebeu '{type_left}' e '{type_right}'")
                if op == '/' and right == 0:
                    raise Exception("Erro de Execução: Divisão por zero.")
                if op == '+': return left + right
                if op == '-': return left - right
                if op == '*': return left * right
                if op == '/': return left // right # Divisão inteira conforme LFun
                
            elif op in ('<', '>'):
                if type_left != 'Int' or type_right != 'Int':
                    raise Exception(f"Erro de Tipos: Operação '{op}' requer operandos do tipo 'Int', mas recebeu '{type_left}' e '{type_right}'")
                if op == '<': return left < right
                if op == '>': return left > right
                
            elif op == '==':
                if type_left != type_right:
                    raise Exception(f"Erro de Tipos: Operação '==' requer operandos do mesmo tipo, mas recebeu '{type_left}' e '{type_right}'")
                return left == right

        # --- Operações Unárias ---
        if tag == 'unop':
            val = self.evaluate(node[2], local_env)
            type_val = get_lfun_type(val)
            if type_val != 'Int':
                raise Exception(f"Erro de Tipos: Operação '-' unária requer operando do tipo 'Int', mas recebeu '{type_val}'")
            return -val

        # --- Condicional IF ---
        if tag == 'if':
            cond = self.evaluate(node[1], local_env)
            if not isinstance(cond, bool):
                raise Exception("Erro de Tipos: Condição do IF deve ser Booleana.")
            if cond:
                return self.evaluate(node[2], local_env)
            else:
                return self.evaluate(node[3], local_env)

        # --- Definições (LET) ---
        if tag == 'let':
            name = node[1]
            declared_type = node[2]
            
            # Enforce single definition / immutability
            if name in self.env:
                raise Exception(f"Erro Semântico: Identificador '{name}' já foi definido e é imutável.")
                
            value = self.evaluate(node[3], local_env)
            
            # Enforce type checking
            if declared_type is not None:
                actual_type = get_lfun_type(value)
                if actual_type != declared_type:
                    raise Exception(f"Erro de Tipos: O identificador '{name}' foi declarado como '{declared_type}', mas a expressão avaliada tem o tipo '{actual_type}'.")
            
            self.env[name] = value
            return value

        # --- Assinaturas de Funções (FUN) ---
        if tag == 'fun_sig':
            name = node[1]
            self.signatures[name] = (node[2], node[3])
            return None

        # --- Definição de Função (LET nome param = corpo) ---
        if tag == 'fun_def':
            name = node[1]
            param = node[2]
            body = node[3]
            
            # Enforce single definition / immutability for functions as well
            if name in self.env:
                raise Exception(f"Erro Semântico: Função/Identificador '{name}' já foi definido e é imutável.")
                
            self.env[name] = ('closure', param, body)
            return f"<fun {name}>"

        # --- Chamada de Função ---
        if tag == 'call':
            name = node[1]
            arg_val = self.evaluate(node[2], local_env)
            
            fun = self.env.get(name)
            if not fun or not isinstance(fun, tuple) or fun[0] != 'closure':
                raise Exception(f"Erro: '{name}' não é uma função definida.")
            
            _, param_name, body = fun
            # Contexto local: o parâmetro recebe o valor do argumento
            # NOTA: Aqui implementamos um escopo simples (lexical scoping básico)
            new_local = {param_name: arg_val}
            return self.evaluate(body, new_local)

        # --- Seleção de Casos (WHEN) ---
        if tag == 'when':
            val = self.evaluate(node[1], local_env)
            cases = node[2]
            for case in cases:
                if case[0] == 'default':
                    return self.evaluate(case[1], local_env)
                
                # case: ('case', list_of_patterns, expression)
                patterns = case[1]
                if val in patterns:
                    return self.evaluate(case[2], local_env)
            
            raise Exception(f"Erro: Nenhum caso no 'when' corresponde ao valor {val}.")

    def run(self, ast):
        results = []
        for instr in ast:
            res = self.evaluate(instr)
            results.append(res)
        return results
