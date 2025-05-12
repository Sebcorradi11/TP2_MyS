def fibonacci_mod(m1: int, m2: int, cantidad: int, modulo: int = 10000) -> list:
    """
    Generador de Fibonacci modificado.
    Parámetros:
        m1, m2: dos semillas iniciales
        cantidad: cuántos números generar
        modulo: para mantener rango fijo
    Retorna:
        Lista de números pseudoaleatorios normalizados en [0,1)
    """
    resultados = []
    a, b = m1, m2
    for _ in range(cantidad):
        r = (a + b) % modulo
        resultados.append(r / modulo)
        a, b = b, r
    return resultados
