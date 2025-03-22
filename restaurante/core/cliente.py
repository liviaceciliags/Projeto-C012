# core/cliente.py

import threading
import time
from restaurante.models.pedido import Pedido, EstadoPedido

class Cliente(threading.Thread):
    """
    Classe que representa um Cliente em um restaurante virtual.
    Controla todo o ciclo do cliente desde a entrada até a saída do estabelecimento.
    
    Atributos:
        id (int): Identificador único do cliente
        config (object): Configurações do sistema
        fila_chamados: Fila para solicitar atendimento dos garçons
        fila_caixa: Fila para pagamento final
        pedido (Pedido): Pedido realizado pelo cliente
        estado (str): Estado atual do cliente (AGUARDANDO_MESA/CHAMANDO_GARCOM/COMENDO/PAGANDO/SAINDO)
        _pedido_recebido (threading.Event): Sinalização de recebimento do pedido
    """
    
    def __init__(self, id: int, fila_chamados, fila_caixa, config):
        """
        Inicializa o cliente com suas configurações básicas
        
        Args:
            id: Número de identificação do cliente
            fila_chamados: Fila para chamar atendimento dos garçons
            fila_caixa: Fila para processamento de pagamentos
            config: Objeto de configuração com parâmetros do sistema
        """
        super().__init__()
        self.id = id
        self.config = config
        self.fila_chamados = fila_chamados
        self.fila_caixa = fila_caixa
        self.pedido = None
        self.estado = "AGUARDANDO_MESA"
        self._pedido_recebido = threading.Event()

    def run(self):
        """
        Fluxo principal do cliente:
        1. Chama o garçom para fazer o pedido
        2. Aguarda confirmação de recebimento do pedido
        3. Espera até a entrega do pedido
        4. Come o pedido
        5. Vai para o caixa pagar
        """
        self.estado = "CHAMANDO_GARCOM"
        self.chamar_garcom()
        
        # Aguarda confirmação de que o pedido foi recebido pelo garçom
        self._pedido_recebido.wait()
        
        # Aguarda até o pedido ser marcado como ENTREGUE
        while self.pedido.estado != EstadoPedido.ENTREGUE:
            time.sleep(0.1)
        
        self.comer()
        self.sair()

    def chamar_garcom(self):
        """
        Adiciona o cliente na fila de chamados para ser atendido por um garçom
        """
        print(f"🔔 [Cliente {self.id}] chamou o garçom")
        self.fila_chamados.adicionar_chamado(self)

    def fazer_pedido(self):
        """
        Cria o pedido do cliente e notifica o sistema
        
        Returns:
            Pedido: Objeto pedido criado com os itens solicitados
        """
        self.pedido = Pedido(
            id=self.id,
            id_cliente=self.id,
            itens=[f"Prato {self.id}"]
        )
        self._pedido_recebido.set()  # Libera a espera do cliente
        return self.pedido

    def comer(self):
        """
        Simula o tempo que o cliente leva para comer seu pedido
        """
        self.estado = "COMENDO"
        print(f"🍽️ [Cliente {self.id}] está comendo")
        time.sleep(self.config.tempoComerCliente)

    def sair(self):
        """
        Inicia o processo de saída do cliente:
        1. Entra na fila do caixa
        2. Aguarda processamento do pagamento
        """
        self.estado = "PAGANDO"
        print(f"🏦 Cliente {self.id} entrou na fila do caixa")
        self.fila_caixa.adicionar_cliente(self)
        
        # Aguarda finalização do pagamento
        while self.estado != "SAINDO":
            time.sleep(0.1)
            
    def processar_pagamento(self):
        """
        Finaliza o ciclo do cliente após o pagamento ser processado
        """
        self.estado = "SAINDO"
        print(f"👋 Cliente {self.id} saiu do restaurante")