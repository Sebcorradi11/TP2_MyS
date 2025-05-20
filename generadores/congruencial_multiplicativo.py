def congruencial_multiplicativo(seed: int, a: int, m: int, cantidad: int) -> tuple:
    """
    Generador congruencial multiplicativo clásico.

    Fórmula: Xn+1 = (a * Xn) mod m

    Parámetros:
    - seed (int): Valor inicial (semilla), debe ser > 0.
    - a (int): Constante multiplicativa.
    - m (int): Módulo.
    - cantidad (int): Número de valores a generar.

    Retorna:
    - tuple: (lista de números en [0,1), primera semilla generada)
    """
    resultados = []
    valor = seed
    primera_semilla = None
    for i in range(cantidad):
        valor = (a * valor) % m
        if i == 0:
            primera_semilla = valor
        resultados.append(valor / m)
    return resultados, primera_semilla
