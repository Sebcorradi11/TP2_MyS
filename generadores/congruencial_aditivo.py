def congruencial_aditivo(seed_list: list, cantidad: int, modulo: int = 10000) -> tuple:
    """
    Generador congruencial aditivo.

    Fórmula: Xn = (Xn-1 + Xn-2) mod m

    Parámetros:
    - seed_list (list): Lista con al menos dos valores iniciales.
    - cantidad (int): Número de valores a generar.
    - modulo (int): Módulo para mantener los valores dentro del rango.

    Retorna:
    - tuple: (lista de números en [0,1), primera semilla generada)
    """
    resultados = []
    primera_semilla = None
    for i in range(cantidad):
        nuevo = (seed_list[-1] + seed_list[-2]) % modulo
        if i == 0:
            primera_semilla = nuevo
        resultados.append(nuevo / modulo)
        seed_list.append(nuevo)
    return resultados, primera_semilla
