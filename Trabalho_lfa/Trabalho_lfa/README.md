# Máquina de Turing Universal

## Descrição do Projeto

Este projeto implementa uma simulação de uma Máquina de Turing Universal em Python, permitindo a execução e visualização de diferentes configurações de máquinas de Turing a partir de um arquivo de configuração em JSON. A Máquina de Turing Universal é uma máquina teórica capaz de simular qualquer outra Máquina de Turing, e este projeto fornece uma interface gráfica para facilitar a interação e a visualização do processo de computação.

## Estrutura do Projeto

- `turing_machine.py`: Script principal que contém a implementação da Máquina de Turing Universal e sua interface gráfica.
- `turing_machine_config.json`: Arquivo de configuração em JSON que define os estados, alfabeto, símbolo branco, estado inicial, estados finais e transições da Máquina de Turing a ser simulada.
- `README.md`: Documento que você está lendo, explicando o projeto e como utilizá-lo.

## Funcionalidades

1. **Carregamento da Configuração**: O código carrega as configurações da máquina a partir de um arquivo JSON, que define os estados, alfabeto, símbolo branco, estado inicial, estados finais e as transições.

2. **Execução da Máquina de Turing**: O código permite a execução de uma sequência de entrada na Máquina de Turing, simulando o processamento da sequência e retornando se a sequência foi "Accepted" ou "Rejected".

3. **Visualização Gráfica da Máquina**: Através do uso de bibliotecas como `networkx` e `matplotlib`, o código cria uma visualização gráfica da Máquina de Turing, mostrando os estados e as transições.

4. **Interface Gráfica (GUI)**: Uma interface gráfica é fornecida para que os usuários possam inserir sequências de entrada, executar a Máquina de Turing e visualizar o resultado, bem como a configuração gráfica da máquina.

## Requisitos

Para executar este projeto, você precisará das seguintes bibliotecas Python:

- `json`
- `tkinter`
- `matplotlib`
- `networkx`

Essas bibliotecas podem ser instaladas via `pip` com o seguinte comando:

pip install matplotlib networkx

## Como Executar

### Configuração

Certifique-se de que o arquivo `turing_machine_config.json` esteja configurado corretamente com os estados e transições desejados.

### Execução

Execute o script `turing_machine.py` em um ambiente Python. Você pode fazer isso a partir da linha de comando com o seguinte comando:

python turing_machine.py

## Interação

A interface gráfica será aberta, permitindo que você insira uma sequência de entrada para ser processada pela Máquina de Turing. Você também pode visualizar a configuração da máquina e o estado das fitas após a execução.

## Estrutura do Código

### Classe TuringMachine

A classe TuringMachine é responsável por toda a lógica da Máquina de Turing Universal. Aqui estão os principais métodos implementados:

- **`__init__`**: Inicializa a máquina carregando a configuração e resetando as fitas.
- **`load_config`**: Carrega as configurações da máquina a partir de um arquivo JSON.
- **`reset_tapes`**: Reseta as fitas e cabeçotes da máquina para o estado inicial.
- **`encode_machine`**: Codifica a máquina para uma forma binária processável.
- **`encode_transition`**: Codifica uma transição específica.
- **`encode_state`**: Codifica um estado em uma forma binária.
- **`encode_symbol`**: Codifica um símbolo em uma forma binária.
- **`execute`**: Executa uma sequência de entrada na máquina e retorna "Accepted" ou "Rejected".
- **`is_valid_input`**: Verifica se a sequência de entrada é válida.
- **`process_transition`**: Processa uma transição da máquina.
- **`expand_tapes_if_needed`**: Expande as fitas se necessário.
- **`move_head`**: Move o cabeçote da fita para a direita ou esquerda.
- **`visualize_machine`**: Cria uma visualização gráfica da máquina.
- **`visualize_tapes`**: Mostra o estado das fitas graficamente.
- **`visualize_gui`**: Cria a interface gráfica para interação com o usuário.

## Autores

1. Felipe Mateus Maximiniano
2. Gabriel Silva
3. Ramon Damasceno Nascimento
