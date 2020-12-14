from intcode_computer import IntcodeComputer


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def safe_add_character_to_screen(screen, x, y, character):
    try:
        row = screen[y]
    except IndexError:
        current_height = len(screen)
        screen = [
            screen[index] if index < current_height else []
            for index in range(y + 1)
        ]
        row = screen[y]

    try:
        row[x] = character
    except IndexError:
        current_width = len(row)
        row = [
            row[index] if index < current_width else ' '
            for index in range(x + 1)
        ]
        row[x] = character
        screen[y] = row

    return screen


def update_screen(screen, outputs):
    tile_id_character_mapping = {
        0: ' ',
        1: 'X',
        2: '#',
        3: '_',
        4: 'O'
    }

    ball_x = -1
    paddle_x = -1
    score = 0

    for (x, y, tile_id) in chunks(outputs, 3):
        if x == -1:
            score = tile_id
        else:
            if tile_id == 3:
                paddle_x = x
            elif tile_id == 4:
                ball_x = x
            screen = safe_add_character_to_screen(screen, x, y, tile_id_character_mapping[tile_id])

    return screen, ball_x, paddle_x, score


def print_screen(screen):
    for row in screen:
        print(''.join(row))


with open('input.txt', 'r') as f:
    origin_memory = [
        int(x) for x in f.readline().split(',')
    ]

# Part 1
intcode_computer = IntcodeComputer(origin_memory, [])
intcode_computer.run()

outputs = intcode_computer.get_all_outputs()

block_count = 0
for index, output in enumerate(outputs):
    if index % 3 == 2 and output == 2:
        block_count += 1

print(block_count)

# Part 2
memory = origin_memory.copy()
memory[0] = 2
intcode_computer = IntcodeComputer(memory, [])
screen = [[]]
score = 0

while not intcode_computer.is_complete():
    intcode_computer.run()
    outputs = intcode_computer.get_all_outputs()
    screen, ball, paddle, score = update_screen(screen, outputs)
    print_screen(screen)
    input = 1 if ball > paddle else -1 if ball < paddle else 0
    intcode_computer.append_new_input(input)

print(score)
