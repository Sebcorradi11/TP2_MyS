
# Importación de generadores y utilidades
from generadores.cuadrados_medios import cuadrados_medios
from generadores.fibonacci import fibonacci_mod
from generadores.congruencial_aditivo import congruencial_aditivo
from generadores.congruencial_multiplicativo import congruencial_multiplicativo
from generadores.congruencial_mixto import congruencial_mixto
from validacion.chi_cuadrado import chi_cuadrado_uniforme

from tkinter import messagebox
import tkinter as tk
import threading
import time
from collections import defaultdict, deque
import numpy as np
from scipy.stats import chisquare

# Duración de la jornada en minutos (14 horas)
TIEMPO_JORNADA = 840

# Definición de franjas horarias y sus respectivos intervalos de llegada
FRANJAS = [
    (0, 240, (4, 6)),     # 8:00 a 12:00
    (240, 360, (2, 4)),   # 12:00 a 14:00
    (360, 600, (3, 5)),   # 14:00 a 18:00
    (600, 780, (2, 4)),   # 18:00 a 21:00
    (780, 840, (1, 2))    # 21:00 a 22:00
]

# Lista de productos disponibles en el bar
PRODUCTOS = ["sándwich", "jugo", "café", "chipá"]

# Representa un cliente con un ID y pedido
class Cliente:
    def __init__(self, id_cliente, pedido):
        self.id = id_cliente
        self.pedido = pedido

# Representa un recurso limitado (como caja o barra)
class Recurso:
    def __init__(self, cantidad):
        self.cantidad = cantidad
        self.ocupados = 0

    def disponible(self):
        return self.ocupados < self.cantidad

    def ocupar(self):
        self.ocupados += 1

    def liberar(self):
        self.ocupados -= 1

