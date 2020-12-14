import re
from math import sin, cos, radians


def calculate_manhattan_distance(coordinate_a, coordinate_b):
    return abs(coordinate_a[0] - coordinate_b[0]) + abs(coordinate_a[1] - coordinate_b[1])


def parse_instruction_string(string):
    m = re.match(r'^(?P<action>[A-Z])(?P<distance>[0-9]+)', string)
    return m.group('action'), int(m.group('distance'))


def rotate_waypoint(waypoint_location, location, direction):
    if direction == 'L':
        dy = waypoint_location[1] - location[1]
        dx = waypoint_location[0] - location[0]
        a = dy
        dy = dx
        dx = -1 * a
        waypoint_location[0] = location[0] + dx
        waypoint_location[1] = location[1] + dy
    else:
        dy = waypoint_location[1] - location[1]
        dx = waypoint_location[0] - location[0]
        a = dx
        dx = dy
        dy = -1 * a
        waypoint_location[0] = location[0] + dx
        waypoint_location[1] = location[1] + dy

    return waypoint_location


def execute_instruction(location, direction, action, distance, waypoint_location=None):
    if action == 'L':
        if waypoint_location:
            for _ in range(distance // 90):
                waypoint_location = rotate_waypoint(waypoint_location, location, action)
        else:
            direction = (direction + distance) % 360
    elif action == 'R':
        if waypoint_location:
            for _ in range(distance // 90):
                waypoint_location = rotate_waypoint(waypoint_location, location, action)
        else:
            direction = (direction - distance) % 360
    elif action == 'F':
        if waypoint_location:
            dx = (waypoint_location[0] - location[0]) * distance
            dy = (waypoint_location[1] - location[1]) * distance
            location[0] += dx
            location[1] += dy
            waypoint_location[0] += dx
            waypoint_location[1] += dy
        else:
            location[0] += int(distance * cos(radians(direction)))
            location[1] += int(distance * sin(radians(direction)))
    elif action == 'N':
        if waypoint_location:
            waypoint_location[1] += distance
        else:
            location[1] += distance
    elif action == 'S':
        if waypoint_location:
            waypoint_location[1] -= distance
        else:
            location[1] -= distance
    elif action == 'E':
        if waypoint_location:
            waypoint_location[0] += distance
        else:
            location[0] += distance
    elif action == 'W':
        if waypoint_location:
            waypoint_location[0] -= distance
        else:
            location[0] -= distance
    else:
        raise Exception('Unexpected action: {}'.format(action))

    return location, direction, waypoint_location


STARTING_LOCATION = [0, 0]
STARTING_WAYPOINT_LOCATION = [10, 1]
STARTING_DIRECTION = 0

with open('input.txt', 'r') as f:
    instructions = f.readlines()

# Part 1
location = STARTING_LOCATION.copy()
direction = STARTING_DIRECTION

for instruction_string in instructions:
    action, distance = parse_instruction_string(instruction_string)
    location, direction, waypoint_location = \
        execute_instruction(location, direction, action, distance, waypoint_location=None)

print(calculate_manhattan_distance(location, STARTING_LOCATION))

# Part 2
location = STARTING_LOCATION.copy()
direction = STARTING_DIRECTION
waypoint_location = STARTING_WAYPOINT_LOCATION.copy()

for instruction_string in instructions:
    action, distance = parse_instruction_string(instruction_string)
    location, direction, waypoint_location = \
        execute_instruction(location, direction, action, distance, waypoint_location=waypoint_location)

print(calculate_manhattan_distance(location, STARTING_LOCATION))
