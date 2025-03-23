# models/mesa.py

class Mesa:
    """
    Representa uma mesa física do restaurante com controle de ocupação.
    
    Atributos:
        id (int): Identificador único (iniciando em 1)
        cliente (Cliente): Cliente atual na mesa (None se disponível)
    
    Propriedades:
        disponivel (bool): Indica se a mesa está livre (True) ou ocupada (False)
    """
    
    def __init__(self, id: int):
        self.id = id
        self.cliente = None

    def ocupar(self, cliente):
        """Atribui cliente à mesa"""
        self.cliente = cliente

    def liberar(self):
        """Remove cliente da mesa"""
        self.cliente = None

    @property
    def disponivel(self):
        return self.cliente is None