def congruencial_mixto(seed: int, a: int, c: int, m: int, cantidad: int) -> list:
    """
    Generador Congruencial Mixto.
    Parámetros:
        seed: semilla inicial
        a: multiplicador
        c: constante aditiva
        m: módulo
        cantidad: cuántos números generar
    Retorna:
        Lista de números pseudoaleatorios normalizados en [0,1)
    """
    resultados = []
    valor = seed
    for _ in range(cantidad):
        valor = (a * valor + c) % m
        resultados.append(valor / m)
    return resultados
