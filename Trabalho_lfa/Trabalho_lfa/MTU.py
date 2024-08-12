import json
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import networkx as nx

class TuringMachine:
    def __init__(self, config_file: str) -> None:
        self.load_config(config_file)
        self.reset_tapes()

    def load_config(self, config_file: str) -> None:
        with open(config_file, 'r') as file:
            config = json.load(file)
            self.states = config["states"]
            self.alphabet = config["alphabet"]
            self.blank_symbol = config["blank_symbol"]
            self.initial_state = config["initial_state"]
            self.final_states = config["final_states"]
            self.transitions = config["transitions"]

    def reset_tapes(self) -> None:
        self.tape1 = self.encode_machine()
        self.tape2 = []
        self.tape3 = []
        self.head1 = 0
        self.head2 = 0
        self.head3 = 0
        self.current_state = self.initial_state

    def encode_machine(self) -> str:
        encoded_transitions = [self.encode_transition(trans) for trans in self.transitions]
        return '000' + '00'.join(encoded_transitions) + '000'

    def encode_transition(self, transition: str) -> str:
        state_from, symbol_read = transition.split(',')
        state_to, symbol_write, move = self.transitions[transition]
        return (
            f"{self.encode_state(state_from)}0"
            f"{self.encode_symbol(symbol_read)}0"
            f"{self.encode_state(state_to)}0"
            f"{self.encode_symbol(symbol_write)}0"
            f"{'1' if move == 'R' else '11'}"
        )

    def encode_state(self, state: str) -> str:
        return '1' * (self.states.index(state) + 1)

    def encode_symbol(self, symbol: str) -> str:
        return '1' * (self.alphabet.index(symbol) + 1)

    def execute(self, sequence: str) -> str:
        self.reset_tapes()
        self.tape3 = list(sequence) + [self.blank_symbol]
        while True:
            if not self.is_valid_input():
                return "Rejected"

            result = self.process_transition()
            if result == "Halt":
                return "Accepted" if self.current_state in self.final_states else "Rejected"

    def is_valid_input(self) -> bool:
        return all(symbol in self.alphabet for symbol in self.tape3)

    def process_transition(self) -> str:
        current_symbol = self.tape3[self.head3]
        current_state = self.current_state

        for transition, value in self.transitions.items():
            state, symbol = transition.split(',')
            if state == current_state and symbol == current_symbol:
                new_state, new_symbol, direction = value

                self.expand_tapes_if_needed()

                self.tape2.append(self.encode_state(new_state))
                self.tape3[self.head3] = new_symbol
                self.current_state = new_state

                self.move_head(direction)

                return "Continue"

        return "Halt"

    def expand_tapes_if_needed(self) -> None:
        if self.head3 >= len(self.tape3):
            self.tape3.append(self.blank_symbol)

    def move_head(self, direction: str) -> None:
        if direction == 'R':
            self.head3 += 1
        else:
            self.head3 -= 1

    def visualize_machine(self) -> None:
        graph = nx.DiGraph()

        for transition, (state_to, symbol_write, move) in self.transitions.items():
            state_from, symbol_read = transition.split(',')
            label = f"{symbol_read} -> {symbol_write}, {move}"
            if graph.has_edge(state_from, state_to):
                graph[state_from][state_to]['label'] += f"\n{label}"
            else:
                graph.add_edge(state_from, state_to, label=label)

        pos = nx.spring_layout(graph)
        fig, ax = plt.subplots(figsize=(8, 6))
        nx.draw(graph, pos, with_labels=True, node_size=2000, node_color='lightblue', font_size=10, font_weight='bold', arrows=True, ax=ax)
        edge_labels = nx.get_edge_attributes(graph, 'label')
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, ax=ax)
        plt.title("Turing Machine Visualization")
        plt.show()

    def visualize_tapes(self) -> None:
        fig, axs = plt.subplots(3, 1, figsize=(12, 6))
        tapes = [self.tape1, self.tape2, self.tape3]
        heads = [self.head1, self.head2, self.head3]
        titles = ['Tape 1', 'Tape 2', 'Tape 3']

        for i in range(3):
            tape_str = ''.join(tapes[i])
            axs[i].text(0.5, 0.5, tape_str, horizontalalignment='center', verticalalignment='center', fontsize=12)
            axs[i].set_xlim(0, 1)
            axs[i].set_ylim(0, 1)
            axs[i].set_title(titles[i])
            axs[i].axis('off')
            axs[i].plot(0.5, 0.55, marker="v", markersize=12, color="red")
            axs[i].set_xlim(-0.1, 1.1)

        plt.tight_layout()
        plt.show()

    def visualize_gui(self) -> None:
        root = tk.Tk()
        root.title("Universal Turing Machine Visualization")
        root.geometry("500x400")
        root.configure(bg='#f0f0f0')

        def execute_sequence() -> None:
            sequence = sequence_entry.get()
            if not sequence:
                messagebox.showwarning("Input Error", "Please enter a sequence.")
                return

            result = self.execute(sequence)
            result_label.config(text=f"Result: {result}")
            self.visualize_tapes()

        def show_machine() -> None:
            self.visualize_machine()

        frame = tk.Frame(root, bg='#f0f0f0')
        frame.pack(pady=20)

        sequence_label = tk.Label(frame, text="Enter sequence:", bg='#f0f0f0', font=("Arial", 12))
        sequence_label.grid(row=0, column=0, padx=5)

        sequence_entry = tk.Entry(frame, width=30, font=("Arial", 12))
        sequence_entry.grid(row=0, column=1, padx=5)

        execute_button = tk.Button(frame, text="Execute", command=execute_sequence, bg='#4CAF50', fg='white', font=("Arial", 12))
        execute_button.grid(row=0, column=2, padx=5)

        machine_button = tk.Button(frame, text="Show Machine", command=show_machine, bg='#2196F3', fg='white', font=("Arial", 12))
        machine_button.grid(row=1, columnspan=3, pady=10)

        result_label = tk.Label(frame, text="Result: ", bg='#f0f0f0', font=("Arial", 12))
        result_label.grid(row=2, columnspan=3, pady=10)

        root.mainloop()

if __name__ == "__main__":
    config_file = 'turing_machine_config2.json'
    UTM = TuringMachine(config_file)
    UTM.visualize_gui()
