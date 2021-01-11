from intcode_computer import IntcodeComputer

with open('input.txt', 'r') as f:
    origin_memory = [
        int(x) for x in f.readline().split(',')
    ]


def is_being_pulled(x, y):
    intcode_computer = IntcodeComputer(origin_memory, [x, y])
    intcode_computer.run()
    return intcode_computer.pop_last_output() == 1


SHIP_SIZE = 100

# Part 1
count = 0
for y in range(50):
    for x in range(50):
        intcode_computer = IntcodeComputer(origin_memory, [x, y])
        intcode_computer.run()
        count += intcode_computer.pop_last_output()

# Part 2
y = 0
x = 0
while True:
    # Find first x in row being pulled. Jump forward in increments of 10, then back up in increments of 1.
    while x < y:
        if is_being_pulled(x, y):
            break
        x += 1

    other_x = x + (SHIP_SIZE - 1)
    other_y = y - (SHIP_SIZE - 1)
    if is_being_pulled(other_x, other_y):
        break
    y += 1

closest_point = (x, y - (SHIP_SIZE - 1))
print(closest_point[0] * 10000 + closest_point[1])
