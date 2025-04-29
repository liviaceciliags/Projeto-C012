# core/caixa.py

import threading
import time

class Caixa(threading.Thread):
    """
    Classe que representa um Caixa de pagamento em um restaurante virtual.
    Responsável por processar pagamentos dos clientes de forma assíncrona.
    
    Atributos:
        id (int): Identificador único do caixa
        config (object): Configurações do sistema
        fila_caixa: Fila de clientes aguardando pagamento
        estado (str): Estado atual (DISPONÍVEL/PROCESSANDO)
        _ativo (bool): Flag para controle da execução da thread
    """
    
    def __init__(self, id: int, fila_caixa, config):
        """
        Inicializa o caixa com suas configurações básicas
        
        Args:
            id: Número de identificação do caixa
            fila_caixa: Fila de clientes para atendimento
            config: Objeto de configuração com parâmetros do sistema
        """
        super().__init__(daemon=True)
        self.id = id
        self.config = config
        self.fila_caixa = fila_caixa
        self.estado = "DISPONÍVEL"
        self._ativo = True  # Controla o ciclo de vida da thread

    def run(self):
        """
        Método principal da thread que processa clientes continuamente:
        1. Obtém próximo cliente da fila
        2. Processa seu pagamento
        Executa enquanto o caixa estiver ativo
        """
        while self._ativo:
            try:
                cliente = self.fila_caixa.proximo_cliente()
                self.processar_pagamento(cliente)
            except:
                break  # Encerra em caso de erros na fila

    def processar_pagamento(self, cliente):
        """
        Executa o processo completo de pagamento:
        1. Atualiza estado para PROCESSANDO
        2. Simula tempo de processamento
        3. Libera cliente para saída
        
        Args:
            cliente: Objeto Cliente a ter pagamento processado
        """
        self.estado = "PROCESSANDO"
        print(f"💸 [Caixa {self.id}] Processando pagamento do Cliente {cliente.id}")
        
        # Simula tempo de processamento conforme configuração
        time.sleep(self.config.tempoProcessamentoPagamento)
        
        print(f"✅ [Caixa {self.id}] Pagamento do Cliente {cliente.id} concluído")
        cliente.estado = "SAINDO"  # Libera cliente para sair do sistema
        self.estado = "DISPONÍVEL"

    def parar(self):
        """
        Encerra a operação do caixa de forma segura
        """
        self._ativo = False