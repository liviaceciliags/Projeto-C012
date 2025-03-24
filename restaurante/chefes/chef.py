# core/chef.py

import threading
import time
from queue import Empty
from restaurante.models.pedido import EstadoPedido

class Chef(threading.Thread):
    """
    Classe que representa um Chef de cozinha no restaurante.
    Responsável por preparar os pedidos dos clientes.
    
    Atributos:
        id (int): Identificador único do chef.
        fila_pedidos (FilaPedidos): Fila de pedidos aguardando preparo.
        fila_prontos (FilaPedidosProntos): Fila de pedidos prontos para entrega.
        config (ConfiguracaoRestaurante): Configurações do sistema.
        estado (str): Estado atual do chef (DISPONÍVEL ou PREPARANDO).
        _ativo (bool): Flag para controle da execução da thread.
    """

    def __init__(self, id, fila_pedidos, fila_prontos, config):
        """
        Inicializa um novo chef.

        Args:
            id (int): Identificador do chef.
            fila_pedidos (FilaPedidos): Fila compartilhada de pedidos a preparar.
            fila_prontos (FilaPedidosProntos): Fila compartilhada de pedidos prontos.
            config (ConfiguracaoRestaurante): Parâmetros globais de configuração.
        """
        super().__init__(daemon=True)
        self.id = id
        self.fila_pedidos = fila_pedidos
        self.fila_prontos = fila_prontos
        self.config = config
        self.estado = "DISPONÍVEL"
        self._ativo = True

    def run(self):
        """
        Método principal da thread. Executa enquanto o chef estiver ativo:
        1. Pega próximo pedido na fila de pedidos.
        2. Prepara o pedido (simula o tempo de preparo).
        3. Coloca o pedido pronto na fila de prontos.
        """
        print(f"[Chef {self.id}] Iniciou o trabalho.")
        while self._ativo:
            try:
                # Tenta pegar um pedido pendente
                pedido = self.fila_pedidos.obter_proximo_pedido()
                self.estado = "PREPARANDO"

                print(f"[Chef {self.id}] Preparando pedido {pedido.id} do Cliente {pedido.id_cliente}")

                # Atualiza estado do pedido
                pedido.estado = EstadoPedido.EM_PREPARO

                # Simula o tempo de preparo
                time.sleep(self.config.tempoPreparoPedido)

                # Pedido pronto
                pedido.estado = EstadoPedido.PRONTO
                pedido.timestampPronto = time.time()

                print(f"[Chef {self.id}] Pedido {pedido.id} do Cliente {pedido.id_cliente} está pronto!")

                # Coloca o pedido na fila de prontos
                self.fila_prontos.adicionar_pedido_pronto(pedido)

                self.estado = "DISPONÍVEL"

            except Empty:
                # Se a fila estiver vazia, descansa um pouco e continua
                time.sleep(0.1)

            except Exception as e:
                print(f"[Chef {self.id}] Erro durante preparo: {str(e)}")
                time.sleep(0.1)

    def parar(self):
        """
        Encerra a execução da thread de forma segura.
        """
        print(f"[Chef {self.id}] Encerrando o expediente.")
        self._ativo = False
