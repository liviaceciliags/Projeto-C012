# core/cliente.py

import threading
import time
from restaurante.models.pedido import Pedido, EstadoPedido

class Cliente(threading.Thread):
    def __init__(self, id: int, fila_chamados):
        super().__init__()
        self.id = id
        self.fila_chamados = fila_chamados
        self.pedido = None
        self.estado = "AGUARDANDO_MESA"
        self._pedido_recebido = threading.Event()

    def run(self):
        self.estado = "CHAMANDO_GARCOM"
        self.chamar_garcom()
        
        # Aguarda garçom coletar pedido
        self._pedido_recebido.wait()
        
        # Aguarda entrega do pedido
        while self.pedido.estado != EstadoPedido.ENTREGUE:
            time.sleep(0.1)
        
        self.comer()
        self.sair()

    def chamar_garcom(self):
        """Adiciona cliente na fila de chamados"""
        print(f"🔔 [Cliente {self.id}] chamou o garçom")
        self.fila_chamados.adicionar_chamado(self)

    def fazer_pedido(self):
        """Interação direta com o garçom"""
        self.pedido = Pedido(
            id=self.id,
            id_cliente=self.id,
            itens=[f"Prato {self.id}"]
        )
        self._pedido_recebido.set()
        return self.pedido

    def comer(self):
        self.estado = "COMENDO"
        print(f"🍽️ [Cliente {self.id}] está comendo")
        time.sleep(0.5)

    def sair(self):
        self.estado = "SAINDO"
        print(f"👋 [Cliente {self.id}] saiu após comer")