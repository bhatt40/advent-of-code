import re
import functools

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


def system_moon_positions_are_equal(moons, other_moons):
    return all([
        moon.get_position() == other_moons[index].get_position()
        for index, moon in enumerate(moons)
    ])


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
initial_moons = [
    Moon(string) for string in moon_position_strings
]

step_counter = 0
while True:
    step_system_time(moons)
    if system_moon_positions_are_equal(moons, initial_moons):
        break
    step_counter += 1
    print(step_counter)

print(step_counter)
