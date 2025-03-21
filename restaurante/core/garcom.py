# core/garcom.py

import threading
import time
from queue import Empty
from restaurante.models.pedido import EstadoPedido

class Garcon(threading.Thread):
    def __init__(self, id: int, fila_solicitacoes, fila_pedidos, fila_prontos):
        super().__init__(daemon=True)
        self.id = id
        self.estado = "DISPONÍVEL"
        self.fila_solicitacoes = fila_solicitacoes  # Pedidos solicitados por clientes
        self.fila_pedidos = fila_pedidos            # Pedidos para preparo
        self.fila_prontos = fila_prontos            # Pedidos prontos para entrega
        self._ativo = True

    def run(self):
        while self._ativo:
            try:
                self._processar_solicitacoes()
                self._entregar_pedidos_prontos()
                time.sleep(0.1)  # Reduz consumo de CPU
            except Exception as e:
                print(f"Erro no Garçom {self.id}: {str(e)}")

    def _processar_solicitacoes(self):
        """Coleta novos pedidos dos clientes e envia para a cozinha"""
        try:
            pedido = self.fila_solicitacoes.get(block=False)
            self.estado = "ATENDENDO"
            print(f"🧑🍳 [Garçom {self.id}] Coletou pedido {pedido.id}")
            
            # Envia pedido para preparo
            pedido.estado = EstadoPedido.PENDENTE
            self.fila_pedidos.adicionar_pedido(pedido)
            
            self.estado = "DISPONÍVEL"
        except Empty:
            pass

    def _entregar_pedidos_prontos(self):
        """Entrega pedidos prontos aos clientes"""
        try:
            pedido = self.fila_prontos.obter_proximo_pedido_pronto(block=False)
            self.estado = "ENTREGANDO"
            print(f"🚚 [Garçom {self.id}] Entregando pedido {pedido.id}")
            
            # Marca pedido como entregue
            pedido.estado = EstadoPedido.ENTREGUE
            
            self.estado = "DISPONÍVEL"
        except Empty:
            pass

    def parar(self):
        self._ativo = False