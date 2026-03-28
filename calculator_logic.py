import math

class CalculatorLogic:
    def __init__(self):
        self.memory = 0.0
        
        # Build safe evaluation environment using the math module
        self.safe_dict = {
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            'asin': math.asin,
            'acos': math.acos,
            'atan': math.atan,
            'sqrt': math.sqrt,
            'log': math.log10,  # general calculator log is base 10
            'ln': math.log,     # general calculator ln is natural log
            'exp': math.exp,
            'abs': abs,
            'pi': math.pi,
            'e': math.e
        }
    
    def format_expression(self, expr: str) -> str:
        """Replace UI symbols with Python operators"""
        replacements = {
            '×': '*',
            '÷': '/',
            '^': '**',
            'xy': '**',
            ',': '',
        }
        formatted = expr
        for old, new in replacements.items():
            formatted = formatted.replace(old, new)
            
        # Add support for implicit multiplication like "2sin(30)" -> "2*sin(30)" or "2(3)" -> "2*(3)"
        # A simple approach for a calculator:
        # We'll just let the standard python eval handle it and if it fails, it fails, 
        # but replacing generic UI stuff is mandatory.
        return formatted

    def evaluate(self, expr: str, is_preview: bool = False):
        if not expr:
            return "" if is_preview else "0"
            
        formatted_expr = self.format_expression(expr)
        
        try:
            # We specifically only allow variables from self.safe_dict
            result = eval(formatted_expr, {"__builtins__": None}, self.safe_dict)
            
            # Format to drop .0 if it's an integer
            if isinstance(result, (int, float)):
                # Handle tiny floating point errors from math module
                result = round(result, 10)
                if result == int(result):
                    return str(int(result))
                return str(result)
            return str(result)
            
        except ZeroDivisionError:
            return "Error: Div by 0" if not is_preview else ""
        except Exception as e:
            return "Error" if not is_preview else ""

    def memory_add(self, current_val_str: str):
        try:
            val = float(self.evaluate(current_val_str))
            self.memory += val
        except:
            pass

    def memory_subtract(self, current_val_str: str):
        try:
            val = float(self.evaluate(current_val_str))
            self.memory -= val
        except:
            pass

    def memory_recall(self) -> str:
        if self.memory == int(self.memory):
            return str(int(self.memory))
        return str(self.memory)

    def memory_clear(self):
        self.memory = 0.0
