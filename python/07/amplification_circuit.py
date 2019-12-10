import importlib
from itertools import permutations

intcode = importlib.import_module('python.05.intcode_again', 'IntcodeMachineDayFive')
IntcodeMachine = getattr(intcode, 'IntcodeMachineDayFive')
INPUT = 'input.txt'
TEST_INPUT = 'test_input.txt'
TEST_SEQUENCE = (1, 0, 4, 3, 2)


class IntcodeMachineDaySeven(IntcodeMachine):
    def __init__(self, program, input_values):
        # This is derp since self.input_value is now throwaway; just didn't want to edit old solutions
        super().__init__(program, input_values[0])
        # Input values are popped; first input at end
        self.input_values = input_values
        self.outputs = []
        self.curr_opcode = None
        self.curr_param_modes = None

    def save_input_value_to_position(self):
        """ OPCODE: 3 """
        self.overwrite_value_at_loc(self.input_values.pop(), self.opcodes[self.cursor + 1])
        self.cursor += 2


class Amplifier:
    def __init__(self, phase_setting, input_value=None):
        if phase_setting is None:
            raise Exception('Phase setting missing. Amplifier must be initialized with phase setting.')
        self.phase_setting = phase_setting
        self.input_value = input_value
        self.output_value = None
        self.intcode_machine = None

    def initialize_intcode_machine(self, program):
        # Input values are popped; first input at end
        self.intcode_machine = IntcodeMachineDaySeven(program, [self.input_value, self.phase_setting])

    def run_intcode_machine(self):
        if self.intcode_machine is None:
            raise Exception('No intcode machine found. Did you forget to initialize it?')
        self.intcode_machine.run_program()
        self.output_value = self.intcode_machine.outputs[-1]


class AmplifierCircuit:
    def __init__(self, phase_code_sequence):
        self.circuit = [Amplifier(phase_code) for phase_code in phase_code_sequence]
        self.output_value = None

    def run_circuit(self, program):
        i = 0
        input_value = 0
        while i < len(self.circuit):
            current_amp = self.circuit[i]
            current_amp.input_value = input_value
            current_amp.initialize_intcode_machine(program)
            current_amp.run_intcode_machine()
            input_value = current_amp.output_value
            i += 1

        self.output_value = input_value


def create_phase_code_sequence_from_text(sequence):
    return [int(char) for char in sequence]


def get_part_one_solution():
    max_thruster_signal = 0
    with open(INPUT) as file:
        program = file.read().strip()

    base_sequence = create_phase_code_sequence_from_text(TEST_SEQUENCE)
    phase_code_sequences = permutations(base_sequence)
    for phase_code in phase_code_sequences:
        amp_circut = AmplifierCircuit(phase_code)
        amp_circut.run_circuit(program)
        if amp_circut.output_value > max_thruster_signal:
            max_thruster_signal = amp_circut.output_value

    print('Max thruster signal:', max_thruster_signal)


get_part_one_solution()
