# core/chef.py

import threading
import time
from restaurante.models.pedido import EstadoPedido

class Chef(threading.Thread):
    def __init__(self, id: int, fila_pedidos, fila_prontos):
        super().__init__(daemon=True)
        self.id = id
        self.estado = "DISPONÍVEL"
        self.fila_pedidos = fila_pedidos
        self.fila_prontos = fila_prontos
        self._ativo = True

    def run(self):
        while self._ativo:
            try:
                pedido = self.fila_pedidos.obter_proximo_pedido()
                self._preparar_pedido(pedido)
            except:
                break

    def _preparar_pedido(self, pedido):
        self.estado = "PREPARANDO"
        print(f"👨‍🍳 [Chef {self.id}] Preparando pedido {pedido.id}")
        pedido.estado = EstadoPedido.EM_PREPARO
        
        # Simula tempo de preparo (2 segundos)
        time.sleep(2)
        
        pedido.estado = EstadoPedido.PRONTO
        self.fila_prontos.adicionar_pedido_pronto(pedido)
        print(f"👨‍🍳 [Chef {self.id}] Finalizou o pedido {pedido.id}")
        self.estado = "DISPONÍVEL"

    def parar(self):
        self._ativo = False