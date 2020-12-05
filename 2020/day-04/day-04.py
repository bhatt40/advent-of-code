import functools
import re


def add_line_to_passport(passport, line):
    passport.update({
        pair.split(':')[0]: pair.split(':')[1]
        for pair in line.split(' ')
    })


def has_required_fields(passport):
    return all(map(lambda x: x in passport, REQUIRED_FIELDS))


def is_valid_passport(passport, validate_data):
    if not validate_data:
        return has_required_fields(passport)

    return has_required_fields(passport) and \
        functools.reduce(lambda is_valid, key: is_valid and is_valid_value(key, passport[key]), passport, True)


def is_valid_value(key, value):
    value = value.split('\n')[0]
    if key == 'byr':
        return 1920 <= int(value) <= 2002
    elif key == 'iyr':
        return 2010 <= int(value) <= 2020
    elif key == 'eyr':
        return 2020 <= int(value) <= 2030
    elif key == 'hgt':
        try:
            number = int(value[0: -2])
        except ValueError:
            return False
        unit = value[-2:]
        if unit == 'cm':
            return 150 <= number <= 193
        elif unit == 'in':
            return 59 <= number <= 76
        else:
            return False
    elif key == 'hcl':
        return re.search(r'^#[0-9a-f]{6}$', value)
    elif key == 'ecl':
        return re.search(r'^amb|blu|brn|gry|grn|hzl|oth$', value)
    elif key == 'pid':
        return re.search('^0*[0-9]{9}$', value)

    return True


def get_valid_password_count(passports, validate_data=False):
    index = 0
    current_passport = {}
    valid_password_count = 0
    while index < len(passports):
        next_passport_line = passports[index]
        if next_passport_line == '\n':
            if is_valid_passport(current_passport, validate_data):
                valid_password_count += 1
            current_passport = {}
        else:
            add_line_to_passport(current_passport, next_passport_line)

        index += 1

    # Check last passport
    if is_valid_passport(current_passport, validate_data):
        valid_password_count += 1

    return valid_password_count


REQUIRED_FIELDS = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']


with open('input.txt', 'r') as f:
    passport_lines = f.readlines()

# Part 1
print(get_valid_password_count(passport_lines, validate_data=False))

# Part 2
print(get_valid_password_count(passport_lines, validate_data=True))
