def parse_old_rule(rule_string):
    (count_range, character) = rule_string.split(' ')
    (min_count, max_count) = count_range.split('-')
    return character, int(min_count), int(max_count)


def parse_new_rule(rule_string):
    (indexes_string, character) = rule_string.split(' ')
    indexes = [
        int(index) for index in indexes_string.split('-')
    ]
    return character, indexes


with open('input.txt', 'r') as f:
    lines = f.readlines()

# Part 1
valid_password_count = 0
for line in lines:
    (rule, password) = line.split(':')
    character, min_count, max_count = parse_old_rule(rule)

    character_count = len(list(filter(lambda x: x == character, password)))

    if min_count <= character_count <= max_count:
        valid_password_count += 1

print(valid_password_count)

# Part 2
valid_password_count = 0
for line in lines:
    (rule, password) = line.split(':')
    character, indexes = parse_new_rule(rule)
    password = password.strip()

    character_matches = map(lambda x: password[x-1] == character, indexes)

    if len(list(filter(lambda x: x, character_matches))) == 1:
        valid_password_count += 1

print(valid_password_count)
