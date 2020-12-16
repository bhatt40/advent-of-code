
def get_new_number(game_dict, current_index, prev_num):
    try:
        last_occurence = game_dict[prev_num]
        new_num = current_index - 1 - last_occurence
    except KeyError:
        new_num = 0

    return new_num


def play_game_for_n_turns(game_dict, current_index, prev_num, n):
    while current_index < n:
        new_num = get_new_number(game_dict, current_index, prev_num)
        game_dict.update({
            prev_num: current_index - 1
        })

        prev_num = new_num
        current_index += 1

    return prev_num


INPUTS = [6, 3, 15, 13, 1, 0]

# Part 1
game_dict = {
    value: index
    for index, value in enumerate(INPUTS)
}

print(play_game_for_n_turns(game_dict, len(INPUTS), INPUTS[-1], 2020))

# Part 2
game_dict = {
    value: index
    for index, value in enumerate(INPUTS)
}

print(play_game_for_n_turns(game_dict, len(INPUTS),  INPUTS[-1], 30000000))
