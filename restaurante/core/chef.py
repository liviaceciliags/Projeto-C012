# core/chef.py

import threading
import time
from restaurante.models.pedido import EstadoPedido

class Chef(threading.Thread):
    def __init__(self, id: int, fila_pedidos, fila_prontos, config):
        super().__init__(daemon=True)
        self.id = id
        self.config = config
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
        pedido.estado = EstadoPedido.EM_PREPARO
        print(f"👨‍🍳 [Chef {self.id}] Preparando pedido {pedido.id}")
        
        # Simula tempo de preparo
        time.sleep(self.config.tempoPreparoPedido)
        
        pedido.estado = EstadoPedido.PRONTO
        self.fila_prontos.adicionar_pedido_pronto(pedido)
        print(f"✅ [Chef {self.id}] Pedido {pedido.id} pronto")
        self.estado = "DISPONÍVEL"

    def parar(self):
        self._ativo = False