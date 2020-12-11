from intcode_computer import IntcodeComputer


class Robot:
    location = None
    direction = None

    def __init__(self, initial_location, initial_direction):
        self.location = initial_location.copy()
        self.direction = initial_direction

    def get_location(self):
        return self.location

    def turn_and_move(self, command):
        angle_delta = 90 if command == 0 else -90
        self.direction = (self.direction + angle_delta) % 360
        self.move(1)

    def move(self, distance):
        if self.direction == 0:
            self.location[0] += distance
        elif self.direction == 90:
            self.location[1] += distance
        elif self.direction == 180:
            self.location[0] -= distance
        elif self.direction == 270:
            self.location[1] -= distance
        else:
            raise Exception('Robot facing invalid direction: {}'.format(self.direction))


class Panel:
    painted_locations = {}
    BLACK = 0
    WHITE = 1
    DEFAULT_COLOR = BLACK

    def __init__(self, initial_colors={}):
        self.painted_locations = initial_colors

    def get_painted_locations(self):
        return self.painted_locations

    def get_color_of_location(self, location):
        try:
            return self.painted_locations[location]
        except KeyError:
            return self.DEFAULT_COLOR

    def get_printed_value_of_location(self, location):
        color = self.get_color_of_location(location)
        return '.' if color == self.BLACK else 'X'

    def paint_location(self, location, color):
        self.painted_locations[location] = color

    def print(self):
        painted_location_list = self.painted_locations.keys()
        x_list, y_list = zip(*painted_location_list)

        min_x = min(x_list)
        max_x = max(x_list)

        min_y = min(y_list)
        max_y = max(y_list)

        y = max_y
        while y >= min_y:
            line = ''.join(
                [
                    '{} '.format(self.get_printed_value_of_location((x, y)))
                    for x in range(min_x, max_x + 1)
                ]
            )
            print(line)
            y -= 1


def paint_panel(c, r, p):
    while not c.is_complete():
        robot_location = tuple(r.get_location())
        location_color = p.get_color_of_location(robot_location)

        c.append_new_input(location_color)
        c.run()

        turn_command = c.pop_last_output()
        new_color = c.pop_last_output()

        p.paint_location(robot_location, new_color)
        r.turn_and_move(turn_command)


with open('input.txt', 'r') as f:
    origin_memory = [
        int(x) for x in f.readline().split(',')
    ]

STARTING_LOCATION = [0, 0]
STARTING_DIRECTION = 90  # Up

# Part 1
intcode_computer = IntcodeComputer(origin_memory, [])
robot = Robot(STARTING_LOCATION, STARTING_DIRECTION)
panel = Panel(initial_colors={})

paint_panel(intcode_computer, robot, panel)

painted_locations = panel.get_painted_locations().keys()
print(len(painted_locations))

# Part 2
intcode_computer = IntcodeComputer(origin_memory, [])
robot = Robot(STARTING_LOCATION, STARTING_DIRECTION)
panel = Panel(initial_colors={
    (0, 0): 1
})

paint_panel(intcode_computer, robot, panel)
panel.print()
