def cuadrados_medios(seed: int, cantidad: int) -> tuple:
    """
    Generador pseudoaleatorio usando el método de Cuadrados Medios de Von Neumann.

    Parámetros:
    - seed (int): Semilla inicial (preferentemente de 4 cifras).
    - cantidad (int): Cantidad de números a generar.

    Retorna:
    - tuple: (lista de números en [0,1), primera semilla generada internamente)
    """
    resultados = []
    valor = seed
    primera_semilla = None
    for i in range(cantidad):
        cuadrado = str(valor ** 2).zfill(8)
        medio = int(cuadrado[2:6])
        if i == 0:
            primera_semilla = medio
        resultados.append(medio / 10000)
        valor = medio
    return resultados, primera_semilla
