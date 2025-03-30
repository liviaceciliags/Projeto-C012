# models/pedido.py

from datetime import datetime
from enum import Enum

class EstadoPedido(Enum):
    PENDENTE = "PENDENTE"
    EM_PREPARO = "EM_PREPARO"
    PRONTO = "PRONTO"
    ENTREGUE = "ENTREGUE"

class Pedido:
    def __init__(self, id: int, id_cliente: int, itens: list):
        self.id = id
        self.id_cliente = id_cliente
        self.itens = itens
        self.estado = EstadoPedido.PENDENTE

    def __repr__(self):
        return f"Pedido {self.id} (Cliente {self.id_cliente}): {self.itens} [{self.estado.value}]"