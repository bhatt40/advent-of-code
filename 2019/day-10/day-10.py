from fractions import Fraction
from operator import itemgetter
from math import atan2, degrees

def get_asteroid_coordinates(map):
    asteroids = set()
    y = 0
    while y < len(map):
        x = 0
        row = map[y]
        while x < len(row):
            if row[x] == '#':
                asteroids.add((x, y))
            x += 1
        y += 1

    return asteroids


def get_asteroids_between_origin_and_other_asteroids(origin, asteroids):
    other_asteroids = asteroids.copy()
    other_asteroids.remove(origin)
    asteroids_between_lookup_dict = {}

    for asteroid in other_asteroids:
        points_in_between = get_points_between_two_points(origin, asteroid)
        asteroids_in_between = other_asteroids & points_in_between

        asteroids_between_lookup_dict.update({
            asteroid: asteroids_in_between
        })

    return asteroids_between_lookup_dict


def calculate_slope_between_two_points(p1, p2):
    (x1, y1) = p1
    (x2, y2) = p2

    if x1 == x2:
        slope = [0, 1]
    elif y1 == y2:
        slope = [1, 0]
    else:
        fractional_slope = Fraction(y2 - y1, x2 - x1)
        slope = [fractional_slope.denominator, fractional_slope.numerator]

    slope[0] = (-1 * abs(slope[0])) if x2 < x1 else abs(slope[0])
    slope[1] = (-1 * abs(slope[1])) if y2 < y1 else abs(slope[1])

    slope = tuple(slope)

    return slope


def get_points_between_two_points(p1, p2):
    (x1, y1) = p1
    (x2, y2) = p2
    slope = calculate_slope_between_two_points(p1, p2)

    x = x1
    y = y1
    points = set()

    while y != y2 or x != x2:
        y = y + slope[1]
        x = x + slope[0]
        points.add((x, y))

    points.remove(p2)

    return points


def count_detectable_asteroids(asteroids_between_lookup_dict):
    count = 0
    for other_asteroid, asteroids_between in asteroids_between_lookup_dict.items():
        if len(asteroids_between) == 0:
            count += 1

    return count


def group_asteroids_between_by_angle(origin, asteroids_between_lookup_dict):
    slopes_dict = {}
    for asteroid, asteroids_between in asteroids_between_lookup_dict.items():
        slope = calculate_slope_between_two_points(origin, asteroid)
        asteroid_item = (asteroid, len(asteroids_between))
        if slope in slopes_dict:
            slopes_dict[slope].append(asteroid_item)
        else:
            slopes_dict[slope] = [asteroid_item]

    # Sort each slope's items by number of asteroids between and convert slope to angle
    slopes_dict = {
        calculate_angle_of_slope(slope): sorted(items, key=itemgetter(1))
        for slope, items in slopes_dict.items()
    }

    return slopes_dict


def calculate_angle_of_slope(slope):
    (x, y) = slope

    # Angles are calculated as clockwise from 90 degrees since laser starts at 12 o'clock
    return (270 - degrees(atan2(y, x))) % 360


def vaporize_next_asteroid_in_list(vaporized_set, list_of_asteroids_at_angle):
    for asteroid_item in list_of_asteroids_at_angle:
        asteroid = asteroid_item[0]
        if asteroid not in vaporized_set:
            return asteroid

    return None


def vaporize_n_asteroids(start_angle, n, sorted_angles, grouped_asteroids):
    laser_index = sorted_angles.index(start_angle)
    vaporized_set = set()
    last_vaporized_android = None

    while len(vaporized_set) < n:
        angle = sorted_angles[laser_index]
        vaporized_asteroid = vaporize_next_asteroid_in_list(vaporized_set, grouped_asteroids[angle])
        if vaporized_asteroid:
            vaporized_set.add(vaporized_asteroid)
            last_vaporized_android = vaporized_asteroid
        else:
            print('Skipped {}'.format(angle))

        laser_index += 1
        laser_index = laser_index % len(sorted_angles)

    return last_vaporized_android


LASER_START_ANGLE = 0
NUMBER_OF_ASTEROIDS_TO_VAPORIZE = 200

with open('input.txt', 'r') as f:
    map = f.readlines()

asteroids = get_asteroid_coordinates(map)
all_asteroids_between_lookup_dict = {
    asteroid: get_asteroids_between_origin_and_other_asteroids(asteroid, asteroids)
    for asteroid in asteroids
}

# Part 1
detectable_asteroid_counts = {
    count_detectable_asteroids(all_asteroids_between_lookup_dict[asteroid]): asteroid
    for asteroid in asteroids
}

max_detectable_asteroids = max(detectable_asteroid_counts.keys())
print(max_detectable_asteroids)

# Part 2
station_location = detectable_asteroid_counts[max_detectable_asteroids]
station_asteroids_between_lookup_dict = all_asteroids_between_lookup_dict[station_location]

grouped_by_angles = group_asteroids_between_by_angle(station_location, station_asteroids_between_lookup_dict)
angles = list(grouped_by_angles.keys())
angles.sort(reverse=True)

print(vaporize_n_asteroids(LASER_START_ANGLE, NUMBER_OF_ASTEROIDS_TO_VAPORIZE, angles, grouped_by_angles))
