import re
from math import sin, cos, radians


def calculate_manhattan_distance(coordinate_a, coordinate_b):
    return abs(coordinate_a[0] - coordinate_b[0]) + abs(coordinate_a[1] - coordinate_b[1])


def parse_instruction_string(string):
    m = re.match(r'^(?P<action>[A-Z])(?P<distance>[0-9]+)', string)
    return m.group('action'), int(m.group('distance'))


def execute_instruction(location, direction, action, distance):
    if action == 'L':
        direction = (direction + distance) % 360
    elif action == 'R':
        direction = (direction - distance) % 360
    elif action == 'F':
        location[0] += int(distance * cos(radians(direction)))
        location[1] += int(distance * sin(radians(direction)))
    elif action == 'N':
        location[1] += distance
    elif action == 'S':
        location[1] -= distance
    elif action == 'E':
        location[0] += distance
    elif action == 'W':
        location[0] -= distance
    else:
        raise Exception('Unexpected action: {}'.format(action))

    return location, direction


STARTING_LOCATION = [0, 0]
STARTING_DIRECTION = 0

with open('input.txt', 'r') as f:
    instructions = f.readlines()

location = STARTING_LOCATION.copy()
direction = STARTING_DIRECTION

for instruction_string in instructions:
    action, distance = parse_instruction_string(instruction_string)
    location, direction = execute_instruction(location, direction, action, distance)

print(calculate_manhattan_distance(location, STARTING_LOCATION))
