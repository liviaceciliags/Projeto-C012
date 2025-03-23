# core/restaurante.py

import threading
from queue import Queue
from restaurante.models.mesa import Mesa

class Restaurante:
    """
    Classe principal que gerencia toda a operação do restaurante.
    Controla alocação de mesas e fluxo de clientes usando filas thread-safe.
    
    Atributos:
        config (ConfiguracaoRestaurante): Configurações do sistema
        mesas_disponiveis (Queue): Fila de mesas livres (Mesa objects)
        fila_espera (Queue): Fila de clientes aguardando mesas (Cliente objects)
        clientes_atendidos (int): Contador de clientes que ocuparam mesas
    
    Métodos Principais:
        adicionar_cliente: Coloca cliente na fila de espera
        liberar_mesa: Devolve mesa para o pool disponível
    """
    
    def __init__(self, config):
        self.config = config
        self.mesas_disponiveis = Queue(config.numeroMesas)
        self.fila_espera = Queue()
        self.clientes_atendidos = 0
        
        # Inicializa mesas
        for i in range(config.numeroMesas):
            self.mesas_disponiveis.put(Mesa(i + 1))
            
        # Inicia thread de gerenciamento
        threading.Thread(target=self._gerenciar_entrada, daemon=True).start()

    def _gerenciar_entrada(self):
        """
        Processo contínuo em thread separada que:
        1. Monitora mesas disponíveis
        2. Atribui aos clientes na fila de espera
        3. Inicia o ciclo de atendimento dos clientes
        """
        while True:
            if not self.mesas_disponiveis.empty() and not self.fila_espera.empty():
                mesa = self.mesas_disponiveis.get()
                cliente = self.fila_espera.get()
                self._alocar_mesa(mesa, cliente)

    def _alocar_mesa(self, mesa, cliente):
        """
        Realiza a ocupação efetiva da mesa:
        1. Marca a mesa como ocupada
        2. Atualiza contadores
        3. Inicia o atendimento do cliente
        
        Args:
            mesa (Mesa): Mesa a ser ocupada
            cliente (Cliente): Cliente que vai ocupar a mesa
        """
        mesa.ocupar(cliente)
        print(f"🪑 [Mesa {mesa.id}] Cliente {cliente.id} sentou-se")
        self.clientes_atendidos += 1
        cliente.iniciar_atendimento(mesa)

    def adicionar_cliente(self, cliente):
        """Adiciona cliente na fila de espera"""
        print(f"⏳ [Cliente {cliente.id}] entrou na fila de espera")
        self.fila_espera.put(cliente)

    def liberar_mesa(self, mesa):
        """Devolve mesa para o pool disponível"""
        if mesa and not mesa.disponivel:
            mesa.liberar()
            self.mesas_disponiveis.put(mesa)
            print(f"🧹 [Mesa {mesa.id}] liberada")