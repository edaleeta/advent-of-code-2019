TEST_INPUT = 'test_input.txt'
INPUT = 'input.txt'


class IntcodeProgram:
    def __init__(self, text):
        self.opcodes = self.parse_text_to_opcodes(text)

    @staticmethod
    def parse_text_to_opcodes(text):
        return [int(opcode) for opcode in text.split(',')]

    def prep_program(self):
        self.opcodes[1] = 12
        self.opcodes[2] = 2

    def run_program(self):
        cursor = 0

        while cursor < self.get_program_length():
            current_chunk_values = self.opcodes[cursor:cursor+Chunk.CHUNK_SIZE]

            current_chunk = Chunk(current_chunk_values, self)
            signal = current_chunk.get_signal()
            if signal.code == Signal.HALT_CODE:
                # Halt!
                print('Halt code received; shutting down program.')
                break
            elif signal.code in Signal.SUCCESS_CODES:
                self.overwrite_value_at_loc(signal.value, signal.overwrite_location)

            cursor += Chunk.CHUNK_SIZE

        print('Finished running program.')
        print('Opcode values are: ')
        print(self.opcodes)

    def overwrite_value_at_loc(self, value, location):
        self.opcodes[location] = value

    def get_value_at_location(self, loc):
        return self.opcodes[loc]

    def get_program_length(self):
        return len(self.opcodes or [])


class Chunk:
    CHUNK_SIZE = 4

    def __init__(self, chunk_values, program):
        self.chunk_values = chunk_values[:4]
        if len(self.chunk_values) != self.CHUNK_SIZE:
            Exception('Invalid chunk length.')
        self.program = program

    def get_signal(self):
        chunk = self.chunk_values
        signal_chunk, value, overwrite_loc = chunk[0], None, chunk[3]

        if signal_chunk == Signal.HALT_CODE:
            return Signal(signal_chunk)

        if signal_chunk in Signal.SUCCESS_CODES:
            input_a_location, input_b_location = chunk[1:3]
            x = self.program.get_value_at_location(input_a_location)
            y = self.program.get_value_at_location(input_b_location)
            rv = None

            if signal_chunk == Signal.ADD_CODE:
                rv = x + y
            elif signal_chunk == Signal.MULT_CODE:
                rv = x * y

            return Signal(signal_chunk, rv, overwrite_loc)

        raise Exception('Unexpected signal chunk {} received.'.format(signal_chunk))


class Signal:

    ADD_CODE = 1
    MULT_CODE = 2
    HALT_CODE = 99
    SUCCESS_CODES = [ADD_CODE, MULT_CODE]

    def __init__(self, code, value=None, overwrite_location=None):
        self.code = code
        self.value = value
        self.overwrite_location = overwrite_location


def get_solution():
    with open('input.txt') as file:
        text = file.read().strip()

    program = IntcodeProgram(text)
    program.prep_program()
    program.run_program()

    print('Value at position 0: ', program.get_value_at_location(0))


get_solution()
