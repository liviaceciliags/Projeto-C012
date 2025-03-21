import threading
import time

class Caixa(threading.Thread):
    def __init__(self, id: int, fila_caixa, config):
        super().__init__(daemon=True)
        self.id = id
        self.config = config
        self.fila_caixa = fila_caixa
        self.estado = "DISPONÍVEL"
        self._ativo = True

    def run(self):
        while self._ativo:
            try:
                cliente = self.fila_caixa.proximo_cliente()
                self.processar_pagamento(cliente)
            except:
                break

    def processar_pagamento(self, cliente):
        self.estado = "PROCESSANDO"
        print(f"💸 [Caixa {self.id}] Processando pagamento do Cliente {cliente.id}")
        
        time.sleep(self.config.tempoProcessamentoPagamento)
        
        print(f"✅ [Caixa {self.id}] Pagamento do Cliente {cliente.id} concluído")
        cliente.estado = "SAINDO"
        self.estado = "DISPONÍVEL"

    def parar(self):
        self._ativo = False