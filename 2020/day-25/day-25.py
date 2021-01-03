
def transform(n, subject_number):
    n = n * subject_number
    return n % 20201227


def get_loop_size(public_key, subject_number):
    loops = 0
    v = 1
    while v != public_key:
        v = transform(v, subject_number)
        loops += 1

    return loops


# Part 1
CARD_PUBLIC_KEY = 8458505
DOOR_PUBLIC_KEY = 16050997
SUBJECT_NUMBER = 7

card_loop_size = get_loop_size(CARD_PUBLIC_KEY, SUBJECT_NUMBER)
door_loop_size = get_loop_size(DOOR_PUBLIC_KEY, SUBJECT_NUMBER)

encryption_key = 1
for _ in range(card_loop_size):
    encryption_key = transform(encryption_key, DOOR_PUBLIC_KEY)

print(encryption_key)
