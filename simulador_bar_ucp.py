import tkinter as tk
import threading
import time
from collections import defaultdict, deque
from generadores.congruencial_mixto import congruencial_mixto
import random
import secrets


TIEMPO_JORNADA = 840  # de 8:00 a 22:00
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
        self.tiempo_llegada = 0
        self.tiempo_caja = 0
        self.tiempo_barra = 0
        self.tiempo_salida = 0

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
        self.reloj = 0
        self.clientes = []
        self.cola_caja = []
        self.cola_barra = []
        self.atendidos = 0
        self.cuellos_por_hora = defaultdict(int)
        self.total_cuellos = 0
        self.contador_pedidos = defaultdict(int)
        self.pedidos_recientes = deque(maxlen=5)
        self.semilla_usada = None
        self.generador = []  # se genera en iniciar()
        self.i_random = 0

        # Interfaz
        frame = tk.Frame(root)
        frame.pack()

        tk.Label(frame, text="Empleados en CAJA:").grid(row=0, column=0)
        self.entry_caja_emp = tk.Entry(frame, width=5)
        self.entry_caja_emp.insert(0, "1")
        self.entry_caja_emp.grid(row=0, column=1)

        tk.Label(frame, text="Empleados en BARRA:").grid(row=1, column=0)
        self.entry_barra_emp = tk.Entry(frame, width=5)
        self.entry_barra_emp.insert(0, "1")
        self.entry_barra_emp.grid(row=1, column=1)

        self.btn_inicio = tk.Button(root, text="▶ Iniciar simulación", command=self.iniciar)
        self.btn_inicio.pack(pady=5)

        self.resultado = tk.Label(root, text="", font=("Consolas", 10), justify="left")
        self.resultado.pack()

        self.lista_pedidos = tk.Label(root, text="📋 Últimos pedidos:\n", justify="left", anchor="w", font=("Consolas", 10))
        self.lista_pedidos.pack()

    def iniciar(self):
        # ✅ Semilla aleatoria en cada simulación
        self.semilla_usada = secrets.randbelow(2**32)
        self.generador = congruencial_mixto(seed=self.semilla_usada, a=1664525, c=1013904223, m=2**32, cantidad=10000)

        self.recurso_caja = Recurso(int(self.entry_caja_emp.get()))
        self.recurso_barra = Recurso(int(self.entry_barra_emp.get()))
        self.simulando = True
        self.reloj = 0
        self.i_random = 0
        self.clientes.clear()
        self.cola_caja.clear()
        self.cola_barra.clear()
        self.atendidos = 0
        self.total_cuellos = 0
        self.cuellos_por_hora.clear()
        self.contador_pedidos.clear()
        self.pedidos_recientes.clear()
        threading.Thread(target=self.ejecutar_simulacion, daemon=True).start()

    def ejecutar_simulacion(self):
        while self.reloj < TIEMPO_JORNADA:
            self.controlar_llegadas()
            self.detectar_cuello()
            self.atender_caja()
            self.atender_barra()
            self.reloj += 1
            self.root.after_idle(self.actualizar_vista)
            time.sleep(0.05)

    def controlar_llegadas(self):
        intervalo = self.obtener_intervalo_llegada()
        if self.reloj % intervalo == 0:
            pedido = random.choice(PRODUCTOS)
            cliente = Cliente(len(self.clientes)+1, pedido)
            cliente.tiempo_llegada = self.reloj
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
        for inicio, fin, (min_l, max_l) in FRANJAS:
            if inicio <= self.reloj < fin:
                r = self.obtener_random()
                return min_l + int(r * (max_l - min_l + 1))
        return 5

    def atender_caja(self):
        while self.cola_caja and self.recurso_caja.disponible():
            cliente = self.cola_caja.pop(0)
            self.recurso_caja.ocupar()
            cliente.tiempo_caja = self.reloj
            threading.Thread(target=self.finalizar_caja, args=(cliente,), daemon=True).start()

    def finalizar_caja(self, cliente):
        duracion = 2 + int(self.obtener_random() * 3)
        time.sleep(duracion * 0.05)
        self.recurso_caja.liberar()
        if cliente.pedido == "café":
            self.cola_barra.append(cliente)
        else:
            cliente.tiempo_salida = self.reloj
            self.atendidos += 1

    def atender_barra(self):
        while self.cola_barra and self.recurso_barra.disponible():
            cliente = self.cola_barra.pop(0)
            self.recurso_barra.ocupar()
            cliente.tiempo_barra = self.reloj
            threading.Thread(target=self.finalizar_barra, args=(cliente,), daemon=True).start()

    def finalizar_barra(self, cliente):
        duracion = 3 + int(self.obtener_random() * 4)
        time.sleep(duracion * 0.05)
        self.recurso_barra.liberar()
        cliente.tiempo_salida = self.reloj
        self.atendidos += 1

    def obtener_random(self):
        if self.i_random >= len(self.generador):
            self.i_random = 0
        valor = self.generador[self.i_random]
        self.i_random += 1
        return valor

    def actualizar_vista(self):
        hora = 8 + self.reloj // 60
        minutos = self.reloj % 60
        reloj_texto = f"{hora:02}:{minutos:02}"
        hora_max = max(self.cuellos_por_hora, key=self.cuellos_por_hora.get, default="N/A")

        porcentaje_cuello = (self.total_cuellos / self.reloj * 100) if self.reloj > 0 else 0

        texto = (
            f"🕒 Hora: {reloj_texto} | Minuto {self.reloj}\n"
            f"👥 Empleados caja: {self.recurso_caja.cantidad} | barra: {self.recurso_barra.cantidad}\n"
            f"📥 Clientes: {len(self.clientes)} | Atendidos: {self.atendidos}\n"
            f"🧾 En cola caja: {len(self.cola_caja)} | Ocupados caja: {self.recurso_caja.ocupados}\n"
            f"🍽️ En barra: {len(self.cola_barra)} | Ocupados barra: {self.recurso_barra.ocupados}\n"
            f"⚠️ Cuello de botella: {self.total_cuellos} casos ({porcentaje_cuello:.1f}%) | Más a las: {hora_max}hs\n"
            f"📊 Pedidos: {dict(self.contador_pedidos)}\n"
            f"🧪 Semilla utilizada: {self.semilla_usada}"
        )
        self.resultado.config(text=texto)

        pedidos_txt = "📋 Últimos pedidos:\n" + "\n".join(list(self.pedidos_recientes))
        self.lista_pedidos.config(text=pedidos_txt)

def iniciar_simulacion():
    root = tk.Tk()
    app = SimuladorBarUCP(root)
    root.mainloop()
