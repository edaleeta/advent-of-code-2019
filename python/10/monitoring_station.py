from math import sqrt

# Create path between origin and other
# If path already exists, don't count LOS
INPUT = 'input.txt'
TEST_INPUT = 'test_input.txt'
TEST_INPUT_PART_TWO = 'test_input_part_two.txt'
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

QUAD_ONE = 'ONE'
QUAD_TWO = 'TWO'
QUAD_THREE = 'THREE'
QUAD_FOUR = 'FOUR'
UP = 'UP'
DOWN = 'DOWN'
RIGHT = 'RIGHT'
LEFT = 'LEFT'
CLOCKWISE_QUAD_ORDER = [UP, QUAD_ONE, RIGHT, QUAD_FOUR, DOWN, QUAD_THREE, LEFT, QUAD_TWO]

values_to_quadrant = {
    (POSITIVE, POSITIVE): QUAD_ONE,
    (NEGATIVE, POSITIVE): QUAD_TWO,
    (NEGATIVE, NEGATIVE): QUAD_THREE,
    (POSITIVE, NEGATIVE): QUAD_FOUR,
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
    # Multiply by -1 because original coordinates are not cartesian
    return -1 * dy / dx


def get_quadrant_of_target(origin, target):
    dx, dy = get_delta(origin, target)
    x_dir = NEGATIVE if dx < 0 else POSITIVE
    y_dir = POSITIVE if dy < 0 else NEGATIVE

    # Handle vertical ray
    if dx == 0:
        return UP if y_dir == POSITIVE else DOWN
    # Handle horizontal ray
    elif dy == 0:
        return RIGHT if x_dir == POSITIVE else LEFT

    # All other slopes
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
        self.asteroids_on_path = {self.get_distance_to_origin(target): target}

    def __repr__(self):
        return '<Ray origin: {}, slope: {}, ' \
            'quadrant: {}, asteroids_on_path: {}>'.format(self.origin, self.slope, self.quadrant, self.asteroids_on_path)

    def __eq__(self, other):
        if not isinstance(other, Ray):
            return False
        return self.origin == other.origin and \
            self.slope == other.slope and \
            self.quadrant == other.quadrant

    def __hash__(self):
        return hash((self.origin, self.slope, self.quadrant))

    def add_asteroid_to_path(self, asteroid):
        distance = self.get_distance_to_origin(asteroid)
        if self.asteroids_on_path.get(distance) is not None:
            raise Exception('Trying to add asteroid to path with existing distancce. That\'s not possible!')
        self.asteroids_on_path[distance] = asteroid

    def get_distance_to_origin(self, asteroid):
        dx, dy = get_delta(self.origin, asteroid)
        return sqrt(dx * dx + dy * dy)

    def get_asteroids_by_distance(self):
        """Sorts asteroids by largest to smallest distance."""
        sorted_distances = sorted(list(self.asteroids_on_path), reverse=True)
        return [self.asteroids_on_path.get(distance) for distance in sorted_distances]


def create_asteroid_map(filename):
    asteroid_map = []
    with open(filename) as the_map:
        for y, line in enumerate(the_map):
            for x, point in enumerate(line):
                if point == ASTEROID:
                    asteroid_map.append((x, y))
    return asteroid_map


def get_asteroids_detected(origin, a_map):
    rays = {}

    for asteroid in a_map:
        if asteroid == origin:
            continue
        ray = Ray(origin, asteroid)
        if rays.get((ray.slope, ray.quadrant)) is not None:
            rays[(ray.slope, ray.quadrant)].add_asteroid_to_path(asteroid)
        else:
            rays[(ray.slope, ray.quadrant)] = ray
    return rays


def get_part_one_solution(filename):
    asteroid_map = create_asteroid_map(filename)
    max_asteroids_detected, max_detection_asteroid = 0, None

    for asteroid in asteroid_map:
        num_detected = len(get_asteroids_detected(asteroid, asteroid_map))
        if num_detected > max_asteroids_detected:
            max_asteroids_detected, max_detection_asteroid = num_detected, asteroid

    print('Part 1, {}: Max asteroids detected: {}'.format(filename, max_asteroids_detected))
    print('Detected from asteroid: {}\n'.format(max_detection_asteroid))
    return max_detection_asteroid


def prepare_rays_for_asteroid_destruction(rays):
    """Sorts rays in clockwise order for laser pewpews."""

    def sort_keys_by_quad_clockwise(keys):
        chunked_keys_by_quad = {}
        for key in keys:
            _, quad = key
            chunked_keys = chunked_keys_by_quad.get(quad, [])
            chunked_keys.append(key)
            chunked_keys_by_quad[quad] = chunked_keys
        rv = []
        for quad in CLOCKWISE_QUAD_ORDER:
            rv += chunked_keys_by_quad.get(quad)
        return rv

    def sort_keys_by_slopes():
        return sorted(rays, key=lambda key: float("inf") if (key[0] is None) else key[0], reverse=True)

    keys_sorted_by_slopes = sort_keys_by_slopes()
    sorted_keys = sort_keys_by_quad_clockwise(keys_sorted_by_slopes)
    return sorted_keys, {key: rays.get(key).get_asteroids_by_distance() for key in sorted_keys}


def destroy_asteroids(sorted_ids, ray_id_to_asteroids, limit):
    num_destroyed = 0
    i = 0
    last_destroyed = None
    while num_destroyed < limit:
        ray_id = sorted_ids[i % len(sorted_ids)]
        curr_asteroids = ray_id_to_asteroids.get(ray_id)
        if len(curr_asteroids) > 0:
            last_destroyed = curr_asteroids.pop()
            num_destroyed += 1
            ray_id_to_asteroids[ray_id] = curr_asteroids
        i += 1
    return last_destroyed


def get_part_two_solution(filename):
    asteroid_map = create_asteroid_map(filename)
    max_detection_asteroid = get_part_one_solution(filename)

    asteroids_detected = get_asteroids_detected(max_detection_asteroid, asteroid_map)
    sorted_ray_ids, ray_data = prepare_rays_for_asteroid_destruction(asteroids_detected)

    num_asteroids_to_destroy = 200
    last_destroyed = destroy_asteroids(sorted_ray_ids, ray_data, num_asteroids_to_destroy)
    print('#{} asteroid destroyed: {}'.format(num_asteroids_to_destroy, last_destroyed))
    x, y = last_destroyed
    print('Part 2 solution: ', x * 100 + y)


# get_part_one_solution(TEST_INPUT)
# get_part_one_solution(INPUT)
get_part_two_solution(TEST_INPUT_PART_TWO)
get_part_two_solution(INPUT)
