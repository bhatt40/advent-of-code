from itertools import product
import re


def parse_instruction(string):
    [o, v] = string.split('\n')[0].split(' = ')
    return o, v


def apply_value_mask(mask, value):
    binary_value = '{0:b}'.format(value)
    binary_value = '{}{}'.format(
        ''.join('0' for _ in range(36 - len(binary_value))),
        binary_value
    )
    binary_value = ''.join([
        '0' if bit == '0' else '1' if bit == '1' else binary_value[index]
        for index, bit in enumerate(mask)
    ])
    return int(binary_value, 2)


def apply_memory_address_mask(mask, address):
    binary_address = '{0:b}'.format(address)
    binary_address = '{}{}'.format(
        ''.join('0' for _ in range(36 - len(binary_address))),
        binary_address
    )
    binary_address = ''.join([
        '{}' if bit == 'X' else '1' if bit == '1' else binary_address[index]
        for index, bit in enumerate(mask)
    ])
    floater_count = binary_address.count('{}')
    products = product('01', repeat=floater_count)
    floating_binary_addresses = [
        binary_address.format(*p)
        for p in products
    ]
    return [
        int(a, 2) for a in floating_binary_addresses
    ]


def execute_instructions(memory, instructions, version=1):
    mask = None
    for instruction in instructions:
        operation, value = parse_instruction(instruction)
        if operation == 'mask':
            mask = value
        else:
            m = re.match(r'^mem\[(?P<address>[0-9]+)\]$', operation)
            address = m.group('address')

            if version == 1:
                value = apply_value_mask(mask, int(value))
                memory.update({
                    address: value
                })
            elif version == 2:
                memory_addresses = apply_memory_address_mask(mask, int(address))
                for memory_address in memory_addresses:
                    memory.update({
                        memory_address: int(value)
                    })

    return memory


with open('input.txt', 'r') as f:
    instructions = f.readlines()


# Part 1
memory = execute_instructions({}, instructions, version=1)
print(sum(memory.values()))

# Part 2
memory = execute_instructions({}, instructions, version=2)
print(sum(memory.values()))
