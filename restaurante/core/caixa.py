import threading
import time

class Caixa(threading.Thread):
    def __init__(self, fila_caixa):
        super().__init__(daemon=True)
        self.fila_caixa = fila_caixa
        self.estado = "DISPONÍVEL"
        self._ativo = True

    def run(self):
        while self._ativo:
            try:
                cliente = self.fila_caixa.proximo_cliente()
                self.processar_pagamento(cliente)
            except:
                time.sleep(0.1)

    def processar_pagamento(self, cliente):
        self.estado = "PROCESSANDO"
        print(f"💸 [Caixa] Processando pagamento do Cliente {cliente.id}")
        
        time.sleep(0.1)
        
        print(f"✅ [Caixa] Pagamento do Cliente {cliente.id} concluído")
        cliente.estado = "SAINDO"
        self.estado = "DISPONÍVEL"

    def parar(self):
        self._ativo = False