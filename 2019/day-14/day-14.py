import re
from collections import Counter


class Ingredient:
    quantity = None
    material = None

    def __init__(self, quantity, material):
        self.quantity = quantity
        self.material = material

    def get_material(self):
        return self.material

    def get_quantity(self):
        return self.quantity


class Reaction:
    inputs = []
    output = None
    INGREDIENT_PATTERN = r'[0-9]+ [A-Z]+'

    def __init__(self, string):
        (inputs, output) = string.split(' => ')
        inputs = re.findall(self.INGREDIENT_PATTERN, inputs)
        output = re.findall(self.INGREDIENT_PATTERN, output)[0]

        (output_quantity, output_material) = output.split(' ')
        self.output = Ingredient(int(output_quantity), output_material)

        inputs = [
            input.split(' ') for input in inputs
        ]
        self.inputs = [
            Ingredient(int(input[0]), input[1]) for input in inputs
        ]

    def get_output(self):
        return self.output

    def get_inputs(self):
        return self.inputs

    def consume_ingredient(self, ingredient, available_materials):
        if ingredient in self.inputs:
            available_materials.update({
                ingredient.get_material(): -1 * ingredient.get_quantity()
            })
        else:
            raise Exception(
                'Unrecognized ingredient: {} {}'.format(ingredient.get_quantity(), ingredient.get_material())
            )

    def produce(self, available_materials):
        available_materials.update({
            self.output.get_material(): self.output.get_quantity()
        })


class Production:
    available_reaction_dict = None
    available_materials = None
    raw_material = None
    raw_material_count = None

    def __init__(self, reactions, raw_material):
        self.available_reaction_dict = {
            reaction.get_output().get_material(): reaction
            for reaction in reactions
        }
        self.raw_material = raw_material
        self.available_materials = Counter()
        self.raw_material_count = 0

    def get_raw_material_count(self):
        return self.raw_material_count

    def get_available_material_count(self):
        return sum(self.available_materials.values())

    def get_available_materials(self):
        return self.available_materials

    def reset(self):
        self.available_materials = Counter()
        self.raw_material_count = 0

    def add_or_consume_material(self, quantity, material):
        self.available_materials.update({
            material: quantity
        })

    def multiply_all_available_materials(self, multiplier):
        self.available_materials = {
            key: value * multiplier
            for key, value in self.available_materials.items()
        }

    def produce_material(self, quantity, material, allow_raw_material_production=True):
        quantity_produced = 0
        while quantity_produced < quantity:
            reaction = self.available_reaction_dict[material]
            inputs = reaction.get_inputs()
            for ingredient in inputs:
                ingredient_quantity = ingredient.get_quantity()
                ingredient_material = ingredient.get_material()
                if self.available_materials[ingredient_material] < ingredient_quantity:
                    if ingredient_material == self.raw_material:
                        if allow_raw_material_production:
                            self.available_materials.update({
                                ingredient_material: ingredient_quantity
                            })
                            self.raw_material_count += ingredient_quantity
                        else:
                            return False
                    else:
                        success = self.produce_material(
                            ingredient_quantity - self.available_materials[ingredient_material],
                            ingredient_material,
                            allow_raw_material_production=allow_raw_material_production
                        )
                        if not success:
                            return False

                reaction.consume_ingredient(ingredient, self.available_materials)

            reaction.produce(self.available_materials)
            quantity_produced += reaction.get_output().get_quantity()

        return True


FUEL = 'FUEL'
ORE = 'ORE'
TOTAL_ORE_COUNT = 1000000000000

with open('input.txt', 'r') as f:
    reaction_strings = f.readlines()

reactions = [
    Reaction(reaction_string) for reaction_string in reaction_strings
]

# Part 1
p = Production(reactions, ORE)
p.produce_material(1, FUEL)
ore_to_produce_one_fuel = p.get_raw_material_count()
print(ore_to_produce_one_fuel)

# Part 2
min_fuel_produced = TOTAL_ORE_COUNT // ore_to_produce_one_fuel
p.reset()
p.produce_material(min_fuel_produced, FUEL)
print(p.get_raw_material_count())



# Attempt 2:
# leftover_ore = TOTAL_ORE_COUNT % ore_to_produce_one_fuel
# p.multiply_all_available_materials(min_fuel_produced)
# p.add_or_consume_material(leftover_ore, ORE)
#
# additional_fuel_produced = 0
# while True:
#     success = p.produce_material(1, FUEL, allow_raw_material_production=False)
#     if not success:
#         break
#     additional_fuel_produced += 1
#     print(additional_fuel_produced)
# print(min_fuel_produced)
# print(min_fuel_produced + additional_fuel_produced)


# Attempt 1:
# p = Production(reactions, ORE)
# fuel_per_period = 0
# while True:
#     p.produce_material(1, FUEL)
#     p.add_or_consume_material(-1, FUEL)
#     fuel_per_period += 1
#     if p.get_available_material_count() == 0:
#         break
#
# ore_per_period = p.get_raw_material_count()
# number_of_periods = (ORE_COUNT // ore_per_period)
# fuel_produced = number_of_periods * fuel_per_period
# leftover_ores = ORE_COUNT % ore_per_period
#
# p.reset()
# leftover_fuel_produced = 0
# while True:
#     p.produce_material(1, FUEL)
#     if p.raw_material_count > leftover_ores:
#         break
#     leftover_fuel_produced += 1
#
# fuel_produced += leftover_fuel_produced
# print(fuel_produced)
