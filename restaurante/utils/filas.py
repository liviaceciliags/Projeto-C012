# utils/filas.py

import queue
import time
import threading

class FilaPedidos:
    def __init__(self):
        self._fila = []
        self._lock = threading.Lock()  # Protege acesso concorrente à fila

    def adicionar_pedido(self, pedido, garcom):
        with self._lock:
            self._fila.append(pedido)
            print(f"🧾 [Garçom {garcom.id}] Anotou pedido {pedido.id} com complexidade total {sum(pedido.complexidades)}")

    def obter_proximo_pedido(self, chef):
        while True:
            with self._lock:
                if self._fila:
                    # Pega o pedido pela ordem de chegada (FCFS)
                    pedido_fcfs = self._fila.pop(0)
                    print(f"📊 [Chef {chef.id}] Pegou pedido {pedido_fcfs.id} com complexidade total {sum(pedido_fcfs.complexidades)} (FCFS)")
                    return pedido_fcfs
            time.sleep(0.05)  # Aguarda um breve intervalo se a fila estiver vazia

class FilaPedidosProntos:
    """
    Fila thread-safe para gerenciar pedidos prontos para entrega.
    Inclui métodos auxiliares para monitoramento do estado da fila.
    
    Atributos:
        _fila (queue.Queue): Fila interna para armazenamento dos pedidos prontos
    """
    
    def __init__(self):
        self._fila = queue.Queue()
        
    def esta_vazia(self):
        """
        Verifica se a fila está vazia
        
        Returns:
            bool: True se não há pedidos prontos, False caso contrário
        """
        return self._fila.empty()

    def tamanho(self):
        """
        Retorna o número atual de pedidos na fila
        
        Returns:
            int: Quantidade de pedidos prontos aguardando entrega
        """
        return self._fila.qsize()
        
    def listar_conteudo(self):
        """
        Método de debug que lista os pedidos sem remover da fila
        (Cuidado: Esvazia temporariamente a fila durante a operação)
        
        Returns:
            list: Cópia dos elementos atuais na fila
        """
        items = []
        while True:
            try:
                items.append(self._fila.get_nowait())
            except queue.Empty:
                break
        # Recoloca os itens na fila
        for item in items:
            self._fila.put(item)
        return items

    def adicionar_pedido_pronto(self, pedido):
        """
        Adiciona um pedido concluído à fila de prontos
        
        Args:
            pedido: Objeto Pedido finalizado
        """
        self._fila.put(pedido)

    def obter_proximo_pedido_pronto(self):
        """
        Remove e retorna o próximo pedido pronto da fila (bloqueante)
        
        Returns:
            Pedido: Próximo pedido a ser entregue
        """
        return self._fila.get()
    
class FilaChamados:
    """
    Fila thread-safe para gerenciar chamados de clientes por garçons.
    
    Atributos:
        _fila (queue.Queue): Fila interna de clientes solicitando atendimento
    """
    
    def __init__(self):
        self._fila = queue.Queue()
        
    def tamanho(self):
        """
        Retorna quantidade de chamados pendentes
        
        Returns:
            int: Número de clientes aguardando atendimento
        """
        return self._fila.qsize()
    
    def adicionar_chamado(self, cliente):
        """
        Adiciona um novo cliente à fila de chamados
        
        Args:
            cliente: Objeto Cliente solicitando atendimento
        """
        self._fila.put(cliente)
    
    def obter_proximo_chamado(self):
        """
        Remove e retorna o próximo cliente da fila (bloqueante)
        
        Returns:
            Cliente: Próximo cliente a ser atendido
        """
        return self._fila.get()
    
class FilaCaixa:
    """
    Fila thread-safe para gerenciar clientes aguardando pagamento.
    
    Atributos:
        _fila (queue.Queue): Fila interna de clientes no caixa
    """
    
    def __init__(self):
        self._fila = queue.Queue()
    
    def adicionar_cliente(self, cliente):
        """
        Adiciona cliente à fila do caixa
        
        Args:
            cliente: Objeto Cliente pronto para pagamento
        """
        self._fila.put(cliente)
    
    def proximo_cliente(self):
        """
        Remove e retorna o próximo cliente da fila (bloqueante)
        
        Returns:
            Cliente: Próximo cliente a ter pagamento processado
        """
        return self._fila.get()
    
    def esta_vazia(self):
        """
        Verifica se a fila do caixa está vazia
        
        Returns:
            bool: True se não há clientes, False caso contrário
        """
        return self._fila.empty()
    
    def tamanho(self):
        """
        Retorna quantidade de clientes na fila do caixa
        
        Returns:
            int: Número de clientes aguardando pagamento
        """
        return self._fila.qsize()