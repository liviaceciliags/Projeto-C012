# Estrutura de projeto

## **Classes**

### **Classes Principais**

#### **1. Restaurante (Classe Controladora)**
- Gerencia o ciclo de vida do sistema e recursos compartilhados.
- **Atributos**:
  - `mesasDisponiveis` (Contador)
  - `filaEspera` (Fila thread-safe para clientes aguardando mesa)
  - `filaPedidos` (Fila de pedidos a serem preparados)
  - `filaPedidosProntos` (Fila de pedidos prontos para entrega)
  - `filaCaixa` (Fila de clientes para pagamento)
  - `aberto` (Flag indicando se o restaurante está aceitando novos clientes)
- **Métodos**:
  - `iniciarDia()`: Inicia threads de funcionários e temporizador de 15s.
  - `finalizarDia()`: Para de aceitar novos clientes e aguarda processos finais.
  - `alocarMesa(Cliente)`: Gerencia alocação de mesas (sincronizado).
  - `liberarMesa(Cliente)`: Libera mesa e chama próximo da filaEspera.

---

#### **2. Cliente (Thread)**
- **Atributos**:
  - `id` (Identificador único)
  - `estado` (AGUARDANDO_MESA, FAZENDO_PEDIDO, COMENDO, PAGANDO, etc.)
  - `pedidoAtual` (Pedido realizado)
  - `mesaAlocada` (Referência à mesa ocupada)
- **Métodos**:
  - `run()`: Controla o fluxo do cliente (chegar → sentar → pedir → comer → pagar → sair).
  - `chamarGarcom()`: Notifica um garçom desocupado (via fila de solicitações).
  - `fazerPedido()`: Interage com o garçom para definir o pedido.
  - `receberPedido()`: Chamado pelo garçom quando o pedido está pronto.

---

#### **3. Garçom (Thread)**
- **Atributos**:
  - `id` (Identificador único)
  - `estado` (DISPONÍVEL, ATENDENDO, ENTREGANDO)
- **Métodos**:
  - `run()`: Escuta eventos (solicitações de clientes ou pedidos prontos).
  - `atenderCliente(Cliente)`: Coleta o pedido e o envia para `filaPedidos`.
  - `entregarPedido(Pedido)`: Busca pedido na `filaPedidosProntos` e entrega ao cliente.

---

#### **4. Chef (Thread)**
- **Atributos**:
  - `id` (Identificador único)
  - `estado` (DISPONÍVEL, PREPARANDO)
- **Métodos**:
  - `run()`: Pega pedidos da `filaPedidos`, prepara (delay de 2s) e envia para `filaPedidosProntos`.

---

#### **5. Caixa (Thread Única)**
- **Atributos**:
  - `estado` (DISPONÍVEL, PROCESSANDO)
- **Métodos**:
  - `run()`: Processa clientes da `filaCaixa` sequencialmente (delay de 0.1s por pagamento).

---

### **Classes de Suporte**

#### **1. Pedido**
- Representa um pedido feito por um cliente.
- **Atributos**:
  - `id` (Identificador único)
  - `idCliente` (Cliente que solicitou o pedido)
  - `itens` (Lista de strings descritivas, ex: `["Pizza", "Refrigerante"]`)
  - `estado` (PENDENTE, EM_PREPARO, PRONTO, ENTREGUE)
  - `timestampCriacao` (Momento em que o pedido foi feito)
  - `timestampPronto` (Momento em que o pedido foi finalizado pelo Chef)

---

#### **2. Mesa**
- Representa uma mesa do restaurante.
- **Atributos**:
  - `id` (Identificador único, ex: Mesa 1 a Mesa 5)
  - `disponivel` (Flag booleana indicando se está ocupada)
  - `clienteAtual` (Referência ao cliente sentado, ou `null`)

---

#### **3. ConfiguracaoRestaurante**
- Armazena parâmetros globais do sistema.
- **Atributos**:
  - `numeroMesas` (Quantidade total de mesas)
  - `probabilidadeChegadaCliente` (Ex: 70% por segundo)
  - `tempoPreparoPedido` (Ex: 2000 ms)
  - `tempoComerCliente` (Ex: 500 ms)
  - `tempoProcessamentoCaixa` (Ex: 100 ms)
  - `tempoFuncionamento` (15 segundos)

---

