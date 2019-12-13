import importlib
from enum import Enum
from enum import IntEnum
intcode = importlib.import_module('python.09.sensor_boost', 'IntcodeMachineDayNine')
IntcodeMachine = getattr(intcode, 'IntcodeMachineDayNine')

INPUT = 'input.txt'


class MachineSignal(Enum):
    OUTPUT_READY = 'OUTPUT_READY'
    HALTED = 'HALTED'


class IntcodeMachineDayEleven(IntcodeMachine):
    def __init__(self, text, get_input_value):
        self.get_input_value = get_input_value
        super().__init__(text, input_value=None)

    def get_input_value(self):
        return self.input_channel.pop()

    # Override behavior to run a func for input
    def save_input_value_to_position(self):
        """ OPCODE: 3 """
        self.overwrite_value_at_loc(self.get_input_value(), self.opcodes[self.cursor+1])
        self.cursor += 2

    def run_program_with_return_signals(self):
        while self.cursor < self.get_program_length():
            modes_and_opcode = str(self.get_value_at_loc(self.cursor))
            self.curr_opcode = int(modes_and_opcode[-2:])
            self.curr_param_modes = [int(mode) for mode in modes_and_opcode[:-2]]

            handler = self.get_handler_for_opcode(self.curr_opcode)
            if not handler:
                return MachineSignal.HALTED
            handler()

            # Post-op signals
            if self.curr_opcode == 4 and len(self.outputs) == 2:
                return MachineSignal.OUTPUT_READY


class Direction(IntEnum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


class TurnInstruction(IntEnum):
    TURN_LEFT = 0
    TURN_RIGHT = 1


class ColorInstruction(IntEnum):
    BLACK = 0
    WHITE = 1


class Color(IntEnum):
    BLACK = 0
    WHITE = 1


class PaintingRobot:
    def __init__(self, position=(0, 0), hull=None):
        self.faced_direction = Direction.UP
        self.position = position
        self.hull = {} if hull is None else hull
        self.brain = None

    def initialize_brain(self, program_text):
        m = IntcodeMachineDayEleven(program_text, get_input_value=self.get_camera_signal)
        self.brain = m

    def turn(self, instruction):
        num_directions = len(Direction)
        if instruction == TurnInstruction.TURN_LEFT:
            self.faced_direction = (self.faced_direction - 1) % num_directions
        elif instruction == TurnInstruction.TURN_RIGHT:
            self.faced_direction = (self.faced_direction + 1) % num_directions
        else:
            raise Exception('Turn instruction {} not recognized.'.format(instruction))

    def move_forward(self):
        x, y = self.position
        if self.faced_direction == Direction.UP:
            y += 1
        elif self.faced_direction == Direction.RIGHT:
            x += 1
        elif self.faced_direction == Direction.DOWN:
            y -= 1
        elif self.faced_direction == Direction.LEFT:
            x -= 1
        self.position = (x, y)

    def paint_panel(self, instruction):
        if instruction == ColorInstruction.BLACK:
            self.hull[self.position] = Color.BLACK
        elif instruction == ColorInstruction.WHITE:
            self.hull[self.position] = Color.WHITE
        else:
            raise Exception('Painting instruction {} not recognized.'.format(instruction))

    def get_camera_signal(self):
        current_panel_color = self.hull.get(self.position)
        signal = current_panel_color or Color.BLACK
        return signal

    def handle_brain_output(self):
        turn_instruction = TurnInstruction(self.brain.outputs.pop())
        color_instruction = ColorInstruction(self.brain.outputs.pop())

        self.paint_panel(color_instruction)
        self.turn(turn_instruction)
        self.move_forward()

    def start_painting(self):
        if self.brain is None:
            raise Exception("Can't start painting without a brain. Did you forget to boot me up?")
        signal = None
        while signal != MachineSignal.HALTED:
            signal = self.brain.run_program_with_return_signals()
            if signal == MachineSignal.OUTPUT_READY:
                self.handle_brain_output()


def get_solution():
    with open(INPUT) as file:
        text = file.read().strip()

    emergency_hull = {}
    paintbot = PaintingRobot(hull=emergency_hull)
    paintbot.initialize_brain(text)
    paintbot.start_painting()
    print("Part 1. Number of panels painted at least once: ", len(emergency_hull))


get_solution()
