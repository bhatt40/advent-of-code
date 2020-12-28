import time


def parse_rule_string(rule_string):
    (key, rule) = rule_string.split(':')
    if '"' in rule:
        rule = [rule.strip()[1]]
    else:
        paths = rule.strip().split('|')
        rule = [
            [
                int(x) for x in path.strip().split(' ')
            ]
            for path in paths
        ]
    return int(key), rule


def replace_key_with_value(key_to_replace, replacement_values, values_to_check):
    for other_paths in values_to_check:
        if isinstance(other_paths, list):
            for other_paths_index, other_path in enumerate(other_paths):
                for other_path_index, k in enumerate(other_path):
                    if k == key_to_replace:
                        new_paths = [
                            [
                                p if i == other_path_index else x
                                for i, x in enumerate(other_paths[other_paths_index])
                            ]
                            for p in replacement_values
                        ]
                        l = len(new_paths)
                        other_paths[other_paths_index:other_paths_index + 1] = new_paths
                        for i in range(other_paths_index, other_paths_index + l):
                            try:
                                other_paths[i] = ''.join(other_paths[i])
                            except TypeError:
                                pass


def translate_mapping(mapping, keys_that_wont_complete=0):
    completed_key_set = set()
    while len(completed_key_set) < (len(mapping.keys()) - keys_that_wont_complete):
        for completed_key, completed_paths in mapping.items():
            if all([isinstance(completed_path, str) for completed_path in completed_paths]):
                # Replace all instances of key with its string value
                replace_key_with_value(completed_key, completed_paths, mapping.values())
                completed_key_set.add(completed_key)

    uncompleted_keys = set(mapping.keys()) - completed_key_set
    uncompleted_mapping = {
        k: mapping[k] for k in uncompleted_keys
    }

    while max([ len(x) for x in uncompleted_mapping[0] ]) < 96:
        print(max([ len(x[0]) for x in uncompleted_mapping[0] ]))
        for uncompleted_key in uncompleted_keys:
            uncompleted_paths = uncompleted_mapping[uncompleted_key]
            replace_key_with_value(uncompleted_key, uncompleted_paths, uncompleted_mapping.values())

    print('here')

rule_strings = []

with open('input.txt', 'r') as f:
    while True:
        rule_string = f.readline()
        if rule_string == '\n':
            break
        rule_strings.append(rule_string.split('\n')[0])

    messages = [
        m.split('\n')[0] for m in f.readlines()
    ]

rule_mapping = {}
for rule_string in rule_strings:
    k, g = parse_rule_string(rule_string)
    rule_mapping[k] = g

# Part 1
# rule_mapping_1 = rule_mapping.copy()
# translate_mapping(rule_mapping_1)
#
# message_is_valid = [
#     any([
#        v == message for v in rule_mapping_1[0]
#     ])
#     for message in messages
# ]
#
# print(sum(message_is_valid))

# Part 2
rule_mapping_2 = rule_mapping.copy()

new_strings = [
    '8: 42 | 42 8',
    '11: 42 31 | 42 11 31'
]
for string in new_strings:
    k, g = parse_rule_string(rule_string)
    rule_mapping_2[k] = g

longest_message_length = max([
    len(m) for m in messages
])
print(longest_message_length)

translate_mapping(rule_mapping_2, keys_that_wont_complete=3)

print(rule_mapping_2[0])

