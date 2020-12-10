from collections import Counter


def build_adapter_mapping(adapter_ratings, max_difference):

    def get_next_possible_adapters(rating, rating_index, max_difference, adapter_ratings):
        index = rating_index + 1
        valid_adapters = []
        while index < len(adapter_ratings) and (adapter_ratings[index] - rating) <= max_difference:
            valid_adapters.append(index)
            index += 1

        return valid_adapters

    mapping = {
        index: get_next_possible_adapters(rating, index, max_difference, adapter_ratings)
        for index, rating in enumerate(adapter_ratings[0:-1])
    }

    return mapping


def count_possible_paths_to_end(mapping, current_index, path_length, completed_path_dict):
    if current_index == (path_length - 1):
        return 1

    paths_to_end = 0
    next_indexes = mapping[current_index]
    for next_index in next_indexes:
        try:
            paths_to_end += completed_path_dict[next_index]
        except KeyError:
            paths_to_end += count_possible_paths_to_end(mapping, next_index, path_length, completed_path_dict)

    # Once the number of paths to the end from an index is found, store it in complete_path_dict
    # so that next time it's reach it won't be checked again.
    completed_path_dict[current_index] = paths_to_end
    return paths_to_end


MAX_ADAPTER_DIFFERENCE = 3

with open('input.txt', 'r') as f:
    adapter_ratings = [
        int(line) for line in f
    ]

adapter_ratings.sort()

adapter_ratings = [0, *adapter_ratings, adapter_ratings[-1] + 3]

# Part 1
rating_differences = [
    rating - (adapter_ratings[index - 1] if index > 0 else 0)
    for index, rating in enumerate(adapter_ratings)
]

c = Counter(rating_differences)
print(c[1] * c[3])

# Part 2
adapter_mapping = build_adapter_mapping(adapter_ratings, MAX_ADAPTER_DIFFERENCE)
print(count_possible_paths_to_end(adapter_mapping, 0, len(adapter_ratings), {}))

