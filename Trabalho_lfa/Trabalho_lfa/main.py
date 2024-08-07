import sys
import json

def ler_dados(arquivo):
    with open(arquivo, "r") as file:
        data = json.load(file)
    
    estados = data["estados"]
    alfabeto_entrada = data["alfabetoEntrada"]
    alfabeto_fita = data["alfabetoFita"]
    transicoes = data["transicoes"]
    estadoInicial = data["estadoInicial"]
    estadoFinal = data["estadoFinal"]
    
    return estados, alfabeto_entrada, alfabeto_fita, transicoes, estadoInicial, estadoFinal

def encode_symbol(symbol):
    encoding_scheme = {'0': '1', '1': '11', 'B': '111', 'D': '11', 'E': '1'}
    if symbol.startswith('q'):
        state_number = int(symbol[1:])
        return '1' * (state_number + 1)
    else:
        return encoding_scheme.get(symbol, symbol)

def convert_input_to_notation(input_str):
    return ''.join(['1' if char == '0' else '11' for char in input_str])

def print_turing_machine(mt):
    print("Turing Machine Configuration:")
    print("States:", mt['estados'])
    print("Input Alphabet:", mt['alfabetoEntrada'])
    print("Tape Alphabet:", mt['alfabetoFita'])
    print("Transitions:")
    for transition in mt['transicoes']:
        print(" ", transition)
    print("Initial State:", mt['estadoInicial'])
    print("Final States:", mt['estadoFinal'])

def main(configTM, chain, output):
    estados, alfabeto_entrada, alfabeto_fita, transicoes, estadoInicial, estadoFinal = ler_dados(configTM)

    encoded_states = [encode_symbol(state) for state in estados]
    encoded_input_alphabet = [encode_symbol(symbol) for symbol in alfabeto_entrada]
    encoded_tape_alphabet = [encode_symbol(symbol) for symbol in alfabeto_fita]
    encoded_transitions = [[encode_symbol(part) for part in transition] for transition in transicoes]
    encoded_initial_state = encode_symbol(estadoInicial)
    encoded_final_states = [encode_symbol(state) for state in estadoFinal]

    mt = {
        'estados': encoded_states,
        'alfabetoEntrada': encoded_input_alphabet,
        'alfabetoFita': encoded_tape_alphabet,
        'transicoes': encoded_transitions,
        'estadoInicial': encoded_initial_state,
        'estadoFinal': encoded_final_states
    }

    print_turing_machine(mt)

if __name__ == "__main__":
    if len(sys.argv) == 3:
        main(sys.argv[1], '', sys.argv[2])
    elif len(sys.argv) == 4:
        main(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        print("Uso: python3 main.py <ArquivoConfigMT> [<Cadeia>] [<ArquivoSaida>]")
        sys.exit(1)
