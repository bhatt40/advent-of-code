
def parse_rule_string(string):
    [field, ranges] = string.split(': ')
    ranges = ranges.split(' or ')
    ranges = [
        range.split('-') for range in ranges
    ]
    ranges = [
        [int(range[0]), int(range[1])] for range in ranges
    ]
    return field, ranges


def is_valid_value(value, rules):
    for ranges in rules.values():
        for range in ranges:
            if value >= range[0] and value <= range[1]:
                return True

    return False


def calculate_error_rate(ticket, rules):
    return sum(filter(lambda x: not is_valid_value(x, rules), ticket))


def get_possible_fields(values, rules):
    fields = set()
    for field, ranges in rules.items():
        if all([
            any([
                value >= range[0] and value <= range[1]
                for range in ranges
            ])
            for value in values
        ]):
            fields.add(field)

    return fields


def has_no_zeroes(ticket):
    try:
        zero = ticket.index(0)
    except ValueError:
        return True

    return False


field_rules = {}

with open('input.txt', 'r') as f:
    while True:
        rule_string = f.readline().split('\n')[0]
        if not rule_string:
            break

        field, ranges = parse_rule_string(rule_string)
        field_rules[field] = ranges

    f.readline()  # your ticket:
    my_ticket = f.readline().split('\n')[0].split(',')
    my_ticket = [
        int(value) for value in my_ticket
    ]

    f.readline()  # blank
    f.readline()  # nearby tickets:

    nearby_tickets = [
        line.split('\n')[0].split(',') for line in f.readlines()
    ]
    nearby_tickets = [
        [
            int(value) for value in ticket
        ]
        for ticket in nearby_tickets
    ]

# Part 1
error_rates = [
    calculate_error_rate(ticket, field_rules) for ticket in nearby_tickets
]

print(sum(error_rates))

# Part 2
valid_tickets = list(filter(
    lambda x: calculate_error_rate(x, field_rules) == 0 and has_no_zeroes(x),
    nearby_tickets
))

possible_fields = {}
for index in range(len(my_ticket)):
    values = [
        ticket[index] for ticket in valid_tickets
    ]
    possible_fields[index] = get_possible_fields(values, field_rules)

actual_fields = [
    '' for _ in range(len(my_ticket))
]
fields_set = 0

while fields_set < len(actual_fields):
    for index, fields in possible_fields.items():
        if len(fields) == 1:
            field_to_set = fields.pop()
            actual_fields[index] = field_to_set
            fields_set += 1
            for index, fields in possible_fields.items():
                try:
                    fields.remove(field_to_set)
                except KeyError:
                    pass

product_of_departure_fields = 1
for index, field in enumerate(actual_fields):
    if field.startswith('departure'):
        product_of_departure_fields *= my_ticket[index]

print(product_of_departure_fields)
