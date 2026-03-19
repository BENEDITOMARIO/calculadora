import json
import os
import math
import re

class CalculatorLogic:
    def __init__(self):
        self.expression = ""
        self.history_file = "history.json"
        self.history = self._load_history()

    def _load_history(self):
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []

    def _save_history(self):
        with open(self.history_file, 'w') as f:
            json.dump(self.history, f, indent=4)

    def add_char(self, char):
        # Evita repetição de sinais
        if self.expression and self.expression[-1] in "+-×÷" and char in "+-×÷":
            self.expression = self.expression[:-1] + char
        else:
            self.expression += str(char)
        return self.expression

    def clear(self):
        self.expression = ""
        return self.expression

    def backspace(self):
        if self.expression:
            self.expression = self.expression[:-1]
        return self.expression if self.expression else "0"

    def sqrt_current(self):
        """Calcula raiz quadrada do que está no display agora."""
        try:
            val = float(self.expression)
            if val < 0:
                self.expression = "Erro"
                return "Erro"
            result = str(math.sqrt(val))
            # Remove .0 desnecessário
            if result.endswith('.0'):
                result = result[:-2]
            entry = f"√{self.expression} = {result}"
            self.history.insert(0, entry)
            if len(self.history) > 10:
                self.history.pop()
            self._save_history()
            self.expression = result
            return result
        except Exception:
            self.expression = "Erro"
            return "Erro"

    def sqrt_prefix(self):
        """Marca que o próximo número receberá raiz quadrada."""
        self.expression = "√"
        return "√"

    def calculate(self):
        try:
            expr = self.expression

            # Caso: expressão começa com √ seguido de número (ex: √9, √25)
            if re.match(r'^√[\d.]+$', expr):
                return self.sqrt_current_from_expr(expr[1:])

            expr_formatted = (
                expr
                .replace('×', '*')
                .replace('÷', '/')
                .replace('^2', '**2')
            )
            # Converte √N ou √(expr) para math.sqrt(...)
            expr_formatted = re.sub(
                r'√(\(.*?\)|\d+\.?\d*)',
                lambda m: f'math.sqrt({m.group(1)})',
                expr_formatted
            )
            result = str(eval(expr_formatted))
            # Remove .0 desnecessário
            if result.endswith('.0'):
                result = result[:-2]
            entry = f"{self.expression} = {result}"
            self.history.insert(0, entry)
            if len(self.history) > 10:
                self.history.pop()
            self._save_history()
            self.expression = result
            return result
        except Exception:
            self.expression = "Erro"
            return "Erro"

    def sqrt_current_from_expr(self, num_str):
        try:
            val = float(num_str)
            if val < 0:
                self.expression = "Erro"
                return "Erro"
            result = math.sqrt(val)
            result_str = str(int(result)) if result == int(result) else str(result)
            entry = f"√{num_str} = {result_str}"
            self.history.insert(0, entry)
            if len(self.history) > 10:
                self.history.pop()
            self._save_history()
            self.expression = result_str
            return result_str
        except Exception:
            self.expression = "Erro"
            return "Erro"

    def get_history_string(self):
        return "\n".join(self.history)