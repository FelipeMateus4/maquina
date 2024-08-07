import json
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

class TuringMachine:
    def __init__(self, config):
        self.states = config['states']
        self.alphabet = config['alphabet']
        self.blank_symbol = config['blank_symbol']
        self.transitions = config['transitions']
        self.initial_state = config['initial_state']
        self.final_states = config['final_states']
        self.current_state = self.initial_state

        # Inicializar a fita com símbolos em branco
        self.tape = np.array([self.blank_symbol] * 300)
        self.head = 50

        # Criar o grafo das transições
        self.graph = nx.DiGraph()
        print("Transitions Format:", self.transitions)  # Depurar formato
        for key, value in self.transitions.items():
            print(f"Key: {key}, Value: {value}")  # Verificar conteúdo
            state, symbol = key.split(',')
            next_state, new_symbol, direction = value
            self.graph.add_edge(state, next_state, symbol=symbol, new_symbol=new_symbol, direction=direction)

    def step(self):
        current_symbol = self.tape[self.head]
        key = f"{self.current_state},{current_symbol}"
        action = self.transitions.get(key, None)

        if action:
            self.current_state, new_symbol, direction = action
            self.tape[self.head] = new_symbol
            if direction == "R":
                self.head += 1
            elif direction == "L":
                self.head -= 1
        else:
            raise Exception(f"No transition found for key {key}")

    def run(self):
        try:
            while self.current_state not in self.final_states:
                self.step()
            return "aceito"
        except Exception as e:
            return "rejeitado"

    def display(self):
        # Exibir a fita sem um monte de 'B' desnecessários
        tape_display = ''.join(self.tape).rstrip(self.blank_symbol)
        print(f"State: {self.current_state}")
        print(f"Tape: {tape_display}")
        print(f"Head Position: {self.head}")
        print("-" * 50)

    def visualize_transitions(self):
        pos = nx.spring_layout(self.graph)
        labels = {(u, v): f"{d['symbol']} -> {d['new_symbol']}, {d['direction']}" for u, v, d in self.graph.edges(data=True)}
        nx.draw(self.graph, pos, with_labels=True, node_size=2000, node_color='lightblue', font_size=10, font_weight='bold')
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=labels)
        plt.show()

def encode_input(input_string, encoding_scheme):
    try:
        encoded = ''.join([encoding_scheme[char] for char in input_string])
        return encoded
    except KeyError as e:
        print(f"Invalid input character: {e}")
        return None

def load_configuration(json_file):
    with open(json_file, 'r') as file:
        config = json.load(file)
    return config

# Esquema de codificação fornecido
encoding_scheme = {
    '0': '1',
    '1': '11',
    'B': '111'
}

# Carregar configuração de um arquivo JSON com o caminho completo
config = load_configuration('turing_machine_config.json')

# Criar a Máquina de Turing
tm = TuringMachine(config)

# Codificar uma entrada de teste
input_string = '0111'
encoded_input = encode_input(input_string, encoding_scheme)

if encoded_input is None:
    print("rejeitado")
else:
    # Verificar se a entrada codificada está no alfabeto da máquina
    if not all(char in tm.alphabet for char in encoded_input):
        print("rejeitado")
    else:
        # Inserir a entrada codificada na fita
        tape = [tm.blank_symbol] * 300
        head_position = 50
        for i, char in enumerate(encoded_input):
            tape[head_position + i] = char

        # Configurar a fita da Máquina de Turing
        tm.tape = tape
        tm.head = head_position

        # Exibir o estado inicial da fita
        tm.display()

        # Executar a Máquina de Turing
        result = tm.run()
        print(result)

        # Exibir o estado final da fita
        tm.display()

        # Substituir "B" por "111" na fita final
        final_tape = ''.join(tm.tape).replace('B', '111')
        final_tape_display = final_tape.rstrip('1')  # Remover símbolos '111' desnecessários no final
        print(f"Final Tape after replacement: {final_tape_display}")

        # Visualizar o grafo das transições
        tm.visualize_transitions()
