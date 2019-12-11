import importlib
from itertools import permutations

intcode = importlib.import_module('python.05.intcode_again', 'IntcodeMachineDayFive')
IntcodeMachine = getattr(intcode, 'IntcodeMachineDayFive')
INPUT = 'input.txt'
TEST_INPUT = 'test_input.txt'
TEST_INPUT_PART_TWO = 'test_input_part_two.txt'
TEST_SEQUENCE = (1, 0, 4, 3, 2)
TEST_SEQUENCE_PART_TWO = (9,7,8,5,6)


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

    def run_program_with_return_signals(self):
        while self.cursor < self.get_program_length():
            modes_and_opcode = str(self.get_value_at_loc(self.cursor))
            self.curr_opcode = int(modes_and_opcode[-2:])
            self.curr_param_modes = [int(mode) for mode in modes_and_opcode[:-2]]

            if self.curr_opcode == 1:
                self.add()
            elif self.curr_opcode == 2:
                self.multiply()
            elif self.curr_opcode == 3:
                self.save_input_value_to_position()
            elif self.curr_opcode == 4:
                self.get_output_from_position()
                return 'OUTPUT'
            elif self.curr_opcode == 5:
                self.jump_if_true()
            elif self.curr_opcode == 6:
                self.jump_if_false()
            elif self.curr_opcode == 7:
                self.less_than()
            elif self.curr_opcode == 8:
                self.equals()
            elif self.curr_opcode == 99:
                return 'HALT'
            else:
                raise Exception("Unrecognized opcode: ", self.curr_opcode)


class Amplifier:
    def __init__(self, phase_setting, input_value=None):
        if phase_setting is None:
            raise Exception('Phase setting missing. Amplifier must be initialized with phase setting.')
        self.phase_setting = phase_setting
        self.input_value = input_value
        self.output_value = None
        self.intcode_machine = None
        self.status = 'NOT_STARTED'

    def initialize_intcode_machine(self, program):
        if self.intcode_machine is not None:
            self.intcode_machine.input_values = [self.input_value]
            return
        # Input values are popped; first input at end
        self.intcode_machine = IntcodeMachineDaySeven(program, [self.input_value, self.phase_setting])

    def run_intcode_machine(self):
        if self.intcode_machine is None:
            raise Exception('No intcode machine found. Did you forget to initialize it?')
        self.intcode_machine.run_program()
        self.output_value = self.intcode_machine.outputs[-1]

    def run_intcode_machine_with_return_signals(self):
        if self.intcode_machine is None:
            raise Exception('No intcode machine found. Did you forget to initialize it?')
        signal = self.intcode_machine.run_program_with_return_signals()
        if signal == 'OUTPUT':
            self.output_value = self.intcode_machine.outputs[-1]
        if signal == 'HALT':
            self.status = 'HALTED'
        else:
            self.status = 'PAUSED'


class AmplifierCircuit:
    def __init__(self, phase_code_sequence):
        self.circuit = [Amplifier(phase_code) for phase_code in phase_code_sequence]
        self.output_value = None

    def get_amp_statuses(self):
        return [amp.status for amp in self.circuit]

    def is_done_running(self):
        return all([status == 'HALTED' for status in self.get_amp_statuses()])

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

    def run_feedback_loop(self, program):
        i = 0
        input_value = 0
        while not self.is_done_running():
            current_amp = self.circuit[i]
            current_amp.input_value = input_value
            current_amp.initialize_intcode_machine(program)
            current_amp.run_intcode_machine_with_return_signals()
            input_value = current_amp.output_value
            i = (i + 1) % len(self.circuit)

        self.output_value = self.circuit[-1].output_value


def create_phase_code_sequence_from_text(sequence):
    return [int(char) for char in sequence]


def get_part_one_solution():
    max_thruster_signal = 0
    with open(INPUT) as file:
        program = file.read().strip()

    base_sequence = create_phase_code_sequence_from_text('01234')
    phase_code_sequences = permutations(base_sequence)
    for phase_code in phase_code_sequences:
        amp_circuit = AmplifierCircuit(phase_code)
        amp_circuit.run_circuit(program)
        if amp_circuit.output_value > max_thruster_signal:
            max_thruster_signal = amp_circuit.output_value

    print('Part 1: Max thruster signal:', max_thruster_signal)


def get_part_two_solution():
    max_thruster_signal = 0
    with open(INPUT) as file:
        program = file.read().strip()

    base_sequence = create_phase_code_sequence_from_text('56789')
    phase_code_sequences = permutations(base_sequence)
    for phase_code in phase_code_sequences:
        amp_circuit = AmplifierCircuit(phase_code)
        amp_circuit.run_feedback_loop(program)
        if amp_circuit.output_value > max_thruster_signal:
            max_thruster_signal = amp_circuit.output_value

    print('Part 2: Max thruster signal:', max_thruster_signal)


get_part_one_solution()
get_part_two_solution()
