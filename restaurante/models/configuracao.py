# models/configuracao.py

class ConfiguracaoRestaurante:
    """Armazena parâmetros globais de configuração do sistema do restaurante."""
    
    def __init__(
        self,
        numeroMesas: int = 5,
        numeroGarcons: int = 2,
        numeroChefs: int = 1,
        numeroCaixas: int = 1,
        probabilidadeChegadaCliente: float = 0.7,
        tempoPreparoPedido: float = 2,
        tempoComerCliente: float = 0.5,
        tempoProcessamentoPagamento: float = 0.1,
        tempoFuncionamento: int = 15
    ):
        """
        Inicializa a configuração com valores padrão ou customizados.
        
        Parâmetros:
        - numeroMesas: Quantidade total de mesas no restaurante (padrão: 5)
        - numeroGarcons: Quantidade total de garçons no restaurante (padrão: 2)
        - numeroChefs: Quantidade total de chefs no restaurante (padrão: 1)
        - numeroCaixas: Quantidade total de caixas no restaurante (padrão: 1)
        - probabilidadeChegadaCliente: Chance por segundo de um novo cliente chegar (0.0 a 1.0, padrão: 0.7)
        - tempoPreparoPedido: Tempo em segundos para preparar um pedido (padrão: 2)
        - tempoComerCliente: Tempo em segundos que o cliente leva para comer (padrão: 0.5)
        - tempoProcessamentoPagamento: Tempo em segundos para processar pagamento (padrão: 0.1)
        - tempoFuncionamento: Tempo total em segundos de operação (padrão: 15)
        """
        self.numeroMesas = numeroMesas
        self.numeroGarcons = numeroGarcons
        self.numeroChefs = numeroChefs
        self.numeroCaixas = numeroCaixas
        self.probabilidadeChegadaCliente = probabilidadeChegadaCliente
        self.tempoPreparoPedido = tempoPreparoPedido
        self.tempoComerCliente = tempoComerCliente
        self.tempoProcessamentoPagamento = tempoProcessamentoPagamento
        self.tempoFuncionamento = tempoFuncionamento

    def __repr__(self):
        return (
            f"ConfiguracaoRestaurante("
            f"mesas={self.numeroMesas}, "
            f"garcons={self.numeroGarcons}, "
            f"chefs={self.numeroChefs}, "
            f"caixas={self.numeroCaixas}, "
            f"prob_clientes={self.probabilidadeChegadaCliente}, "
            f"t_preparo={self.tempoPreparoPedido}s, "
            f"t_comer={self.tempoComerCliente}s, "
            f"t_caixa={self.tempoProcessamentoPagamento}s, "
            f"t_total={self.tempoFuncionamento}s)"
        )