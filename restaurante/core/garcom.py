# core/garcom.py

import threading
import time
from queue import Empty
from restaurante.models.pedido import EstadoPedido

class Garcon(threading.Thread):
    def __init__(self, id: int, fila_chamados, fila_pedidos, fila_prontos):
        super().__init__(daemon=True)
        self.id = id
        self.estado = "DISPONÍVEL"
        self.fila_chamados = fila_chamados      # Clientes chamando garçons
        self.fila_pedidos = fila_pedidos            # Pedidos para preparo
        self.fila_prontos = fila_prontos            # Pedidos prontos para entrega
        self._ativo = True

    def run(self):
        while self._ativo:
            try:
                self._processar_solicitacoes()
                self._entregar_pedidos_prontos()
            except Exception as e:
                print(f"Erro no Garçom {self.id}: {str(e)}")

    def _processar_solicitacoes(self):
        try:
            cliente = self.fila_chamados.obter_proximo_chamado()
            self.estado = "ATENDENDO"
            print(f"🚶♀️ [Garçom {self.id}] Atendendo cliente {cliente.id}")
            
            # Coleta pedido do cliente
            pedido = cliente.fazer_pedido()
            print(f"📝 [Garçom {self.id}] Anotou pedido {pedido.id}")
            self.fila_pedidos.adicionar_pedido(pedido)
            
            self.estado = "DISPONÍVEL"
        except Empty:
            pass

    def _entregar_pedidos_prontos(self):
        """Entrega pedidos prontos aos clientes"""
        try:
            pedido = self.fila_prontos.obter_proximo_pedido_pronto()
            self.estado = "ENTREGANDO"
            
            # Marca pedido como entregue
            pedido.estado = EstadoPedido.ENTREGUE
            print(f"📦 [Garçom {self.id}] Pedido {pedido.id} entregue ao cliente {pedido.id_cliente}")
            
            self.estado = "DISPONÍVEL"
        except Empty:
            pass
        except Exception as e:
            print(f"Erro na entrega: {str(e)}")

    def parar(self):
        self._ativo = False