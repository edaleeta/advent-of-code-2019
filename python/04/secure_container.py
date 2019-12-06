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


def is_valid_password(password):
    digits = [digit for digit in password]
    has_adjacent_dupe = False
    ptr = 0

    while ptr < (len(digits)-1):
        a, b = digits[ptr:ptr+2]
        if a == b and not has_adjacent_dupe:
            has_adjacent_dupe = True
        if not b >= a:
            return False
        ptr += 1

    return has_adjacent_dupe


def get_solution():
    min_value, max_value = parse_input(PUZZLE_INPUT)
    valid_password_count = 0
    valid_passwords = []
    for i in range(min_value, max_value+1):
        if is_valid_password(str(i)):
            valid_password_count += 1
            valid_passwords.append(i)
    print("Number of valid passwords in range: ", valid_password_count)


get_solution()
