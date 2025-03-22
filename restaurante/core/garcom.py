# core/garcom.py

import threading
from queue import Empty
from restaurante.models.pedido import EstadoPedido

class Garcon(threading.Thread):
    """
    Classe que representa um Garçom em um restaurante virtual.
    Responsável por atender clientes e gerenciar o fluxo de pedidos.
    
    Atributos:
        id (int): Identificação única do garçom
        estado (str): Estado atual (DISPONÍVEL/ATENDENDO/ENTREGANDO)
        fila_chamados: Fila de clientes solicitando atendimento
        fila_pedidos: Fila de pedidos para envio à cozinha
        fila_prontos: Fila de pedidos prontos para entrega
        _ativo (bool): Flag para controle da execução da thread
    """
    
    def __init__(self, id: int, fila_chamados, fila_pedidos, fila_prontos):
        """
        Inicializa o garçom com suas filas de trabalho
        
        Args:
            id: Número de identificação do garçom
            fila_chamados: Fila de chamados de clientes
            fila_pedidos: Fila onde são colocados os pedidos para preparo
            fila_prontos: Fila de onde são retirados os pedidos prontos
        """
        super().__init__(daemon=True)
        self.id = id
        self.estado = "DISPONÍVEL"
        self.fila_chamados = fila_chamados
        self.fila_pedidos = fila_pedidos
        self.fila_prontos = fila_prontos
        self._ativo = True

    def run(self):
        """
        Método principal da thread que executa continuamente:
        1. Processa solicitações de clientes
        2. Entrega pedidos prontos
        Mantém o ciclo enquanto o garçom estiver ativo
        """
        while self._ativo:
            try:
                self._processar_solicitacoes()
                self._entregar_pedidos_prontos()
            except Exception as e:
                print(f"Erro no Garçom {self.id}: {str(e)}")

    def _processar_solicitacoes(self):
        """
        Processa chamados de clientes e coleta pedidos:
        1. Obtém próximo cliente da fila de chamados
        2. Coleta o pedido do cliente
        3. Encaminha o pedido para a fila de preparo
        """
        try:
            cliente = self.fila_chamados.obter_proximo_chamado()
            self.estado = "ATENDENDO"
            print(f"🚶♀️ [Garçom {self.id}] Atendendo cliente {cliente.id}")
            
            # Interação com o cliente para obter o pedido
            pedido = cliente.fazer_pedido()
            print(f"📝 [Garçom {self.id}] Anotou pedido {pedido.id}")
            self.fila_pedidos.adicionar_pedido(pedido)
            
            self.estado = "DISPONÍVEL"
        except Empty:
            pass  # Ignora se não houver chamados na fila

    def _entregar_pedidos_prontos(self):
        """
        Entrega pedidos finalizados aos clientes:
        1. Obtém próximo pedido pronto da fila
        2. Atualiza estado do pedido para ENTREGUE
        3. Notifica entrega ao cliente
        """
        try:
            pedido = self.fila_prontos.obter_proximo_pedido_pronto()
            self.estado = "ENTREGANDO"
            
            # Finaliza o processo do pedido
            pedido.estado = EstadoPedido.ENTREGUE
            print(f"📦 [Garçom {self.id}] Pedido {pedido.id} entregue ao cliente {pedido.id_cliente}")
            
            self.estado = "DISPONÍVEL"
        except Empty:
            pass  # Ignora se não houver pedidos prontos
        except Exception as e:
            print(f"Erro na entrega: {str(e)}")

    def parar(self):
        """
        Encerra a execução do garçom de forma segura
        """
        self._ativo = False