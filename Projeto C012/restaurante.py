import threading
import queue
import random
import time

# Fila de pedidos
fila_pedidos = queue.Queue()

class Cliente(threading.Thread):
    def __init__(self, nome):
        super().__init__()
        self.nome = nome

    def run(self):
        prato = random.choice(["Pizza", "Hambúrguer", "Sushi", "Salada"])
        print(f"🍽️ {self.nome} fez um pedido de {prato}.")
        fila_pedidos.put((self.nome, prato))

        # Espera pelo pedido (simulação do tempo de refeição)
        tempo_espera = random.randint(5, 10)
        time.sleep(tempo_espera)
        print(f"✅ {self.nome} terminou a refeição e saiu do restaurante.")

class Garcom(threading.Thread):
    def run(self):
        while True:
            if not fila_pedidos.empty():
                cliente, prato = fila_pedidos.get()
                print(f"👨‍🍳 Garçom levou o pedido de {prato} do {cliente} para a cozinha.")
                fila_cozinha.put((cliente, prato))
                time.sleep(random.randint(1, 3))  # Tempo para levar o pedido

class Chefe(threading.Thread):
    def run(self):
        while True:
            if not fila_cozinha.empty():
                cliente, prato = fila_cozinha.get()
                tempo_preparo = random.randint(3, 8)
                print(f"🔥 Chef preparando {prato} para {cliente}. Tempo estimado: {tempo_preparo}s")
                time.sleep(tempo_preparo)
                print(f"✅ Prato {prato} de {cliente} está pronto!")
                fila_prontos.put((cliente, prato))

class Servico(threading.Thread):
    def run(self):
        while True:
            if not fila_prontos.empty():
                cliente, prato = fila_prontos.get()
                print(f"🍽️ Garçom serviu {prato} para {cliente}.")

# Fila para pedidos na cozinha e pratos prontos
fila_cozinha = queue.Queue()
fila_prontos = queue.Queue()

# Criando threads
clientes = [Cliente(f"Cliente {i}") for i in range(5)]
garcons = [Garcom() for _ in range(2)]
chefes = [Chefe() for _ in range(2)]
servico = Servico()

# Iniciando threads
for cliente in clientes:
    cliente.start()

for garcom in garcons:
    garcom.start()

for chefe in chefes:
    chefe.start()

servico.start()

# Esperando todos os clientes terminarem
for cliente in clientes:
    cliente.join()

print("🏁 O restaurante encerrou as operações.")
