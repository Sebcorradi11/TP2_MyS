def congruencial_mixto(seed: int, a: int, c: int, m: int, cantidad: int) -> tuple:
    """
    Generador congruencial mixto (con componente aditivo).

    Fórmula: Xn+1 = (a * Xn + c) mod m

    Parámetros:
    - seed (int): Semilla inicial.
    - a (int): Constante multiplicativa.
    - c (int): Constante aditiva.
    - m (int): Módulo.
    - cantidad (int): Número de valores a generar.

    Retorna:
    - tuple: (lista de números en [0,1), primera semilla generada)
    """
    resultados = []
    valor = seed
    primera_semilla = None
    for i in range(cantidad):
        valor = (a * valor + c) % m
        if i == 0:
            primera_semilla = valor
        resultados.append(valor / m)
    return resultados, primera_semilla