# Simulador principal del Bar UCP
class SimuladorBarUCP:
    def __init__(self, root):
        # Inicialización de la interfaz y variables del sistema
        self.root = root
        self.root.title("Simulación Bar UCP")
        self.clientes = []
        self.reloj = 0
        self.atendidos = 0
        self.cola_caja = []
        self.cola_barra = []
        self.total_cuellos = 0
        self.cuellos_por_hora = defaultdict(int)
        self.contador_pedidos = defaultdict(int)
        self.pedidos_recientes = deque(maxlen=5)

        # Elementos gráficos (entradas y controles)
        frame = tk.Frame(root)
        frame.pack()
        tk.Label(frame, text="Caja:").grid(row=0, column=0)
        self.entry_caja = tk.Entry(frame, width=5)
        self.entry_caja.insert(0, "1")
        self.entry_caja.grid(row=0, column=1)

        tk.Label(frame, text="Barra:").grid(row=1, column=0)
        self.entry_barra = tk.Entry(frame, width=5)
        self.entry_barra.insert(0, "1")
        self.entry_barra.grid(row=1, column=1)

        tk.Label(frame, text="Generador:").grid(row=2, column=0)
        self.var_generador = tk.StringVar(value="Cong. mixto")
        opciones = ["Cuadrados Medios", "Fibonacci", "Cong. aditivo", "Cong. multiplicativo", "Cong. mixto"]
        self.selector = tk.OptionMenu(frame, self.var_generador, *opciones, command=self.actualizar_parametros)
        self.selector.grid(row=2, column=1)

        self.param_frame = tk.Frame(root)
        self.param_frame.pack()

        self.advertencias = tk.Label(root, text="", fg="orange", font=("Consolas", 9), justify="left")
        self.advertencias.pack()
        self.semilla_label = tk.Label(root, text="", fg="green", font=("Consolas", 10))
        self.semilla_label.pack()

        self.btn_inicio = tk.Button(root, text="▶ Iniciar simulación", command=self.iniciar)
        self.btn_inicio.pack(pady=5)
        self.resultado = tk.Label(root, text="", font=("Consolas", 10), justify="left")
        self.resultado.pack()
        self.lista_pedidos = tk.Label(root, text="", justify="left", font=("Consolas", 10))
        self.lista_pedidos.pack()
        self.resultado_chi = tk.Label(root, text="", fg="blue", font=("Consolas", 10))
        self.resultado_chi.pack()

        self.param_entries = {}
        self.actualizar_parametros("Cong. mixto")

    def actualizar_parametros(self, metodo):
        """
        Muestra los campos necesarios según el método seleccionado.
        """
        for widget in self.param_frame.winfo_children():
            widget.destroy()
        self.param_entries.clear()

        campos = {
            "Cuadrados Medios": ["semilla (4 cifras)"],
            "Fibonacci": ["m1 (>0)", "m2 (>0)", "modulo (≥1000)"],
            "Cong. aditivo": ["semillas (coma separadas)", "modulo (≥1000)"],
            "Cong. multiplicativo": ["semilla (>0)", "a (>0)", "modulo (>a)"],
            "Cong. mixto": ["semilla (≥0)", "a (>0)", "c (≥0)", "modulo (>a)"]
        }

        for i, campo in enumerate(campos[metodo]):
            label = tk.Label(self.param_frame, text=campo + ":")
            label.grid(row=i, column=0)
            entry = tk.Entry(self.param_frame)
            entry.grid(row=i, column=1)
            self.param_entries[campo.split()[0]] = entry

    def iniciar(self):
        """
        Inicializa la simulación: recursos, parámetros y generador seleccionado.
        """
        self.recurso_caja = Recurso(int(self.entry_caja.get()))
        self.recurso_barra = Recurso(int(self.entry_barra.get()))
        metodo = self.var_generador.get()
        advertencias = []

        try:
            if metodo == "Cuadrados Medios":
                semilla = int(self.param_entries["semilla"].get())
                self.generador_actual, semilla_generada = cuadrados_medios(seed=semilla, cantidad=10000)
            elif metodo == "Fibonacci":
                m1 = int(self.param_entries["m1"].get())
                m2 = int(self.param_entries["m2"].get())
                modulo = int(self.param_entries["modulo"].get())
                self.generador_actual, semilla_generada = fibonacci_mod(m1, m2, 10000, modulo)
            elif metodo == "Cong. aditivo":
                semillas = list(map(int, self.param_entries["semillas"].get().split(",")))
                modulo = int(self.param_entries["modulo"].get())
                self.generador_actual, semilla_generada = congruencial_aditivo(semillas, 10000, modulo)
            elif metodo == "Cong. multiplicativo":
                semilla = int(self.param_entries["semilla"].get())
                a = int(self.param_entries["a"].get())
                m = int(self.param_entries["modulo"].get())
                self.generador_actual, semilla_generada = congruencial_multiplicativo(semilla, a, m, 10000)
            elif metodo == "Cong. mixto":
                semilla = int(self.param_entries["semilla"].get())
                a = int(self.param_entries["a"].get())
                c = int(self.param_entries["c"].get())
                m = int(self.param_entries["modulo"].get())
                self.generador_actual, semilla_generada = congruencial_mixto(semilla, a, c, m, 10000)

            self.semilla_label.config(text=f"🔑 Primera semilla generada: {semilla_generada}")

        except Exception as e:
            self.resultado.config(text=f"Error en parámetros: {e}")
            return

        self.i_random = 0
        self.reloj = 0
        self.clientes.clear()
        self.atendidos = 0
        self.cola_caja.clear()
        self.cola_barra.clear()
        self.total_cuellos = 0
        self.cuellos_por_hora.clear()
        self.contador_pedidos.clear()
        self.pedidos_recientes.clear()
        self.resultado_chi.config(text="")
        threading.Thread(target=self.simular, daemon=True).start()

    def simular(self):
        """
        Ejecuta el bucle principal de la simulación minuto a minuto.
        """
        while self.reloj < TIEMPO_JORNADA:
            self.controlar_llegadas()
            self.detectar_cuello()
            self.atender_caja()
            self.atender_barra()
            self.reloj += 1
            self.root.after_idle(self.actualizar_vista)
            time.sleep(0.05)
        self.validar_chi_cuadrado()

    def controlar_llegadas(self):
        """
        Simula la llegada de clientes usando el generador seleccionado.
        """
        if self.reloj % self.obtener_intervalo_llegada() == 0:
            r = self.obtener_random()
            indice = int(r * len(PRODUCTOS))
            pedido = PRODUCTOS[indice % len(PRODUCTOS)]
            cliente = Cliente(len(self.clientes)+1, pedido)
            self.clientes.append(cliente)
            self.cola_caja.append(cliente)
            self.contador_pedidos[pedido] += 1
            self.pedidos_recientes.appendleft(f"Cliente {cliente.id}: {pedido}")

    def detectar_cuello(self):
        """
        Detecta y registra cuellos de botella si hay más de 3 clientes en caja.
        """
        if len(self.cola_caja) > 3:
            hora = 8 + self.reloj // 60
            self.cuellos_por_hora[hora] += 1
            self.total_cuellos += 1

    def obtener_intervalo_llegada(self):
        """
        Devuelve el intervalo aleatorio de llegada según la franja horaria.
        """
        for ini, fin, (min_l, max_l) in FRANJAS:
            if ini <= self.reloj < fin:
                r = self.obtener_random()
                return min_l + int(r * (max_l - min_l + 1))
        return 5

    def atender_caja(self):
        """
        Atiende los clientes en la caja si hay recursos libres.
        """
        while self.cola_caja and self.recurso_caja.disponible():
            cliente = self.cola_caja.pop(0)
            self.recurso_caja.ocupar()
            threading.Thread(target=self.finalizar_caja, args=(cliente,), daemon=True).start()

    def finalizar_caja(self, cliente):
        """
        Simula la atención en caja. Si es café, pasa a la barra.
        """
        time.sleep((2 + int(self.obtener_random() * 3)) * 0.05)
        self.recurso_caja.liberar()
        if cliente.pedido == "café":
            self.cola_barra.append(cliente)
        else:
            self.atendidos += 1

    def atender_barra(self):
        """
        Atiende a los clientes que esperan café en la barra.
        """
        while self.cola_barra and self.recurso_barra.disponible():
            cliente = self.cola_barra.pop(0)
            self.recurso_barra.ocupar()
            threading.Thread(target=self.finalizar_barra, daemon=True, args=(cliente,)).start()

    def finalizar_barra(self, cliente):
        """
        Simula la atención en barra.
        """
        time.sleep((3 + int(self.obtener_random() * 4)) * 0.05)
        self.recurso_barra.liberar()
        self.atendidos += 1

    def obtener_random(self):
        """
        Obtiene un valor pseudoaleatorio de la secuencia generada.
        """
        if self.i_random >= len(self.generador_actual):
            self.i_random = 0
        val = self.generador_actual[self.i_random]
        self.i_random += 1
        return val

    def actualizar_vista(self):
        """
        Actualiza los datos de la simulación en pantalla.
        """
        hora = 8 + self.reloj // 60
        reloj_texto = f"{hora:02}:{self.reloj % 60:02}"
        hora_max = max(self.cuellos_por_hora, key=self.cuellos_por_hora.get, default="N/A")
        cuello_pct = (self.total_cuellos / self.reloj) * 100 if self.reloj > 0 else 0
        self.resultado.config(text=(
            f"🕒 Hora: {reloj_texto} | Minuto {self.reloj}\n"
            f"👥 Caja: {self.recurso_caja.ocupados}/{self.recurso_caja.cantidad} | Barra: {self.recurso_barra.ocupados}/{self.recurso_barra.cantidad}\n"
            f"📥 Clientes: {len(self.clientes)} | Atendidos: {self.atendidos}\n"
            f"⚠️ Cuellos: {self.total_cuellos} ({cuello_pct:.1f}%) | Más a las: {hora_max}hs\n"
            f"📊 Pedidos: {dict(self.contador_pedidos)}"
        ))
        self.lista_pedidos.config(text="📋 Últimos pedidos:\n" + "\n".join(list(self.pedidos_recientes)))

    def validar_chi_cuadrado(self):
        """
        Aplica el test chi-cuadrado a los primeros 100 números generados.
        """
        datos = self.generador_actual[:100]
        obs, _ = np.histogram(datos, bins=10, range=(0, 1))
        chi2_stat, _ = chisquare(obs)
        critico = 16.919
        resultado = f"--- Test Chi-cuadrado ---\nχ² observado: {chi2_stat:.3f}\nχ² crítico: {critico}\n¿Pasa?: {'✅ Sí' if chi2_stat < critico else '❌ No'}"
        self.resultado_chi.config(text=resultado)

# Ejecuta la interfaz y simulación
def iniciar_simulacion():
    """
    Inicia la aplicación gráfica Tkinter.
    """
    root = tk.Tk()
    app = SimuladorBarUCP(root)
    root.mainloop()

iniciar_simulacion()
