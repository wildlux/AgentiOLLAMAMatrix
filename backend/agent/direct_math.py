"""
Modulo per calcoli matematici diretti usando librerie Python
"""

import numpy as np
import sympy as sp
from sympy import symbols, Eq, solve, diff, integrate, limit, oo
from sympy.plotting import plot
from sympy.abc import x, y, z
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from typing import Dict, List, Union, Tuple

class DirectMathSolver:
    """Classe per risolvere problemi matematici usando librerie Python"""
    
    def __init__(self):
        self.use_direct = True  # Flag per usare calcoli diretti
    
    def solve_equation(self, equation: str) -> Dict:
        """Risolvi un'equazione usando SymPy"""
        try:
            # Converti l'equazione in formato SymPy
            eq = self._parse_equation(equation)
            
            # Risolvi l'equazione
            solutions = solve(eq, x)
            
            # Prepara il risultato
            result = {
                "equation": equation,
                "solutions": str(solutions),
                "type": "direct",
                "method": "SymPy",
                "success": True
            }
            
            # Aggiungi passaggi se possibile
            if len(solutions) > 0:
                result["steps"] = [
                    f"Equazione: {equation}",
                    f"Soluzioni trovate: {solutions}",
                    "Metodo: risoluzione simbolica con SymPy"
                ]
            
            return result
            
        except Exception as e:
            return {
                "equation": equation,
                "error": str(e),
                "type": "direct",
                "success": False
            }
    
    def _parse_equation(self, equation: str) -> Eq:
        """Parsing dell'equazione in formato SymPy"""
        # Sostituisci ^ con ** per la notazione Python
        equation = equation.replace('^', '**')
        
        # Crea l'equazione
        try:
            expr = sp.sympify(equation)
            if '=' in equation:
                return Eq(expr.lhs, expr.rhs)
            else:
                return Eq(expr, 0)
        except:
            # Prova a creare un'espressione semplice
            return sp.sympify(equation)
    
    def calculate_derivative(self, function: str, variable: str = 'x') -> Dict:
        """Calcola la derivata di una funzione"""
        try:
            # Crea la funzione
            f = sp.sympify(function)
            var = symbols(variable)
            
            # Calcola la derivata
            derivative = diff(f, var)
            
            return {
                "function": function,
                "derivative": str(derivative),
                "variable": variable,
                "type": "direct",
                "success": True
            }
        except Exception as e:
            return {
                "error": str(e),
                "type": "direct",
                "success": False
            }
    
    def calculate_integral(self, function: str, variable: str = 'x') -> Dict:
        """Calcola l'integrale di una funzione"""
        try:
            # Crea la funzione
            f = sp.sympify(function)
            var = symbols(variable)
            
            # Calcola l'integrale indefinito
            integral = integrate(f, var)
            
            return {
                "function": function,
                "integral": str(integral),
                "variable": variable,
                "type": "direct",
                "success": True
            }
        except Exception as e:
            return {
                "error": str(e),
                "type": "direct",
                "success": False
            }
    
    def calculate_limit(self, function: str, point: str) -> Dict:
        """Calcola il limite di una funzione"""
        try:
            # Parsing della funzione e del punto
            f = sp.sympify(function)
            var = symbols('x')
            
            # Parsing del punto (es. "x->2" o "2")
            if '->' in point:
                var_name, value = point.split('->')
                var = symbols(var_name.strip())
                value = float(value.strip())
            else:
                value = float(point)
            
            # Calcola il limite
            lim = limit(f, var, value)
            
            return {
                "function": function,
                "limit": str(lim),
                "point": point,
                "type": "direct",
                "success": True
            }
        except Exception as e:
            return {
                "error": str(e),
                "type": "direct",
                "success": False
            }
    
    def solve_system(self, equations: List[str]) -> Dict:
        """Risolvi un sistema di equazioni"""
        try:
            # Parsing delle equazioni
            eqs = [self._parse_equation(eq) for eq in equations]
            
            # Risolvi il sistema
            solutions = solve(eqs, dict=True)
            
            return {
                "equations": equations,
                "solutions": str(solutions),
                "type": "direct",
                "success": True
            }
        except Exception as e:
            return {
                "error": str(e),
                "type": "direct",
                "success": False
            }
    
    def generate_plot(self, function: str, x_range: Tuple[float, float] = (-5, 5)) -> Dict:
        """Genera un grafico della funzione"""
        try:
            # Crea la funzione
            f = sp.sympify(function)
            x_vals = np.linspace(x_range[0], x_range[1], 400)
            y_vals = [float(f.subs(x, val)) for val in x_vals]
            
            # Crea il grafico
            plt.figure(figsize=(8, 4))
            plt.plot(x_vals, y_vals, label=f'${sp.latex(f)}$')
            plt.title(f'Grafico di {function}')
            plt.xlabel('x')
            plt.ylabel('f(x)')
            plt.grid(True)
            plt.legend()
            
            # Salva il grafico come immagine base64
            buf = BytesIO()
            plt.savefig(buf, format='png', bbox_inches='tight')
            plt.close()
            image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
            
            return {
                "function": function,
                "plot": f"data:image/png;base64,{image_base64}",
                "type": "direct",
                "success": True
            }
        except Exception as e:
            return {
                "error": str(e),
                "type": "direct",
                "success": False
            }
    
    def set_method(self, use_direct: bool):
        """Imposta il metodo di calcolo"""
        self.use_direct = use_direct
        return {"method": "direct" if use_direct else "llm", "success": True}

class MathMethodSelector:
    """Classe per selezionare il metodo di calcolo (LLM o diretto)"""
    
    def __init__(self):
        self.direct_solver = DirectMathSolver()
        self.use_direct = True  # Default: usa calcoli diretti
    
    def solve(self, equation: str, method: str = "auto") -> Dict:
        """Risolvi usando il metodo selezionato"""
        if method == "direct" or (method == "auto" and self.use_direct):
            return self.direct_solver.solve_equation(equation)
        else:
            # Qui andrebbe la chiamata al modulo LLM
            return {"error": "Metodo LLM non ancora implementato", "success": False}
    
    def set_method(self, method: str):
        """Imposta il metodo preferito"""
        self.use_direct = (method == "direct")
        return {"method": method, "success": True}

# Funzione di utilità per creare un solver
def create_math_solver(use_direct: bool = True):
    """Crea un solver matematico con il metodo preferito"""
    solver = DirectMathSolver()
    solver.set_method(use_direct)
    return solver