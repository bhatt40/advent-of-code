
def check_time(time, buses):
    return all([
        time % bus == delay
        for bus, delay in buses.items()
    ])


with open('input.txt', 'r') as f:
    departure_time = int(f.readline())
    bus_schedule = f.readline().split('\n')[0]


# Part 1
buses = bus_schedule.split(',')
buses = filter(lambda a: a != 'x', buses)
buses = [
    int(bus) for bus in buses
]

time = departure_time
earliest_bus = None
while earliest_bus is None:
    time += 1
    for bus in buses:
        if time % bus == 0:
            earliest_bus = bus
            break

wait_time = time - departure_time
print(wait_time * bus)

# Part 2
buses = bus_schedule.split(',')
first_bus = int(buses[0])
buses = buses[1:]

period = first_bus
time = 0
for index, bus in enumerate(buses):
    if bus != 'x':
        bus = int(bus)
        target = (bus - (index + 1)) % bus
        while True:
            time += period
            if time % bus == target:
                break

        period = bus * period

print(time)

