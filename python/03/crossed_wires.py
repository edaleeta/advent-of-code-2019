INPUT = 'input.txt'


def create_path(instructions):
    path = set()
    current_x = 0
    current_y = 0

    for instruction in instructions:
        direction, *distance = instruction
        distance = int(''.join(distance))

        for i in range(distance):
            if direction == 'R':
                current_x += 1
            elif direction == 'L':
                current_x -= 1
            elif direction == 'U':
                current_y += 1
            elif direction == 'D':
                current_y -= 1
            else:
                raise Exception("Invalid direction {} found.".format(direction))
            path.add((current_x, current_y))

    return path


def get_intersections(path_a, path_b):
    intersections = []

    for coord in path_b:
        if coord in path_a:
            intersections.append(coord)
    return intersections


def get_euclidean_distance_from_origin(coord):
    x, y = coord
    return abs(x) + abs(y)


def parse_input_text(filename):
    with open(filename) as file:
        text = file.read().split('\n')

    return [path.split(',') for path in text]


def find_solution():
    wire_a_input, wire_b_input = parse_input_text(INPUT)

    path_a = create_path(wire_a_input)
    path_b = create_path(wire_b_input)

    intersections = get_intersections(path_a, path_b)
    print("Intersections:", intersections)

    min_distance = min([get_euclidean_distance_from_origin(intersection) for intersection in intersections])
    print("Min distance is: ", min_distance)


find_solution()





