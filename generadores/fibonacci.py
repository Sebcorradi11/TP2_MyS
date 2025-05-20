def fibonacci_mod(m1: int, m2: int, cantidad: int, modulo: int = 10000) -> tuple:
    """
    Generador de números pseudoaleatorios basado en la secuencia de Fibonacci modificada.

    Parámetros:
    - m1 (int): Primera semilla inicial.
    - m2 (int): Segunda semilla inicial.
    - cantidad (int): Cantidad de números a generar.
    - modulo (int): Valor del módulo para mantener los valores dentro de un rango.

    Retorna:
    - tuple: (lista de números en [0,1), primera semilla generada internamente)
    """
    resultados = []
    a, b = m1, m2
    primera_semilla = None
    for i in range(cantidad):
        r = (a + b) % modulo
        if i == 0:
            primera_semilla = r
        resultados.append(r / modulo)
        a, b = b, r
    return resultados, primera_semilla