#### **4. EventoRestaurante**
- Usada para logging ou monitoramento de ações.
- **Atributos**:
  - `timestamp` (Data/hora do evento)
  - `tipo` (Ex: CLIENTE_CHEGOU, PEDIDO_ENTREGUE, PAGAMENTO)
  - `idCliente` (Cliente envolvido)
  - `idFuncionario` (Garçom/Chef/Caixa envolvido)
  - `descricao` (Detalhes do evento)

---

#### **5. FilaPedidos**
- Fila thread-safe para gerenciar pedidos pendentes e prontos.
- **Métodos**:
  - `adicionarPedido(Pedido pedido)`
  - `obterProximoPedido()` (Bloqueia até haver pedidos)

---

#### **6. FilaClientes**
- Fila thread-safe para clientes aguardando mesas ou pagamento.
- **Métodos**:
  - `adicionarCliente(Cliente cliente)`
  - `removerCliente()` (Retorna o próximo cliente da fila)

---

## **Interações entre Classes**

1. **Cliente → Mesa**:
   - Quando um cliente é alocado a uma mesa, `Mesa.clienteAtual` é atualizado.
   - Quando o cliente sai, `Mesa.disponivel` é liberado.

2. **Cliente → Garçom**:
   - O cliente chama o garçom via `Restaurante.filaSolicitacoesGarcom`.
   - O garçom responde coletando o pedido (`Pedido.itens`).

3. **Garçom → FilaPedidos**:
   - O garçom adiciona o pedido à `filaPedidos` após anotá-lo.

4. **Chef → FilaPedidos**:
   - O Chef pega pedidos da `filaPedidos`, prepara e os move para `filaPedidosProntos`.

5. **Garçom → FilaPedidosProntos**:
   - Garçons disponíveis pegam pedidos prontos para entrega.

6. **Cliente → Caixa**:
   - Após comer, o cliente entra na `filaCaixa`, onde o caixa processa seu pagamento.

---

### **Exemplo de Fluxo de Objetos**

1. **Cliente 1** chega, ocupa **Mesa 3**.
2. **Garçom 2** atende **Cliente 1**, cria **Pedido 45** (`itens: ["Hambúrguer"]`).
3. **Chef 1** prepara **Pedido 45**, marca como `PRONTO`.
4. **Garçom 3** entrega **Pedido 45** ao **Cliente 1**.
5. **Cliente 1** come, vai para **Caixa**, pagamento processado → **Mesa 3** é liberada.

---


## **Fluxo de Interações**

1. **Início do Dia**:
   - Restaurante inicia `Garçons`, `Chefs`, e `Caixa`.
   - Clientes são criados aleatoriamente (ex: 70% de chance por segundo).

2. **Cliente Chega**:
   - Se `mesasDisponiveis > 0` → senta e chama garçom.
   - Caso contrário → entra na `filaEspera`.

3. **Pedido**:
   - Garçom recebe solicitação → anota pedido → coloca na `filaPedidos`.
   - Chef pega pedido → prepara → coloca na `filaPedidosProntos`.
   - Garçom disponível pega pedido pronto → entrega ao cliente.

4. **Pagamento**:
   - Cliente termina de comer → entra na `filaCaixa`.
   - Caixa processa pagamento → cliente sai do sistema.

5. **Fechamento**:
   - Após 15s, `Restaurante.finalizarDia()` é chamado.
   - Novos clientes são bloqueados, mas os existentes finalizam seus ciclos.

---

## **Estrutura de Pastas e Arquivos**

```
restaurante/
├── core/                    # Classes principais (threads e controladora)
│   ├── __init__.py
│   ├── restaurante.py       # Classe Restaurante (Controladora)
│   ├── cliente.py           # Classe Cliente (Thread)
│   ├── garcom.py            # Classe Garçom (Thread)
│   ├── chef.py              # Classe Chef (Thread)
│   └── caixa.py             # Classe Caixa (Thread)
│
├── models/                  # Classes de dados e configuração
│   ├── __init__.py
│   ├── pedido.py            # Classe Pedido
│   ├── mesa.py              # Classe Mesa
│   ├── configuracao.py      # Classe ConfiguracaoRestaurante (parâmetros)
│   └── evento.py            # Classe EventoRestaurante (logs)
│
├── utils/                   # Utilitários e estruturas thread-safe
│   ├── __init__.py
│   └── filas.py             # Implementação de Filas (FilaPedidos e FilaClientes)
│
└── main.py                  # Script principal para iniciar a simulação
```