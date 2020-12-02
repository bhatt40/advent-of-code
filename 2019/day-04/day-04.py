def count_valid_passwords_in_range(min, max, limit_adjacent_duplicates_to_two=False):
    count = 0

    for number in range(min, max + 1):
        number_string = str(number)
        has_decreasing_pair_of_digits = False
        has_adjacent_duplicates = False
        has_two_adjacent_duplicates = False
        current_duplicates_streak = 1

        for index in range(1, len(number_string)):
            if number_string[index] < number_string[index - 1]:
                has_decreasing_pair_of_digits = True
            elif number_string[index] == number_string[index - 1]:
                has_adjacent_duplicates = True
                current_duplicates_streak += 1
            else:
                if current_duplicates_streak == 2:
                    has_two_adjacent_duplicates = True
                current_duplicates_streak = 1

        # In case number ends with two duplicates
        if current_duplicates_streak == 2:
            has_two_adjacent_duplicates = True

        if has_adjacent_duplicates and not has_decreasing_pair_of_digits and not (
            limit_adjacent_duplicates_to_two and not has_two_adjacent_duplicates
        ):
            count += 1

    return count


INPUT_MIN = 134564
INPUT_MAX = 585159

valid_password_count = count_valid_passwords_in_range(INPUT_MIN, INPUT_MAX)
print(valid_password_count)

valid_password_count = count_valid_passwords_in_range(INPUT_MIN, INPUT_MAX, limit_adjacent_duplicates_to_two=True)
print(valid_password_count)
