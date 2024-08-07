import json

def convert_to_unary(value):
    """Converte um valor para seu formato unário correspondente"""
    if value == '0':
        return '10'
    elif value == '1':
        return '110'
    elif value == 'B':
        return '1110'
    elif value == 'L':
        return '10'
    elif value == 'R':
        return '110'
    elif value.startswith('q'):
        n = int(value[1:])
        return '1' * (n + 1) + '0'
    else:
        raise ValueError(f"Valor não reconhecido para conversão: {value}")

def convert_from_unary(value):
    """Converte um valor do formato unário para o formato original"""
    if value == '10':
        return '0'
    elif value == '110':
        return '1'
    elif value == '1110':
        return 'B'
    elif value == '10':
        return 'L'
    elif value == '110':
        return 'R'
    elif value.endswith('0'):
        n = len(value) - 1
        return f'q{n}'
    else:
        raise ValueError(f"Valor não reconhecido para desconversão: {value}")

def convert_config_to_unary(config):
    """Converte toda a configuração da máquina de Turing para o formato unário"""
    unary_config = {
        'states': [convert_to_unary(state) for state in config['states']],
        'alphabet': [convert_to_unary(symbol) for symbol in config['alphabet']],
        'blank_symbol': convert_to_unary(config['blank_symbol']),
        'initial_state': convert_to_unary(config['initial_state']),
        'final_states': [convert_to_unary(state) for state in config['final_states']],
        'transitions': {
            f"{convert_to_unary(key.split(',')[0])},{convert_to_unary(key.split(',')[1])}": [
                convert_to_unary(value[0]), convert_to_unary(value[1]), convert_to_unary(value[2])
            ]
            for key, value in config['transitions'].items()
        }
    }
    return unary_config

def convert_config_from_unary(unary_config):
    """Converte a configuração da máquina de Turing do formato unário para o formato original"""
    config = {
        'states': [convert_from_unary(state) for state in unary_config['states']],
        'alphabet': [convert_from_unary(symbol) for symbol in unary_config['alphabet']],
        'blank_symbol': convert_from_unary(unary_config['blank_symbol']),
        'initial_state': convert_from_unary(unary_config['initial_state']),
        'final_states': [convert_from_unary(state) for state in unary_config['final_states']],
        'transitions': {
            f"{convert_from_unary(key.split(',')[0])},{convert_from_unary(key.split(',')[1])}": [
                convert_from_unary(value[0]), convert_from_unary(value[1]), convert_from_unary(value[2])
            ]
            for key, value in unary_config['transitions'].items()
        }
    }
    return config

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
        self.tape = [self.blank_symbol] * 300
        self.head = 50

    def read_symbol(self):
        """Lê o símbolo atual da fita considerando os diferentes tamanhos de strings unárias"""
        symbol = ''
        pos = self.head
        while self.tape[pos] != '0':
            symbol += self.tape[pos]
            pos += 1
        return symbol + '0', pos - self.head + 1

    def step(self):
        current_symbol, symbol_length = self.read_symbol()
        key = f"{self.current_state},{current_symbol}"
        action = self.transitions.get(key, None)

        if action:
            next_state, new_symbol, direction = action

            # Atualizar a fita
            new_symbol_length = len(new_symbol)
            self.tape[self.head:self.head + symbol_length] = list(new_symbol)
            
            # Movimentar a cabeça
            if direction == '110':  # 'R' em unário
                self.head += new_symbol_length
            elif direction == '10':  # 'L' em unário
                self.head -= new_symbol_length

            # Atualizar o estado atual
            self.current_state = next_state
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

def load_configuration(json_file):
    with open(json_file, 'r') as file:
        config = json.load(file)
    return config

def main():
    # Carregar configuração de um arquivo JSON com o caminho completo
    config = load_configuration('turing_machine_config.json')

    # Receber entrada do usuário
    input_binary = input("Digite a entrada: ")

    # Converter a configuração para o formato unário
    unary_config = convert_config_to_unary(config)
    print("\nUnary Configuration:")
    print(json.dumps(unary_config, indent=2))

    # Configurar a Máquina de Turing com a configuração unária
    tm = TuringMachine(unary_config)

    # Converter a entrada para o formato unário
    unary_input = ''.join([convert_to_unary(char) for char in input_binary])

    # Inserir a entrada convertida na fita
    head_position = 50
    for symbol in unary_input:
        tm.tape[head_position] = symbol
        head_position += 1

    # Configurar a cabeça da fita
    tm.head = 50

    # Exibir o estado inicial da fita
    tm.display()

    # Executar a Máquina de Turing
    result = tm.run()
    print(result)

    # Exibir o estado final da fita
    tape_final = ''.join(tm.tape).rstrip(tm.blank_symbol)
    print(f"Final Tape: {tape_final}")

if __name__ == "__main__":
    main()
