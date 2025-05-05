# core/cliente.py

import threading
import time
from restaurante.models.pedido import Pedido, EstadoPedido
import random

class Cliente(threading.Thread):
    """
    Classe que representa um Cliente em um restaurante virtual.
    Gerencia todo o ciclo desde a entrada até a saída do estabelecimento.
    
    Atributos:
        id (int): Identificador único
        restaurante (Restaurante): Referência ao restaurante
        config (object): Configurações do sistema
        fila_chamados (FilaChamados): Fila para solicitar atendimento
        fila_caixa (FilaCaixa): Fila para processar pagamentos
        pedido (Pedido): Pedido realizado pelo cliente
        estado (str): Estado atual (NA_FILA_ESPERA/CHAMANDO_GARCOM/COMENDO/PAGANDO/SAINDO)
        mesa (Mesa): Mesa ocupada pelo cliente
        _pedido_recebido (threading.Event): Sinalização de recebimento do pedido
    """
    
    def __init__(self, id: int, restaurante, fila_chamados, fila_caixa, config):
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
        self.restaurante = restaurante
        self.config = config
        self.fila_chamados = fila_chamados
        self.fila_caixa = fila_caixa
        self.pedido = None
        self.estado = "NA_FILA_ESPERA"
        self.mesa = None
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
        
        # Entra na fila de espera
        self.restaurante.adicionar_cliente(self)
        
        # Aguarda mesa ser atribuída pelo restaurante
        while self.estado == "NA_FILA_ESPERA":
            time.sleep(0.1)
        
        # Aguarda confirmação de que o pedido foi recebido pelo garçom
        self._pedido_recebido.wait()
        
        # Aguarda até o pedido ser marcado como ENTREGUE
        while self.pedido.estado != EstadoPedido.ENTREGUE:
            time.sleep(0.1)
        
        self.comer(self.pedido)
        self.sair()
        
    def iniciar_atendimento(self, mesa):
        """
        Inicia o atendimento do cliente quando uma mesa é alocada.
        Chamado automaticamente pelo Restaurante.
        
        Args:
            mesa (Mesa): Objeto Mesa atribuído ao cliente
        """
        self.mesa = mesa  # Marca que está com mesa
        self.estado = "CHAMANDO_GARCOM"
        self.chamar_garcom()

    def chamar_garcom(self):
        """
        Adiciona o cliente na fila de chamados para ser atendido por um garçom
        """
        print(f"🔔 [Cliente {self.id}] chamou o garçom")
        self.fila_chamados.adicionar_chamado(self)

    def fazer_pedido(self):
        quantidade_itens = random.randint(1, 5)
        itens = [f"Prato {self.id}-{i}" for i in range(quantidade_itens)]
        complexidades = [random.randint(1, 10) for _ in range(quantidade_itens)]

        self.pedido = Pedido(
            id=self.id,
            id_cliente=self.id,
            itens=itens,
            complexidades=complexidades
        )
        self._pedido_recebido.set()
        return self.pedido

    def comer(self, pedido):
        """
        Simula o tempo que o cliente leva para comer seu pedido
        """
        self.estado = "COMENDO"
        print(f"🍽️ [Cliente {self.id}] está comendo")
        time.sleep(sum(pedido.complexidades) * self.config.tempoComerCliente)

    def sair(self):
        """
        Inicia o processo de saída do cliente:
        1. Entra na fila do caixa
        2. Aguarda processamento do pagamento
        """
        self.restaurante.liberar_mesa(self.mesa)
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