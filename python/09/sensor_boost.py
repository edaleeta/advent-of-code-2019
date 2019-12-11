import importlib
intcode = importlib.import_module('python.05.intcode_again', 'IntcodeMachineDayFive')
IntcodeMachine = getattr(intcode, 'IntcodeMachineDayFive')

TEST_INPUT = 'test_input.txt'
INPUT = 'input.txt'


class IntcodeMachineDayNine(IntcodeMachine):
    def __init__(self, text, input_value):
        super().__init__(text, input_value)
        self.relative_base = 0

    def allocate_additional_memory(self, i):
        # Allocates additional memory through index `i`
        memory_diff = i - (len(self.opcodes) - 1)
        new_memory = [0] * memory_diff
        self.opcodes = self.opcodes + new_memory

    def get_value_at_loc(self, loc):
        # If accessing unallocated memory, allocate it
        if loc > (len(self.opcodes) - 1):
            self.allocate_additional_memory(loc)
        return self.opcodes[loc]

    def overwrite_value_at_loc(self, value, loc):
        mode = self.get_mode()
        final_loc = (loc + self.relative_base) if mode == 2 else loc
        # If writing to unallocated memory, allocate it
        if final_loc > (len(self.opcodes) - 1):
            self.allocate_additional_memory(final_loc)
        self.opcodes[final_loc] = value

    def get_value_for_param(self, param, is_write=False):
        mode = self.get_mode()
        # Relative mode
        if mode == 2:
            if is_write:
                return param + self.relative_base
            return self.get_value_at_loc(param + self.relative_base)
        # Immediate mode
        elif mode == 1:
            return param
        # Position mode
        elif mode == 0:
            if is_write:
                return param
            return self.get_value_at_loc(param)
        else:
            raise Exception('Unknown mode {} found.'.format(mode))

    def adjust_relative_base(self):
        """ OPCODE: 9"""
        param_a = self.opcodes[self.cursor+1]
        self.relative_base += self.get_value_for_param(param_a)
        self.cursor += 2

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
        elif opcode == 9:
            return self.adjust_relative_base
        elif opcode == 99:
            return None
        else:
            raise Exception("Unrecognized opcode: ", self.curr_opcode)


def get_solution():
    with open(TEST_INPUT) as file:
        text = file.read().strip()
    m = IntcodeMachineDayNine(text, 1)
    m.run_program()
    print("Test output:", m.outputs)

    with open(INPUT) as file:
        text = file.read().strip()
    m = IntcodeMachineDayNine(text, 1)
    m.run_program()
    print("Part 1 solution:", m.outputs)


get_solution()
