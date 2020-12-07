import functools
import string


def add_person_to_group(person, group):
    yes_answers = set([
        character for character in person.split('\n')[0]
    ])
    group.append(yes_answers)


def count_group_yes_answers(group, everyone=False):
    initial_set = set(string.ascii_lowercase) if everyone else set()
    group_yes_answers = functools.reduce(lambda a, b: a.intersection(b), group, initial_set) if everyone else \
        functools.reduce(lambda a, b: a.union(b), group, initial_set)
    return len(group_yes_answers)


def get_sum_of_group_yes_answers(groups, everyone_must_answer_yes=False):
    index = 0
    current_group = []
    sum_of_yes_answers = 0

    while index < len(groups):
        next_person = groups[index]
        if next_person == '\n':
            sum_of_yes_answers += count_group_yes_answers(current_group, everyone_must_answer_yes)
            current_group = []
        else:
            add_person_to_group(next_person, current_group)
        index += 1

    # Check last group
    sum_of_yes_answers += count_group_yes_answers(current_group, everyone_must_answer_yes)

    return sum_of_yes_answers


with open('input.txt', 'r') as f:
    groups = f.readlines()

# Part 1
print(get_sum_of_group_yes_answers(groups))

# Part 2
print(get_sum_of_group_yes_answers(groups, everyone_must_answer_yes=True))
