from intcode_computer import IntcodeComputer
from queue import Queue, Empty


def setup_network():
    intcode_computers = [
        None for _ in range(NUMBER_OF_COMPUTERS)
    ]

    input_queues = [
        Queue() for _ in range(NUMBER_OF_COMPUTERS)
    ]

    for i in range(NUMBER_OF_COMPUTERS):
        intcode_computer = IntcodeComputer(origin_memory, [i])
        intcode_computer.run()
        intcode_computers[i] = intcode_computer

    return intcode_computers, input_queues


def run_network(intcode_computers, input_queues, nat_address, terminate_on_nat=False):
    i = 0
    nat = None
    empty_inputs = [
        False for _ in range(NUMBER_OF_COMPUTERS)
    ]
    empty_outputs = [
        False for _ in range(NUMBER_OF_COMPUTERS)
    ]
    last_delivered_y = None

    while True:
        if all(empty_inputs) and all(empty_outputs):
            if nat[1] == last_delivered_y:
                return nat[1]
            last_delivered_y = nat[1]
            input_queues[0].put(nat)
            i = 0

        try:
            x, y = input_queues[i].get(block=False)
        except Empty:
            x = -1
            y = None
            empty_inputs[i] = True
        else:
            empty_inputs[i] = False

        intcode_computer = intcode_computers[i]
        intcode_computer.append_new_input(x)
        if y:
            intcode_computer.append_new_input(y)

        intcode_computer.run()

        outputs = intcode_computer.get_all_outputs()
        empty_outputs[i] = len(outputs) == 0
        for i, o in enumerate(outputs):
            if i % 3 == 0:
                dest = o
            elif i % 3 == 1:
                x = o
            else:
                y = o
                if dest == nat_address:
                    if terminate_on_nat:
                        return y
                    nat = (x, y)
                else:
                    dest_queue = input_queues[dest]
                    dest_queue.put((x, y))

        i = (i + 1) % NUMBER_OF_COMPUTERS


with open('input.txt', 'r') as f:
    origin_memory = [
        int(x) for x in f.readline().split(',')
    ]

NUMBER_OF_COMPUTERS = 50

# Part 1
intcode_computers, input_queues = setup_network()
y = run_network(intcode_computers, input_queues, 255, terminate_on_nat=True)
print(y)

# Part 2
intcode_computers, input_queues = setup_network()
y = run_network(intcode_computers, input_queues, 255, terminate_on_nat=False)
print(y)
