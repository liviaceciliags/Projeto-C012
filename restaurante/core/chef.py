# core/chef.py

import threading
import time
from restaurante.models.pedido import EstadoPedido

class Chef(threading.Thread):
    """
    Classe que representa um Chef em um restaurante virtual.
    Herda de Thread para executar o preparo de pedidos em paralelo.
    
    Atributos:
        id (int): Identificador único do chef
        config (object): Objeto de configuração com parâmetros do sistema
        estado (str): Estado atual do chef (DISPONÍVEL/PREPARANDO)
        fila_pedidos (FilaPedidos): Fila de pedidos pendentes para preparo
        fila_prontos (FilaProntos): Fila de pedidos finalizados
        _ativo (bool): Flag para controle da execução da thread
    """
    
    def __init__(self, id: int, fila_pedidos, fila_prontos, config):
        """
        Inicializa o chef com suas configurações básicas
        
        Args:
            id: Número de identificação do chef
            fila_pedidos: Fila de pedidos a serem processados
            fila_prontos: Fila onde serão colocados os pedidos prontos
            config: Objeto de configuração com parâmetros do sistema
        """
        super().__init__(daemon=True)
        self.id = id
        self.config = config
        self.estado = "DISPONÍVEL"
        self.fila_pedidos = fila_pedidos
        self.fila_prontos = fila_prontos
        self._ativo = True  # Controla a execução contínua da thread

    def run(self):
        """
        Método principal da thread que processa pedidos continuamente.
        Obtém pedidos da fila e os prepara enquanto estiver ativo.
        """
        while self._ativo:
            try:
                pedido = self.fila_pedidos.obter_proximo_pedido()
                self._preparar_pedido(pedido)
            except:
                break  # Encerra a execução em caso de erros

    def _preparar_pedido(self, pedido):
        """
        Executa o processo de preparo de um pedido, incluindo:
        - Atualização de estados
        - Simulação de tempo de preparo
        - Movimentação do pedido para a fila de prontos
        
        Args:
            pedido: Objeto Pedido a ser preparado
        """
        self.estado = "PREPARANDO"
        pedido.estado = EstadoPedido.EM_PREPARO
        print(f"👨‍🍳 [Chef {self.id}] Preparando pedido {pedido.id}")
        
        # Simula o tempo de preparo usando o valor da configuração
        time.sleep(self.config.tempoPreparoPedido)
        
        # Finaliza o pedido e move para a fila de prontos
        pedido.estado = EstadoPedido.PRONTO
        self.fila_prontos.adicionar_pedido_pronto(pedido)
        print(f"✅ [Chef {self.id}] Pedido {pedido.id} pronto")
        self.estado = "DISPONÍVEL"

    def parar(self):
        """
        Método para encerrar a execução do chef de forma segura
        """
        self._ativo = False