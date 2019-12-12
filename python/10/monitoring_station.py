# Create path between origin and other
# If path already exists, don't count LOS
INPUT = 'input.txt'
TEST_INPUT = 'test_input.txt'
test_origin = (3, 4)
test_map = [
    (1, 0), (4, 0),
    (0, 2), (1, 2), (2, 2), (3, 2), (4, 2),
    (4, 3),
    (3, 4), (4, 4)
]

POSITIVE = '+'
NEGATIVE = '-'
ASTEROID = '#'

quadrant_to_values = {
    1: (POSITIVE, POSITIVE),
    2: (NEGATIVE, POSITIVE),
    3: (NEGATIVE, NEGATIVE),
    4: (POSITIVE, NEGATIVE)
}

values_to_quadrant = {
    (POSITIVE, POSITIVE): 1,
    (NEGATIVE, POSITIVE): 2,
    (NEGATIVE, NEGATIVE): 3,
    (POSITIVE, NEGATIVE): 4,
}


def get_delta(origin, target):
    # Returns dx, dy
    o_x, o_y = origin
    t_x, t_y = target
    return t_x - o_x, t_y - o_y


def get_slope(origin, target):
    dx, dy = get_delta(origin, target)
    if dx == 0:
        return None
    return dy / dx


def get_quadrant_of_target(origin, target):
    dx, dy = get_delta(origin, target)
    x_dir = NEGATIVE if dx < 0 else POSITIVE
    y_dir = NEGATIVE if dy < 0 else POSITIVE

    q = values_to_quadrant.get((x_dir, y_dir))
    if q is None:
        raise Exception('Quadrant not found.')
    return q


class Ray:
    """
        Represents a ray that intersects an origin and target.
        A ray is equivalent to another if its origin, slope, and quadrant are equal.
    """

    def __init__(self, origin, target):
        self.origin = origin
        self.slope = get_slope(origin, target)
        self.quadrant = get_quadrant_of_target(origin, target)

    def __repr__(self):
        return '<Ray origin: {}, slope: {}, quadrant: {}>'.format(self.origin, self.slope, self.quadrant)

    def __eq__(self, other):
        if not isinstance(other, Ray):
            return False
        return self.origin == other.origin and \
            self.slope == other.slope and \
            self.quadrant == other.quadrant

    def __hash__(self):
        return hash((self.origin, self.slope, self.quadrant))


def create_asteroid_map(filename):
    asteroid_map = []
    with open(filename) as the_map:
        for y, line in enumerate(the_map):
            for x, point in enumerate(line):
                if point == ASTEROID:
                    asteroid_map.append((x, y))
    return asteroid_map


def get_asteroids_detected(origin, a_map):
    rays = set()

    for asteroid in a_map:
        if asteroid == origin:
            continue
        rays.add(Ray(origin, asteroid))
    return len(rays)


def get_part_one_solution(filename):
    asteroid_map = create_asteroid_map(filename)
    max_asteroids_detected = 0

    for asteroid in asteroid_map:
        num_detected = get_asteroids_detected(asteroid, asteroid_map)
        if num_detected > max_asteroids_detected:
            max_asteroids_detected = num_detected

    print('Part 1, {}: Max asteroids detected: {}'.format(filename, max_asteroids_detected))


get_part_one_solution(TEST_INPUT)
get_part_one_solution(INPUT)
