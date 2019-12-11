INPUT = 'input.txt'
TEST_INPUT = 'test_input.txt'


def chunk_list(chunked_list, length):
    for i in range(0, len(chunked_list), length):
        yield chunked_list[i:i+length]


class SpaceImage:
    def __init__(self, image_data, height, width):
        self.image_data = [int(px) for px in image_data]
        self.height = height
        self.width = width
        self.layers = self.create_image_layers(self.image_data, height, width)

    @staticmethod
    def create_image_layers(image_data, height, width):
        num_px_in_layer = height * width
        return list(chunk_list(image_data, num_px_in_layer))

    @staticmethod
    def get_digit_count_of_layer(layer, target_digit):
        count = 0
        for digit in layer:
            if target_digit == digit:
                count += 1
        return count

    def get_digit_counts_for_layers(self, target_digit):
        return [self.get_digit_count_of_layer(layer, target_digit) for layer in self.layers]


def get_index_of_min_value(lst):
    min_i, min_value = None, None

    for i, value in enumerate(lst):
        if min_value is None or value < min_value:
            min_i, min_value = i, value
    return min_i


def get_solution():
    with open(INPUT) as file:
        image_data = file.read().strip()
    img = SpaceImage(image_data, 6, 25)
    digit_counts = img.get_digit_counts_for_layers(0)
    min_index = get_index_of_min_value(digit_counts)
    layer_to_scan = img.layers[min_index]
    num_ones = img.get_digit_count_of_layer(layer_to_scan, 1)
    num_twos = img.get_digit_count_of_layer(layer_to_scan, 2)
    solution = num_ones * num_twos

    print('Part 1 solution:', solution)


get_solution()
