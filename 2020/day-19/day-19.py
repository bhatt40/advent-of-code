import re


def parse_rule_string(rule_string):
    (key, rule) = rule_string.split(':')
    if '"' in rule:
        rule = [rule.strip()[1]]
    else:
        rule = rule.strip().split(' ')
    return int(key), rule


def create_regex_mapping(mapping):
    regex_mapping = {}
    for k, rule in mapping.items():
        add_to_regex_mapping(k, rule, regex_mapping, mapping)

    return regex_mapping


def add_to_regex_mapping(k, rule, regex_mapping, rule_mapping):
    value = ''.join([
        get_value(value, regex_mapping, rule_mapping) for value in rule
    ])
    regex_mapping[k] = value if len(value) == 1 else '({})'.format(value)


def get_value(v, regex_mapping, rule_mapping):
    try:
        v = int(v)
    except ValueError:
        return v
    try:
        return regex_mapping[v]
    except KeyError:
        add_to_regex_mapping(v, rule_mapping[v], regex_mapping, rule_mapping)
    return regex_mapping[v]


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

regex_mapping = create_regex_mapping(rule_mapping)
regex_mapping = {
    k: '^{}$'.format(v) for k, v in regex_mapping.items()
}

message_is_valid = [
    bool(re.match(regex_mapping[0], m)) for m in messages
]

print(sum(message_is_valid))
