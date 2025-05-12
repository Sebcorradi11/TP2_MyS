def congruencial_multiplicativo(seed: int, a: int, m: int, cantidad: int) -> list:
    """
    Generador Congruencial Multiplicativo.
    Parámetros:
        seed: semilla inicial
        a: constante multiplicativa
        m: módulo
        cantidad: cuántos números generar
    Retorna:
        Lista de números pseudoaleatorios normalizados en [0,1)
    """
    resultados = []
    valor = seed
    for _ in range(cantidad):
        valor = (a * valor) % m
        resultados.append(valor / m)
    return resultados
