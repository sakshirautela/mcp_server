from mcp.server.fastmcp import FastMCP
import sympy as sp

mcp = FastMCP('Math')

@mcp.tool()
def add(a: int, b: int) -> int:
    return a + b

@mcp.tool()
def subtract(a: float, b: float) -> float:
    return a - b

@mcp.tool()
def multiply(a: float, b: float) -> float:
    return a * b

@mcp.tool()
def divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Division by zero")
    return a / b

@mcp.tool()
def power(a: float, b: float) -> float:
    return a ** b

@mcp.tool()
def derivative(expr: str, var: str) -> str:
    x = sp.symbols(var)
    return str(sp.diff(expr, x))

@mcp.tool()
def integrate(expr: str, var: str) -> str:
    x = sp.symbols(var)
    return str(sp.integrate(expr, x))

@mcp.tool()
def solve_equation(expr: str, var: str) -> list:
    x = sp.symbols(var)
    solutions = sp.solve(expr, x)
    return [str(sol) for sol in solutions]

@mcp.tool()
def area(shape: str, *params: float) -> float:
    """
    Calculate area of common shapes.
    shape: 'circle', 'rectangle', 'triangle'
    params: 
        - circle: radius
        - rectangle: length, width
        - triangle: base, height
    """
    if shape == "circle" and len(params) == 1:
        return float(sp.pi) * params[0] ** 2
    elif shape == "rectangle" and len(params) == 2:
        return params[0] * params[1]
    elif shape == "triangle" and len(params) == 2:
        return 0.5 * params[0] * params[1]
    else:
        raise ValueError("Unsupported shape or wrong parameters")

if __name__ == '__main__':
    mcp.run(transport='stdio')