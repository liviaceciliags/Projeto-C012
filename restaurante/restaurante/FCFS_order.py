import threading
import time
import random
from enum import Enum
from queue import Queue

# Estado do pedido
class EstadoPedido(Enum):
    PENDENTE = "PENDENTE"
    EM_PREPARO = "EM_PREPARO"
    PRONTO = "PRONTO"
    ENTREGUE = "ENTREGUE"

# Classe Pedido
class Pedido:
    def __init__(self, id: int, id_cliente: int, itens: list):
        self.id = id
        self.id_cliente = id_cliente
        self.itens = itens
        self.estado = EstadoPedido.PENDENTE
        self.tempo_preparo = random.randint(3, 8)  # aleatório entre 3 e 8 segundos

    def __repr__(self):
        return (f"Pedido {self.id} (Cliente {self.id_cliente}): {self.itens} "
                f"[{self.estado.value}] - Preparo: {self.tempo_preparo}s")

# Classe Cliente
#class Cliente(threading.Thread):
#    def __init__(self, id, fila_pedidos):
#        super().__init__()
#        self.id = id
#        self.fila_pedidos = fila_pedidos
#
#    def run(self):
#        pedido = Pedido(id=self.id, id_cliente=self.id, itens=[f"Prato {self.id}"])
#        print(f"[Cliente {self.id}] Fez pedido: {pedido}")
#        self.fila_pedidos.put(pedido)
#
## Classe Cozinheiro
#class Cozinheiro(threading.Thread):
#    def __init__(self, fila_pedidos, fila_entregas):
#        super().__init__()
#        self.fila_pedidos = fila_pedidos
#        self.fila_entregas = fila_entregas
#
#    def run(self):
#        while True:
#            pedido = self.fila_pedidos.get()
#            if pedido is None:
#                break  # sinal para parar
#            pedido.estado = EstadoPedido.EM_PREPARO
#            print(f"[Cozinheiro] Preparando {pedido}")
#            time.sleep(pedido.tempo_preparo)
#            pedido.estado = EstadoPedido.PRONTO
#            print(f"[Cozinheiro] Pedido pronto: {pedido}")
#            self.fila_entregas.put(pedido)
#
## Classe Garçom
#class Garcom(threading.Thread):
#    def __init__(self, fila_entregas):
#        super().__init__()
#        self.fila_entregas = fila_entregas
#
#    def run(self):
#        while True:
#            pedido = self.fila_entregas.get()
#            if pedido is None:
#                break
#            pedido.estado = EstadoPedido.ENTREGUE
#            print(f"[Garçom] Entregando {pedido}")
#            time.sleep(1)
#
## Main
#def main():
#    fila_pedidos = Queue()
#    fila_entregas = Queue()
#
#    cozinheiro = Cozinheiro(fila_pedidos, fila_entregas)
#    garcom = Garcom(fila_entregas)
#
#    cozinheiro.start()
#    garcom.start()
#
#    clientes = [Cliente(i, fila_pedidos) for i in range(1, 6)]
#
#    for cliente in clientes:
#        cliente.start()
#
#    for cliente in clientes:
#        cliente.join()
#
#    # Parar threads com None
#    fila_pedidos.put(None)
#    fila_entregas.put(None)
#
#    cozinheiro.join()
#    garcom.join()
#    print("Simulação encerrada.")
#
#if __name__ == "__main__":
#    main()