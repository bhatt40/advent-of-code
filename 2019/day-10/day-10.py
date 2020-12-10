from fractions import Fraction


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


def get_points_between_two_points(p1, p2):
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

# Part
station_location = detectable_asteroid_counts[max_detectable_asteroids]
print(station_location)

