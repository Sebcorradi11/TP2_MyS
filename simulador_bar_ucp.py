import tkinter as tk
import threading
import time
from collections import defaultdict, deque
import random
import secrets
import numpy as np
from scipy.stats import chisquare

# Importar tus generadores
from generadores.cuadrados_medios import cuadrados_medios
from generadores.fibonacci import fibonacci_mod as fibonacci
from generadores.congruencial_aditivo import congruencial_aditivo
from generadores.congruencial_multiplicativo import congruencial_multiplicativo
from generadores.congruencial_mixto import congruencial_mixto

TIEMPO_JORNADA = 840
FRANJAS = [
    (0, 240, (4, 6)),
    (240, 360, (2, 4)),
    (360, 600, (3, 5)),
    (600, 780, (2, 4)),
    (780, 840, (1, 2))
]
PRODUCTOS = ["sándwich", "jugo", "café", "chipá"]

class Cliente:
    def __init__(self, id_cliente, pedido):
        self.id = id_cliente
        self.pedido = pedido

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

class SimuladorBarUCP:
    def __init__(self, root):
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
        self.generadores = {
        "Von Neumann (Cuadrados Medios)": lambda: cuadrados_medios(seed=secrets.randbelow(10**8), cantidad=10000),
        "Fibonacci": lambda: fibonacci(secrets.randbelow(1000), secrets.randbelow(1000), 10000, 10000),
        "Cong. aditivo": lambda: congruencial_aditivo(
            [secrets.randbelow(1000), secrets.randbelow(1000)], 10000, 10000),
        "Cong. multiplicativo": lambda: congruencial_multiplicativo(
            seed=secrets.randbelow(1000), a=secrets.randbelow(10000), m=10007, cantidad=10000),
        "Cong. mixto": lambda: congruencial_mixto(
            seed=secrets.randbelow(2**32), a=1664525, c=1013904223, m=2**32, cantidad=10000)
       }

        # Interfaz
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
        self.selector = tk.OptionMenu(frame, self.var_generador, *self.generadores.keys())
        self.selector.grid(row=2, column=1)
        self.btn_inicio = tk.Button(root, text="▶ Iniciar simulación", command=self.iniciar)
        self.btn_inicio.pack(pady=5)
        self.resultado = tk.Label(root, text="", font=("Consolas", 10), justify="left")
        self.resultado.pack()
        self.lista_pedidos = tk.Label(root, text="", justify="left", font=("Consolas", 10))
        self.lista_pedidos.pack()
        self.resultado_chi = tk.Label(root, text="", fg="blue", font=("Consolas", 10))
        self.resultado_chi.pack()

    def iniciar(self):
        self.recurso_caja = Recurso(int(self.entry_caja.get()))
        self.recurso_barra = Recurso(int(self.entry_barra.get()))
        self.generador_actual = self.generadores[self.var_generador.get()]()
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
        if self.reloj % self.obtener_intervalo_llegada() == 0:
            pedido = random.choice(PRODUCTOS)
            cliente = Cliente(len(self.clientes)+1, pedido)
            self.clientes.append(cliente)
            self.cola_caja.append(cliente)
            self.contador_pedidos[pedido] += 1
            self.pedidos_recientes.appendleft(f"Cliente {cliente.id}: {pedido}")

    def detectar_cuello(self):
        if len(self.cola_caja) > 3:
            hora = 8 + self.reloj // 60
            self.cuellos_por_hora[hora] += 1
            self.total_cuellos += 1

    def obtener_intervalo_llegada(self):
        for ini, fin, (min_l, max_l) in FRANJAS:
            if ini <= self.reloj < fin:
                r = self.obtener_random()
                return min_l + int(r * (max_l - min_l + 1))
        return 5

    def atender_caja(self):
        while self.cola_caja and self.recurso_caja.disponible():
            cliente = self.cola_caja.pop(0)
            self.recurso_caja.ocupar()
            threading.Thread(target=self.finalizar_caja, args=(cliente,), daemon=True).start()

    def finalizar_caja(self, cliente):
        time.sleep((2 + int(self.obtener_random() * 3)) * 0.05)
        self.recurso_caja.liberar()
        if cliente.pedido == "café":
            self.cola_barra.append(cliente)
        else:
            self.atendidos += 1

    def atender_barra(self):
        while self.cola_barra and self.recurso_barra.disponible():
            cliente = self.cola_barra.pop(0)
            self.recurso_barra.ocupar()
            threading.Thread(target=self.finalizar_barra, daemon=True, args=(cliente,)).start()

    def finalizar_barra(self, cliente):
        time.sleep((3 + int(self.obtener_random() * 4)) * 0.05)
        self.recurso_barra.liberar()
        self.atendidos += 1

    def obtener_random(self):
        if self.i_random >= len(self.generador_actual):
            self.i_random = 0
        val = self.generador_actual[self.i_random]
        self.i_random += 1
        return val

    def actualizar_vista(self):
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
        datos = self.generador_actual[:100]
        obs, _ = np.histogram(datos, bins=10, range=(0, 1))
        chi2_stat, _ = chisquare(obs)
        critico = 16.919  # α=0.05 con 9 grados de libertad
        resultado = f"--- Test Chi-cuadrado ---\nχ² observado: {chi2_stat:.3f}\nχ² crítico: {critico}\n¿Pasa?: {'✅ Sí' if chi2_stat < critico else '❌ No'}"
        self.resultado_chi.config(text=resultado)

def iniciar_simulacion():
    root = tk.Tk()
    app = SimuladorBarUCP(root)
    root.mainloop()

iniciar_simulacion()
