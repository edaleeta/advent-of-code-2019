# It is a six-digit number.
# The value is within the range given in your puzzle input.
# Two adjacent digits are the same (like 22 in 122345).
# Going from left to right, the digits never decrease;
# they only ever increase or stay the same (like 111123 or 135679).

PUZZLE_INPUT = '147981-691423'


def parse_input(input_text):
    input_values = input_text.split('-')
    input_values = [int(value) for value in input_values]
    if len(input_values) != 2:
        raise Exception("Invalid input {} received.".format(input_text))
    return input_values


def is_valid_password(password, is_part_two=False):
    digits = [digit for digit in password]
    adjacent_dupe_char = None
    adjacent_group = []
    adjacent_groups = []
    ptr = 0

    while ptr < (len(digits)-1):
        a, b = digits[ptr:ptr+2]

        if not b >= a:
            return False

        if a == b:
            if adjacent_dupe_char != a:
                if len(adjacent_group) > 0:
                    adjacent_groups.append(adjacent_group)
                adjacent_dupe_char = a
                adjacent_group = [a, b]
            else:
                adjacent_group.append(a)
        else:
            if len(adjacent_group) > 0:
                adjacent_groups.append(adjacent_group)
                adjacent_group = []

        ptr += 1

    if len(adjacent_group) > 0:
        adjacent_groups.append(adjacent_group)

    if is_part_two:
        return any([len(group) == 2 for group in adjacent_groups])

    return bool(adjacent_dupe_char)


def get_solution():
    min_value, max_value = parse_input(PUZZLE_INPUT)
    valid_password_count = 0
    for i in range(min_value, max_value+1):
        if is_valid_password(str(i)):
            valid_password_count += 1
    print("Part 1: Number of valid passwords in range: ", valid_password_count)

    valid_password_count = 0
    for i in range(min_value, max_value+1):
        if is_valid_password(str(i), is_part_two=True):
            valid_password_count += 1
    print("Part 2: Number of valid passwords in range: ", valid_password_count)


get_solution()
