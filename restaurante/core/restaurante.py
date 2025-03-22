# core/restaurante.py
import threading
import time
import random
from models.mesa import Mesa
from models.configuracao import ConfiguracaoRestaurante
from utils.filas import FilaPedidos, FilaClientes

class Restaurante:
    def __init__(self, config: ConfiguracaoRestaurante):
        # Configuração do sistema (parâmetros de operação)
        self.config = config
        
        # Recursos compartilhados
        self.mesas_disponiveis = config.numeroMesas  # Contador não protegido
        self.fila_espera = FilaClientes()            # Fila de clientes sem mesa
        self.fila_pedidos = FilaPedidos()            # Pedidos a serem preparados
        self.fila_pedidos_prontos = FilaPedidos()    # Pedidos prontos para entrega
        self.fila_caixa = FilaClientes()             # Clientes para pagamento
        self.fila_solicitacoes = FilaClientes()      # Clientes chamando garçons
        
        # Estado do restaurante (controle básico)
        self.aberto = False  # Flag de operação

        # Inicialização de componentes físicos
        self._inicializar_mesas()       # Cria as mesas do estabelecimento
        self._inicializar_funcionarios()  # Contrata a equipe de trabalho

    def _inicializar_mesas(self):
        """Cria as mesas físicas do restaurante"""
        # Gera mesas sequenciais (ex: Mesa 1, Mesa 2...)
        self.mesas = [Mesa(id=i+1) for i in range(self.config.numeroMesas)]

    def _inicializar_funcionarios(self):
        """Contrata e prepara a equipe de funcionários"""
        from core.garcom import Garcom
        from core.chef import Chef
        from core.caixa import Caixa
        
        # Criação dos funcionários (quantidades fixas)
        self.garcons = [Garcom(id=i+1, restaurante=self) for i in range(2)]  # 2 garçons
        self.chefs = [Chef(id=i+1, restaurante=self) for i in range(1)]      # 1 chef
        self.caixa = Caixa(restaurante=self)                                 # 1 caixa

    def iniciarDia(self):
        """Inicia todas as operações do restaurante"""
        self.aberto = True  # Abre as portas
        
        # Inicia o turno de trabalho dos funcionários
        for garcom in self.garcons:
            garcom.start()  # Garçons começam a trabalhar
        for chef in self.chefs:
            chef.start()    # Chefs iniciam preparo
        self.caixa.start()   # Caixa abre o guichê
        
        # Inicia geração automática de clientes
        threading.Thread(target=self._gerar_clientes, daemon=True).start()
        
        # Programa fechamento automático após tempo configurado
        threading.Timer(
            self.config.tempoFuncionamento, 
            self.finalizarDia
        ).start()

    def _gerar_clientes(self):
        """Gera clientes aleatoriamente enquanto o restaurante está aberto"""
        from core.cliente import Cliente
        
        while self.aberto:
            # Gera cliente com probabilidade configurada (ex: 70% por segundo)
            if random.random() < self.config.probabilidadeChegadaCliente:
                Cliente(restaurante=self).start()  # Cliente entra no restaurante
            time.sleep(1)  # Verifica a cada segundo

    def alocarMesa(self, cliente):
        """Tenta alocar uma mesa para o cliente"""
        # ⚠️ Seção crítica sem proteção contra race conditions
        if self.mesas_disponiveis > 0:
            # Procura primeira mesa disponível
            for mesa in self.mesas:
                if mesa.disponivel:
                    mesa.ocupar(cliente)            # Ocupa a mesa
                    self.mesas_disponiveis -= 1     
                    return True  # Mesa alocada com sucesso
            return False  # Mesas marcadas como indisponíveis inconsistentemente
        # Se não há mesas, coloca na fila de espera
        self.fila_espera.adicionarCliente(cliente)
        return False

    def liberarMesa(self, cliente):
        """Libera uma mesa e chama próximo cliente"""
        cliente.mesa.liberar()               # Libera a mesa física
        self.mesas_disponiveis += 1          
        
        # Tenta alocar próxima pessoa da fila (se houver)
        if not self.fila_espera.esta_vazia():
            proximo = self.fila_espera.removerCliente()
            self.alocarMesa(proximo)

    def finalizarDia(self):
        """Encerra as operações do restaurante"""
        self.aberto = False  # Para de aceitar novos clientes
        
        # Encerra o turno dos funcionários
        for garcom in self.garcons:
            garcom.parar()
        for chef in self.chefs:
            chef.parar()
        self.caixa.parar()