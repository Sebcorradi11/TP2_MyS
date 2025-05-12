def congruencial_aditivo(seed_list: list, cantidad: int, modulo: int = 10000) -> list:
    """
    Generador Congruencial Aditivo.
    Parámetros:
        seed_list: lista con al menos dos semillas iniciales
        cantidad: cuántos números generar
        modulo: para normalizar la salida
    Retorna:
        Lista de números pseudoaleatorios normalizados en [0,1)
    """
    resultados = []
    for _ in range(cantidad):
        nuevo = (seed_list[-1] + seed_list[-2]) % modulo
        resultados.append(nuevo / modulo)
        seed_list.append(nuevo)
    return resultados
