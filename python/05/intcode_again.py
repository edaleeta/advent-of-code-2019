import importlib
from functools import reduce

intcode = importlib.import_module('python.02.intcode', 'IntcodeMachine')
IntcodeMachine = getattr(intcode, 'IntcodeMachine')
INPUT = 'input.txt'
TEST_INPUT = 'test_input.txt'


class IntcodeMachineDayFive(IntcodeMachine):
    def __init__(self, text, input_value):
        super().__init__(text)
        self.input_value = input_value
        self.outputs = []
        self.curr_opcode = None
        self.curr_param_modes = None

    def add(self):
        """ OPCODE: 1 """
        overwrite_loc = self.opcodes[self.cursor+3]
        nums_to_sum = []
        for i in range(1, 3):
            mode = 0
            param = self.opcodes[self.cursor+i]
            if len(self.curr_param_modes) > 0:
                mode = self.curr_param_modes.pop()

            if mode == 0:
                nums_to_sum.append(self.get_value_at_loc(param))
            elif mode == 1:
                nums_to_sum.append(param)

        self.overwrite_value_at_loc(sum(nums_to_sum), overwrite_loc)
        self.cursor += 4

    def multiply(self):
        """ OPCODE: 2 """
        overwrite_loc = self.opcodes[self.cursor+3]
        nums_to_mult = []

        for i in range(1, 3):
            mode = 0
            param = self.opcodes[self.cursor+i]
            if len(self.curr_param_modes) > 0:
                mode = self.curr_param_modes.pop()
            if mode == 0:
                nums_to_mult.append(self.get_value_at_loc(param))
            elif mode == 1:
                nums_to_mult.append(param)

        self.overwrite_value_at_loc(reduce(lambda x, y: x * y, nums_to_mult), overwrite_loc)
        self.cursor += 4

    def save_input_value_to_position(self):
        """ OPCODE: 3 """
        self.overwrite_value_at_loc(self.input_value, self.opcodes[self.cursor+1])
        self.cursor += 2

    def get_output_from_position(self):
        """ OPCODE: 4 """
        mode = 0
        if len(self.curr_param_modes) > 0:
            mode = self.curr_param_modes.pop()

        param = self.opcodes[self.cursor+1]
        output_value = None

        if mode == 0:
            output_value = self.get_value_at_loc(param)
        elif mode == 1:
            output_value = param

        self.outputs.append(output_value)
        self.cursor += 2

    def run_program(self):
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
            elif self.curr_opcode == 99:
                break
            else:
                raise Exception("Unrecognized opcode: ", self.curr_opcode)


def get_solution():
    with open(INPUT) as file:
        text = file.read().strip()
    m = IntcodeMachineDayFive(text, 1)
    m.run_program()
    print("Part 1 output: ", m.outputs)


get_solution()
