TEST_INPUT = 'test_input.txt'
INPUT = 'input.txt'

WANTED_OUTPUT = 19690720


class IntcodeMachine:
    def __init__(self, text):
        self.opcodes = self.parse_text_to_opcodes(text)
        self.opcodes_orig = self.opcodes[:]
        self.cursor = 0

    @staticmethod
    def parse_text_to_opcodes(text):
        return [int(opcode) for opcode in text.split(',')]

    def prep_program(self, noun=12, verb=2):
        self.opcodes[1] = noun
        self.opcodes[2] = verb

    def reset_program(self):
        self.opcodes = self.opcodes_orig[:]
        self.cursor = 0

    def add(self):
        input_loc_a, input_loc_b, overwrite_loc = self.opcodes[self.cursor+1:self.cursor+4]
        overwrite_value = self.get_value_at_loc(input_loc_a) + self.get_value_at_loc(input_loc_b)
        self.overwrite_value_at_loc(overwrite_value, overwrite_loc)
        self.cursor += 4

    def multiply(self):
        input_loc_a, input_loc_b, overwrite_loc = self.opcodes[self.cursor+1:self.cursor+4]
        overwrite_value = self.get_value_at_loc(input_loc_a) * self.get_value_at_loc(input_loc_b)
        self.overwrite_value_at_loc(overwrite_value, overwrite_loc)
        self.cursor += 4

    def run_program(self):
        while self.cursor < self.get_program_length():
            opcode = self.get_value_at_loc(self.cursor)

            if opcode == 1:
                self.add()
            elif opcode == 2:
                self.multiply()
            elif opcode == 99:
                break
            else:
                raise Exception("Unrecognized opcode: ", opcode)

    def overwrite_value_at_loc(self, value, location):
        self.opcodes[location] = value

    def get_value_at_loc(self, loc):
        return self.opcodes[loc]

    def get_program_length(self):
        return len(self.opcodes or [])


def get_solutions():
    with open('input.txt') as file:
        text = file.read().strip()

    program = IntcodeMachine(text)
    program.prep_program()
    program.run_program()

    print('Part 1. Value at position 0: ', program.get_value_at_loc(0))

    solution_noun, solution_verb = None, None
    for noun in range(0, 100):
        for verb in range(0, 100):
            program.reset_program()
            program.prep_program(noun, verb)
            try:
                program.run_program()
                if program.get_value_at_loc(0) == WANTED_OUTPUT:
                    solution_noun, solution_verb = noun, verb
                    break
            except Exception as e:
                print(e)
                print("Program failed with test inputs noun: {}, verb: {}".format(noun, verb))
                continue
        if solution_noun is not None and solution_verb is not None:
            break

    print('Output {} found using noun: {} and verb: {}'.format(WANTED_OUTPUT, solution_noun, solution_verb))
    print('Part 2 answer: ', 100 * solution_noun + solution_verb)


if __name__ == '__main__':
    get_solutions()

