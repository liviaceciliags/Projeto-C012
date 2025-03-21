# utils/filas.py

import queue

class FilaPedidos:
    def __init__(self):
        self._fila = queue.Queue()

    def adicionar_pedido(self, pedido):
        self._fila.put(pedido)

    def obter_proximo_pedido(self):
        return self._fila.get()

class FilaPedidosProntos:
    def __init__(self):
        self._fila = queue.Queue()

    def adicionar_pedido_pronto(self, pedido):
        self._fila.put(pedido)

    def obter_proximo_pedido_pronto(self, block=True, timeout=None):
        return self._fila.get(block, timeout)
    
class FilaSolicitacoes:
    def __init__(self):
        self._fila = queue.Queue()
    
    def adicionar_solicitacao(self, item):
        self._fila.put(item)
    
    def get(self, block=True, timeout=None):
        return self._fila.get(block, timeout)