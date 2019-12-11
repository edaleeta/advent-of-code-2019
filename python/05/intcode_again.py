import importlib

intcode = importlib.import_module('python.02.intcode', 'IntcodeMachine')
IntcodeMachine = getattr(intcode, 'IntcodeMachine')
INPUT = 'input.txt'
TEST_INPUT = 'test_input.txt'
INPUT_TEST_PART_TWO = 'test_input_part_two.txt'


class IntcodeMachineDayFive(IntcodeMachine):
    def __init__(self, text, input_value):
        super().__init__(text)
        self.input_value = input_value
        self.outputs = []
        self.curr_opcode = None
        self.curr_param_modes = None

    def get_mode(self):
        if self.curr_param_modes:
            return self.curr_param_modes.pop()
        # Default to 0: position mode
        return 0

    def get_value_for_param(self, param):
        mode = self.get_mode()
        if mode == 1:
            return param
        elif mode == 0:
            return self.get_value_at_loc(param)
        else:
            raise Exception('Unknown mode {} found.'.format(mode))

    def add(self):
        """ OPCODE: 1 """
        param_a, param_b, overwrite_loc = self.opcodes[self.cursor+1:self.cursor+4]
        summed_params = self.get_value_for_param(param_a) + self.get_value_for_param(param_b)
        self.overwrite_value_at_loc(summed_params, overwrite_loc)
        self.cursor += 4

    def multiply(self):
        """ OPCODE: 2 """
        param_a, param_b, overwrite_loc = self.opcodes[self.cursor+1:self.cursor+4]
        summed_params = self.get_value_for_param(param_a) * self.get_value_for_param(param_b)
        self.overwrite_value_at_loc(summed_params, overwrite_loc)
        self.cursor += 4

    def save_input_value_to_position(self):
        """ OPCODE: 3 """
        self.overwrite_value_at_loc(self.input_value, self.opcodes[self.cursor+1])
        self.cursor += 2

    def get_output_from_position(self):
        """ OPCODE: 4 """

        param = self.opcodes[self.cursor+1]
        output_value = self.get_value_for_param(param)
        self.outputs.append(output_value)
        self.cursor += 2

    def jump_if_true(self):
        """ OPCODE: 5 """
        param_a, param_b = self.opcodes[self.cursor+1:self.cursor+3]
        test_value = self.get_value_for_param(param_a)

        if test_value != 0:
            overwrite_value = self.get_value_for_param(param_b)
            self.cursor = overwrite_value
        else:
            self.cursor += 3

    def jump_if_false(self):
        """ OPCODE: 6 """
        param_a, param_b = self.opcodes[self.cursor+1:self.cursor+3]
        test_value = self.get_value_for_param(param_a)

        if test_value == 0:
            overwrite_value = self.get_value_for_param(param_b)
            self.cursor = overwrite_value
        else:
            self.cursor += 3

    def less_than(self):
        """ OPCODE: 7 """
        param_a, param_b, overwrite_loc = self.opcodes[self.cursor+1:self.cursor+4]
        if self.get_value_for_param(param_a) < self.get_value_for_param(param_b):
            self.overwrite_value_at_loc(1, overwrite_loc)
        else:
            self.overwrite_value_at_loc(0, overwrite_loc)
        self.cursor += 4

    def equals(self):
        """ OPCODE: 8 """
        param_a, param_b, overwrite_loc = self.opcodes[self.cursor+1:self.cursor+4]
        if self.get_value_for_param(param_a) == self.get_value_for_param(param_b):
            self.overwrite_value_at_loc(1, overwrite_loc)
        else:
            self.overwrite_value_at_loc(0, overwrite_loc)
        self.cursor += 4

    def get_handler_for_opcode(self, opcode):
        if opcode == 1:
            return self.add
        elif opcode == 2:
            return self.multiply
        elif opcode == 3:
            return self.save_input_value_to_position
        elif opcode == 4:
            return self.get_output_from_position
        elif opcode == 5:
            return self.jump_if_true
        elif opcode == 6:
            return self.jump_if_false
        elif opcode == 7:
            return self.less_than
        elif opcode == 8:
            return self.equals
        elif opcode == 99:
            return None
        else:
            raise Exception("Unrecognized opcode: ", self.curr_opcode)

    def run_program(self):
        while self.cursor < self.get_program_length():
            modes_and_opcode = str(self.get_value_at_loc(self.cursor))
            self.curr_opcode = int(modes_and_opcode[-2:])
            self.curr_param_modes = [int(mode) for mode in modes_and_opcode[:-2]]

            handler = self.get_handler_for_opcode(self.curr_opcode)
            if not handler:
                break
            handler()


def get_solution():
    with open(INPUT) as file:
        text = file.read().strip()
    m = IntcodeMachineDayFive(text, 1)
    m.run_program()
    print("Part 1 output: ", m.outputs)

    with open(INPUT) as file:
        text = file.read().strip()
    m = IntcodeMachineDayFive(text, 5)
    m.run_program()
    print("Part 2 output: ", m.outputs)


if __name__ == '__main__':
    get_solution()
