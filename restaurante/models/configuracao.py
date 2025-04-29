# models/configuracao.py

class ConfiguracaoRestaurante:
    """
    Classe central de configuração do sistema do restaurante.
    Armazena todos os parâmetros ajustáveis para operação do estabelecimento.
    
    Atributos:
        numeroMesas (int): Quantidade de mesas disponíveis (capacidade máxima simultânea de clientes)
        numeroGarcons (int): Número total de garçons em atendimento
        numeroChefs (int): Número total de chefs na cozinha
        numeroCaixas (int): Número de caixas para processar pagamentos
        probabilidadeChegadaCliente (float): Probabilidade por segundo de novos clientes chegarem (0.0 a 1.0)
        tempoPreparoPedido (float): Tempo médio de preparo de um pedido em segundos
        tempoComerCliente (float): Tempo médio que cliente leva para comer em segundos
        tempoProcessamentoPagamento (float): Tempo médio para processar um pagamento em segundos
        tempoFuncionamento (int): Tempo total de operação do restaurante em segundos
    """
    
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
        
        Args:
            numeroMesas: Capacidade simultânea de clientes (padrão: 5)
            numeroGarcons: Garçons disponíveis para atendimento (padrão: 2)
            numeroChefs: Capacidade de produção da cozinha (padrão: 1)
            numeroCaixas: Pontos de pagamento disponíveis (padrão: 1)
            probabilidadeChegadaCliente: Frequência de chegada de clientes (0.0-1.0, padrão: 0.7)
            tempoPreparoPedido: Velocidade da cozinha em segundos (padrão: 2)
            tempoComerCliente: Duração da refeição em segundos (padrão: 0.5)
            tempoProcessamentoPagamento: Eficiência do caixa em segundos (padrão: 0.1)
            tempoFuncionamento: Duração da simulação em segundos (padrão: 15)
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
        """
        Retorna representação legível da configuração para debug
        
        Returns:
            str: String formatada com todos os parâmetros configurados
        """
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