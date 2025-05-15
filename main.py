from generadores.cuadrados_medios import cuadrados_medios
from generadores.fibonacci import fibonacci_mod
from generadores.congruencial_aditivo import congruencial_aditivo
from generadores.congruencial_multiplicativo import congruencial_multiplicativo
from generadores.congruencial_mixto import congruencial_mixto
from validacion.chi_cuadrado import chi_cuadrado_uniforme
from simulador_bar_ucp import iniciar_simulacion

# Función para generar números pseudoaleatorios y validarlos con Chi-cuadrado
def generar_y_validar():
    print("\n=== Generadores Pseudoaleatorios ===")
    print("1. Cuadrados Medios")
    print("2. Fibonacci")
    print("3. Congruencial Aditivo")
    print("4. Congruencial Multiplicativo")
    print("5. Congruencial Mixto")

    # Selección de método
    opcion = input("Seleccione una opción (1-5): ")
    cantidad = int(input("Ingrese cantidad de números a generar: "))

    # Opciones para cada generador
    if opcion == "1":
        semilla = int(input("Ingrese semilla (de 4 cifras, ej. 1234): "))
        if semilla < 1000 or semilla > 9999:
            print("⚠️ Semilla recomendada: 4 cifras (1000–9999).")
        numeros = cuadrados_medios(semilla, cantidad)

    elif opcion == "2":
        m1 = int(input("Ingrese semilla 1: "))
        m2 = int(input("Ingrese semilla 2: "))
        if m1 == m2:
            print("⚠️ m1 y m2 deberían ser distintos para mejor aleatoriedad.")
        modulo = int(input("Ingrese módulo (sugerido ≥1000): ") or 10000)
        if modulo < 1000:
            print("⚠️ Se recomienda módulo mayor o igual a 1000.")
        numeros = fibonacci_mod(m1, m2, cantidad, modulo)

    elif opcion == "3":
        seeds = input("Ingrese al menos 2 semillas separadas por coma (ej. 123,456): ")
        seed_list = list(map(int, seeds.split(",")))
        if len(seed_list) < 2:
            print("⚠️ Ingrese al menos 2 semillas para iniciar.")
        modulo = int(input("Ingrese módulo (sugerido ≥1000): ") or 10000)
        if modulo < 1000:
            print("⚠️ Se recomienda módulo mayor o igual a 1000.")
        numeros = congruencial_aditivo(seed_list, cantidad, modulo)

    elif opcion == "4":
        seed = int(input("Ingrese semilla (>0): "))
        a = int(input("Ingrese constante a (>0): "))
        m = int(input("Ingrese módulo m (>a): "))
        if seed <= 0:
            print("⚠️ La semilla debería ser mayor a 0.")
        if a <= 0:
            print("⚠️ 'a' debe ser mayor que 0.")
        if m <= a:
            print("⚠️ 'm' debe ser mayor que 'a'.")
        numeros = congruencial_multiplicativo(seed, a, m, cantidad)

    elif opcion == "5":
        seed = int(input("Ingrese semilla (≥0): "))
        a = int(input("Ingrese constante a (>0): "))
        c = int(input("Ingrese constante c (≥0): "))
        m = int(input("Ingrese módulo m (>a): "))
        if a <= 0:
            print("⚠️ Se recomienda que 'a' > 0.")
        if c < 0:
            print("⚠️ 'c' debe ser positivo o cero.")
        if m <= a:
            print("⚠️ 'm' debe ser mayor que 'a'.")
        if seed < 0:
            print("⚠️ Semilla negativa, resultados podrían no ser válidos.")
        numeros = congruencial_mixto(seed, a, c, m, cantidad)

    else:
        print("Opción inválida")
        return

    # Validación del generador con el test de Chi-cuadrado
    print("\n--- Resultados del Test Chi-cuadrado ---")
    resultado = chi_cuadrado_uniforme(numeros)
    print(f"Chi2 observado: {resultado['chi2_observado']:.3f}")
    print(f"Chi2 crítico:   {resultado['chi2_critico']:.3f}")
    print("¿Pasa el test?:", "✅ Sí" if resultado["resultado"] else "❌ No")
    print("Frecuencias observadas por intervalo:", resultado['frecuencias_observadas'])

# Menú principal por consola
def main():
    while True:
        print("\n=== TP2 – Simulación Bar UCP ===")
        print("1. Generar y validar números pseudoaleatorios")
        print("2. Ir a simulación del bar")
        print("3. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            generar_y_validar()
        elif opcion == "2":
            iniciar_simulacion()
        elif opcion == "3":
            print("Saliendo...")
            break
        else:
            print("Opción inválida.")

# Punto de entrada del programa
if __name__ == "__main__":
    main()
