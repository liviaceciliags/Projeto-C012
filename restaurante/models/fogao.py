# models/pedido.py

import threading

class Fogao:
    """
    Classe que representa um fogão compartilhado por chefs.
    Utiliza um semáforo para garantir que apenas um chef utilize o fogão por vez.
    """
    def __init__(self, id: int):
        self.id = id
        # Semáforo com valor 1 para acesso exclusivo
        self._semaforo = threading.Semaphore(1)
        self._chef_atual = None

    def tentar_usar(self, chef):
        """
        Tenta usar o fogão de forma não bloqueante.
        """
        
        self._usuario_atual = chef
        print(f"👨‍🍳 [Chef {chef.id}] conseguiu usar o fogão {self.id}.")
        return True

    def liberar(self, chef):
        """
        Chef libera o fogão, permitindo que outro chef utilize.
        """
        print(f"👨‍🍳 [Chef {chef.id}] liberou o fogão {self.id}.")
        self._usuario_atual = None