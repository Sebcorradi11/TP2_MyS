import math

def chi_cuadrado_uniforme(numeros: list, k: int = 10, alpha: float = 0.05) -> dict:
    """
    Realiza el test de Chi-cuadrado para verificar si una lista de números sigue distribución uniforme.

    Parámetros:
        numeros: lista de números en el intervalo [0,1)
        k: cantidad de intervalos (por defecto 10)
        alpha: nivel de significancia (por defecto 0.05)

    Retorna:
        Diccionario con chi2_observado, chi2_critico, resultado (True=acepta H0)
    """
    n = len(numeros)
    frecuencias_observadas = [0] * k
    for numero in numeros:
        indice = min(int(numero * k), k - 1)  # para evitar índice fuera de rango si es 0.999...
        frecuencias_observadas[indice] += 1

    frecuencia_esperada = n / k
    chi2_observado = sum(
        (fo - frecuencia_esperada) ** 2 / frecuencia_esperada
        for fo in frecuencias_observadas
    )

    # Valor crítico de chi-cuadrado (usamos una tabla simplificada para k hasta 20)
    from scipy.stats import chi2
    chi2_critico = chi2.ppf(1 - alpha, df=k - 1)

    resultado = chi2_observado < chi2_critico

    return {
        "chi2_observado": chi2_observado,
        "chi2_critico": chi2_critico,
        "resultado": resultado,
        "frecuencias_observadas": frecuencias_observadas
    }
from generadores.cuadrados_medios import cuadrados_medios
from validacion.chi_cuadrado import chi_cuadrado_uniforme

