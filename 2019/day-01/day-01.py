
def calculate_module_fuel(module_mass):
    return (module_mass // 3) - 2


def calculate_module_total_fuel(module_mass):
    fuel = calculate_module_fuel(module_mass)
    if fuel <= 0:
        return 0
    return fuel + calculate_module_total_fuel(fuel)


with open('input.txt', 'r') as f:
    masses = [
        int(line) for line in f
    ]

# Part 1
total_fuel = 0
for mass in masses:
    total_fuel += calculate_module_fuel(mass)

print(total_fuel)

# Part 2
total_fuel = 0
for mass in masses:
    total_fuel += calculate_module_total_fuel(mass)

print(total_fuel)
