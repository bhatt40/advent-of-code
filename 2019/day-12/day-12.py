import re
import functools
from math import gcd


class Moon:
    x = None
    y = None
    z = None

    dx = None
    dy = None
    dz = None

    def __init__(self, position_string):
        m = re.match(r'^<x=(?P<x>[0-9\-]+), y=(?P<y>[0-9\-]+), z=(?P<z>[0-9\-]+)>$', position_string)
        self.x = int(m.group('x'))
        self.y = int(m.group('y'))
        self.z = int(m.group('z'))

        self.dx = 0
        self.dy = 0
        self.dz = 0

    def get_position(self):
        return self.x, self.y, self.z

    def get_velocity(self):
        return self.dx, self.dy, self.dz

    def apply_gravity(self, other_bodies):
        for body in other_bodies:
            (x, y, z) = body.get_position()
            self.dx += 1 if x > self.x else -1 if x < self.x else 0
            self.dy += 1 if y > self.y else -1 if y < self.y else 0
            self.dz += 1 if z > self.z else -1 if z < self.z else 0

    def move(self):
        self.x += self.dx
        self.y += self.dy
        self.z += self.dz

    def calculate_energy(self):
        absolute_energy = abs(self.x) + abs(self.y) + abs(self.z)
        kinetic_energy = abs(self.dx) + abs(self.dy) + abs(self.dz)
        return absolute_energy * kinetic_energy


def step_system_time(moons):
    for moon in moons:
        moon.apply_gravity(moons)

    for moon in moons:
        moon.move()


def calculate_system_energy(moons):
    return functools.reduce(lambda a, b: a + b.calculate_energy(), moons, 0)


def step_single_axis(positions, velocities):
    gravity = [
        [
            1 if other_position > position else -1 if other_position < position else 0 for other_position in positions
        ] for position in positions
    ]

    velocities = [
        velocity + sum(gravity[index])
        for index, velocity in enumerate(velocities)
    ]

    positions = [
        position + velocities[index]
        for index, position in enumerate(positions)
    ]

    return positions, velocities


def determine_axis_orbit_period(moons, axis_index):
    positions = [
        moon.get_position()[axis_index] for moon in moons
    ]

    velocities = [
        moon.get_velocity()[axis_index] for moon in moons
    ]
    original_positions = positions.copy()
    original_velocities = velocities.copy()

    orbit_period = 0
    while True:
        positions, velocities = step_single_axis(positions, velocities)
        orbit_period += 1
        if positions == original_positions and velocities == original_velocities:
            break

    return orbit_period


def calculate_least_common_multiple(nums):
    return functools.reduce(lambda a, b: a * b // gcd(a, b), nums)


STEPS_TO_APPLY = 1000


with open('input.txt', 'r') as f:
    moon_position_strings = f.readlines()

# Part 1
moons = [
    Moon(string) for string in moon_position_strings
]

for _ in range(STEPS_TO_APPLY):
    step_system_time(moons)

print(calculate_system_energy(moons))

# Part 2
moons = [
    Moon(string) for string in moon_position_strings
]

x_orbit_period = determine_axis_orbit_period(moons, 0)
y_orbit_period = determine_axis_orbit_period(moons, 1)
z_orbit_period = determine_axis_orbit_period(moons, 2)

print(calculate_least_common_multiple([x_orbit_period, y_orbit_period, z_orbit_period]))
