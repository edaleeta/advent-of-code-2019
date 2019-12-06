INPUT = 'input.txt'
TEST_INPUT = 'test_input.txt'


def create_path_coords(instructions, is_list=False):
    path = [] if is_list else set()
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

            if is_list:
                path.append((current_x, current_y))
            else:
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


def get_sum_steps_to_intersection(intersection, path_a, path_b):
    steps_a = path_a.index(intersection) + 1
    steps_b = path_b.index(intersection) + 1
    return steps_a + steps_b


def find_solution():
    wire_a_input, wire_b_input = parse_input_text(INPUT)

    path_a_coords = create_path_coords(wire_a_input)
    path_b_coords = create_path_coords(wire_b_input)

    intersections = get_intersections(path_a_coords, path_b_coords)
    print("Intersections:", intersections)

    min_distance = min([get_euclidean_distance_from_origin(intersection) for intersection in intersections])
    print("Min distance is: ", min_distance)

    print("Part 2:")

    path_a_ordered = create_path_coords(wire_a_input, is_list=True)
    path_b_ordered = create_path_coords(wire_b_input, is_list=True)

    min_steps = min([get_sum_steps_to_intersection(intersection, path_a_ordered, path_b_ordered) for intersection in intersections])
    print("Min steps: ", min_steps)


find_solution()





