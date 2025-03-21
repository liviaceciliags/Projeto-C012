# core/cliente.py

import threading
import time
from restaurante.models.pedido import Pedido, EstadoPedido

class Cliente(threading.Thread):
    def __init__(self, id: int, fila_chamados, fila_caixa):
        super().__init__()
        self.id = id
        self.fila_chamados = fila_chamados
        self.fila_caixa = fila_caixa
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
    # Antes de sair, vai para o caixa
        self.estado = "PAGANDO"
        print(f"🏦 Cliente {self.id} entrou na fila do caixa")
        self.fila_caixa.adicionar_cliente(self)
        
        # Aguarda processamento do caixa
        while self.estado != "SAINDO":
            time.sleep(0.1)
            
    def processar_pagamento(self):
        self.estado = "SAINDO"
        print(f"👋 Cliente {self.id} saiu do restaurante")