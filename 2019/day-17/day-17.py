from intcode_computer import IntcodeComputer


def parse_camera_view(output):
    character_dict = {
        35: '#',
        46: '.',
        94: '^',
        10: '\n'
    }
    view = []
    line = ''
    for x in output:
        c = character_dict[x]
        if c == '\n':
            view.append(line)
            line = ''
            continue
        line += c

    return view


def print_view(view):
    for line in view:
        print(line)


def get_intersections(view):
    intersections = set()
    for li, line in enumerate(view):
        for ci, c in enumerate(line):
            try:
                if c not in ['#', '^']:
                    continue
                if all([
                    x in ['#', '^']
                    for x in [
                        line[ci - 1],
                        line[ci + 1],
                        view[li - 1][ci],
                        view[li + 1][ci]
                    ]
                ]):
                    intersections.add((ci, li))
            except IndexError:
                continue

    return intersections


def collect_dust(memory, main, functions, continuous_video_feed=False):
    memory[0] = 2

    inputs = main + functions[0] + functions[1] + functions[2] + [121 if continuous_video_feed else 110, 10]
    intcode_computer = IntcodeComputer(memory, initial_inputs=inputs)
    intcode_computer.run()
    return intcode_computer.get_all_outputs()


with open('input.txt', 'r') as f:
    origin_memory = [
        int(x) for x in f.readline().split(',')
    ]

# Part 1
intcode_computer = IntcodeComputer(origin_memory, [])
intcode_computer.run()
camera_view = parse_camera_view(intcode_computer.get_all_outputs())

print_view(camera_view)
intersections = get_intersections(camera_view)
alignment_parameters = [
    x * y for x, y in intersections
]
print(sum(alignment_parameters))

# Part 2

# Uncompressed sequence
# L,10,R,8,L,6,R,6,L,8,L,8,R,8,L,10,R,8,L,6,R,6,R,8,L,6,L,10,L,10,L,10,R,8,L,6,R,6,L,8,L,8,R,8,R,8,L6,L,10,L,10,L8,L,8,R,8,R,8,L,6,L,10,L,10,L,8,L,8,R,8

# Main sequence
# A,B,A,C,A,B,C,B,C,B

# Function A
# L,10,R,8,L,6,R,6

# Function B
# L,8,L,8,R,8

# Function C
# R,8,L,6,L,10,L,10

movement_routine = [65, 44, 66, 44, 65, 44, 67, 44, 65, 44, 66, 44, 67, 44, 66, 44, 67, 44, 66, 10]
function_a = [76, 44, 49, 48, 44, 82, 44, 56, 44, 76, 44, 54, 44, 82, 44, 54, 10]
function_b = [76, 44, 56, 44, 76, 44, 56, 44, 82, 44, 56, 10]
function_c = [82, 44, 56, 44, 76, 44, 54, 44, 76, 44, 49, 48, 44, 76, 44, 49, 48, 10]

dust_count = collect_dust(origin_memory, movement_routine, [function_a, function_b, function_c], continuous_video_feed=False)
print(dust_count)
