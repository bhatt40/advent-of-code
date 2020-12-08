import re


def parse_inner_bags_string(inner_bags_string):
    rule_strings = inner_bags_string.split(',')
    inner_bag_rules = []
    for rule_string in rule_strings:
        m = re.match(r'^ ?(?P<number>[0-9]+) (?P<color>[a-z ]+) bag[s]?[.]?$', rule_string)
        if m:
            inner_bag_rules.append((int(m.group('number')), m.group('color')))

    return inner_bag_rules


def parse_rule_string(rule_string):
    [outer_bag_string, inner_bags_string] = rule_string.split('contain')
    outer_bag_color = outer_bag_string.split(' bags')[0]
    inner_bag_rules = parse_inner_bags_string(inner_bags_string)
    return outer_bag_color, inner_bag_rules


def build_inner_to_outer_rule_mapping(rule_strings):
    mapping = {}
    for rule_string in rule_strings:
        outer_bag_color, inner_bag_rules = parse_rule_string(rule_string)
        for (number, inner_bag_color) in inner_bag_rules:
            rule = (number, outer_bag_color)
            try:
                mapping[inner_bag_color].append(rule)
            except KeyError:
                mapping.update({
                    inner_bag_color: [rule]
                })

    return mapping


def build_outer_to_inner_rule_mapping(rule_strings):
    mapping = {}
    for rule_string in rule_strings:
        outer_bag_color, inner_bag_rules = parse_rule_string(rule_string)
        try:
            mapping[outer_bag_color].extend(inner_bag_rules)
        except KeyError:
            mapping.update({
                outer_bag_color: inner_bag_rules
            })

    return mapping


def find_outer_bag_colors(mapping, bag_color, color_set):
    color_set.add(bag_color)
    try:
        for (number, color) in mapping[bag_color]:
            find_outer_bag_colors(mapping, color, outer_bag_color_set)
    except KeyError:
        pass


def count_inner_bags(mapping, bag_color, multiplier):
    sum = 1
    for (number, color) in mapping[bag_color]:
       sum += count_inner_bags(mapping, color, number)
    return sum * multiplier


MY_BAG_COLOR = 'shiny gold'

with open('input.txt', 'r') as f:
    rule_strings = f.readlines()

# Part 1
rule_mapping = build_inner_to_outer_rule_mapping(rule_strings)
outer_bag_color_set = set()
find_outer_bag_colors(rule_mapping, MY_BAG_COLOR, outer_bag_color_set)
outer_bag_color_set.remove(MY_BAG_COLOR)
print(len(outer_bag_color_set))

# Part 2
rule_mapping = build_outer_to_inner_rule_mapping(rule_strings)
print(count_inner_bags(rule_mapping, MY_BAG_COLOR, 1) - 1)
