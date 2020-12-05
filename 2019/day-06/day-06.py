
def add_orbit_old(orbit_dict, orbit):
    (orbitee, orbiter) = orbit.split('\n')[0].split(')')
    orbiters = orbit_dict.get(orbitee, [])
    orbiters.append(orbiter)
    orbit_dict[orbitee] = orbiters

    if orbiter not in orbit_dict:
        orbit_dict[orbiter] = []


def add_orbit(orbit_dict, orbit):
    (orbitee, orbiter) = orbit.split('\n')[0].split(')')
    orbit_dict[orbiter] = orbitee


def get_orbits(orbit_dict, orbiter):
    orbits = []
    while orbiter in orbit_dict:
        orbiter = orbit_dict[orbiter]
        orbits.append(orbiter)

    return orbits


def calculate_distance_to_target(object_orbits, target):
    try:
        return object_orbits.index(target) + 1
    except ValueError:
        raise Exception('Object does not orbit target: {}'.format(target))


def get_minimum_distance(orbit_dict, object_a, object_b):
    object_a_orbits = get_orbits(orbit_dict, object_a)
    object_b_orbits = get_orbits(orbit_dict, object_b)

    intersection_set = set(object_a_orbits) & set(object_b_orbits)
    distances = map(
        lambda x: calculate_distance_to_target(object_a_orbits, x) + calculate_distance_to_target(object_b_orbits, x),
        intersection_set
    )

    return min(distances)


YOU = 'YOU'
SAN = 'SAN'

with open('input.txt', 'r') as f:
    orbits = f.readlines()

orbit_dict = {}
# Part 1
for orbit in orbits:
    add_orbit(orbit_dict, orbit)

orbit_counts = map(lambda x: len(get_orbits(orbit_dict, x)), orbit_dict.keys())
print(sum(orbit_counts))

# Part 2
you_orbitee = orbit_dict[YOU]
san_orbitee = orbit_dict[SAN]

print(get_minimum_distance(orbit_dict, you_orbitee, san_orbitee))
