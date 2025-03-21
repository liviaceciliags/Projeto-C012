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
        
    def esta_vazia(self):
        return self._fila.empty()

    def tamanho(self):
        return self._fila.qsize()
        
    def listar_conteudo(self):
        """Método para debug: retorna lista de pedidos na fila"""
        items = []
        while True:
            try:
                items.append(self._fila.get_nowait())
            except queue.Empty:
                break
        # Recoloca os itens na fila
        for item in items:
            self._fila.put(item)
        return items

    def adicionar_pedido_pronto(self, pedido):
        self._fila.put(pedido)

    def obter_proximo_pedido_pronto(self):
        return self._fila.get()
    
class FilaChamados:
    def __init__(self):
        self._fila = queue.Queue()
        
    def tamanho(self):
        return self._fila.qsize()
    
    def adicionar_chamado(self, cliente):
        self._fila.put(cliente)
    
    def obter_proximo_chamado(self):
        return self._fila.get()