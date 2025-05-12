def cuadrados_medios(seed: int, cantidad: int) -> list:
    """
    Generador de Cuadrados Medios.
    Parámetros:
        seed: semilla inicial (de 4 cifras preferentemente)
        cantidad: cuántos números generar
    Retorna:
        Lista de números pseudoaleatorios normalizados en [0,1)
    """
    resultados = []
    valor = seed
    for _ in range(cantidad):
        cuadrado = str(valor ** 2).zfill(8)  # aseguramos 8 dígitos
        medio = int(cuadrado[2:6])           # tomamos los 4 del medio
        resultados.append(medio / 10000)     # normalizamos
        valor = medio
    return resultados
