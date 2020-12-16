
def append_to_sequence(seq, index, num):
    try:
        seq[index] = num
    except IndexError:
        seq = [
            seq[index] if index < len(seq) else -1
            for index in range(2 * len(seq))
        ]
        seq[index] = num

    return seq


def find_last_instance(seq, index, num):
    while index >= 0:
        if seq[index] == num:
            return index
        index -= 1

    return None


def add_number(seq, prev_nums, current_index):
    prev_index = current_index - 1
    prev_num = seq[prev_index]
    if prev_num in prev_nums:
        last_index = find_last_instance(seq, current_index - 2, prev_num)
        seq = append_to_sequence(seq, current_index, prev_index - last_index)

    else:
        seq = append_to_sequence(seq, current_index, 0)
    prev_nums.add(prev_num)

    return seq


def play_game_for_n_turns(seq, n):
    previous_numbers = set(seq[0:-1])
    current_index = len(seq)

    while current_index < n:
        seq = add_number(seq, previous_numbers, current_index)
        current_index += 1

    return seq[current_index - 1]


INPUTS = [6, 3, 15, 13, 1, 0]

# Part 1
print(play_game_for_n_turns(INPUTS.copy(), 2020))

# Part 2
print(play_game_for_n_turns(INPUTS.copy(), 30000000))