from generadores.cuadrados_medios import cuadrados_medios
from generadores.fibonacci import fibonacci_mod
from generadores.congruencial_aditivo import congruencial_aditivo
from generadores.congruencial_multiplicativo import congruencial_multiplicativo
from generadores.congruencial_mixto import congruencial_mixto
from validacion.chi_cuadrado import chi_cuadrado_uniforme
from simulador_bar_ucp import iniciar_simulacion


def generar_y_validar():
    print("\n=== Generadores Pseudoaleatorios ===")
    print("1. Cuadrados Medios")
    print("2. Fibonacci")
    print("3. Congruencial Aditivo")
    print("4. Congruencial Multiplicativo")
    print("5. Congruencial Mixto")
    opcion = input("Seleccione una opción (1-5): ")
    cantidad = int(input("Ingrese cantidad de números a generar: "))

    if opcion == "1":
        semilla = int(input("Ingrese semilla (ej. 1234): "))
        numeros = cuadrados_medios(semilla, cantidad)

    elif opcion == "2":
        m1 = int(input("Ingrese semilla 1: "))
        m2 = int(input("Ingrese semilla 2: "))
        modulo = int(input("Ingrese módulo (por defecto 10000): ") or 10000)
        numeros = fibonacci_mod(m1, m2, cantidad, modulo)

    elif opcion == "3":
        seeds = input("Ingrese al menos 2 semillas separadas por coma (ej. 123,456): ")
        seed_list = list(map(int, seeds.split(",")))
        modulo = int(input("Ingrese módulo (por defecto 10000): ") or 10000)
        numeros = congruencial_aditivo(seed_list, cantidad, modulo)

    elif opcion == "4":
        seed = int(input("Ingrese semilla: "))
        a = int(input("Ingrese constante multiplicativa a: "))
        m = int(input("Ingrese módulo m: "))
        numeros = congruencial_multiplicativo(seed, a, m, cantidad)

    elif opcion == "5":
        seed = int(input("Ingrese semilla: "))
        a = int(input("Ingrese constante a: "))
        c = int(input("Ingrese constante c: "))
        m = int(input("Ingrese módulo m: "))
        numeros = congruencial_mixto(seed, a, c, m, cantidad)

    else:
        print("Opción inválida")
        return

    print("\n--- Resultados del Test Chi-cuadrado ---")
    resultado = chi_cuadrado_uniforme(numeros)
    print(f"Chi2 observado: {resultado['chi2_observado']:.3f}")
    print(f"Chi2 crítico:   {resultado['chi2_critico']:.3f}")
    print("¿Pasa el test?:", "✅ Sí" if resultado["resultado"] else "❌ No")
    print("Frecuencias observadas por intervalo:", resultado['frecuencias_observadas'])

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

if __name__ == "__main__":
    main()
