
def parse_food(string):
    ingredients, allergens = string.split(')')[0].split(' (contains ')
    ingredients = set(ingredients.split(' '))
    allergens = set(allergens.split(', '))
    return ingredients, allergens


def determine_allergens(mapping):
    mapping_complete = False
    while not mapping_complete:
        mapping_complete = True
        for allergen, possible_ingredients in mapping.items():
            if type(possible_ingredients) == set:
                mapping_complete = False
                if len(possible_ingredients) == 1:
                    allergen_ingredient = possible_ingredients.pop()
                    mapping.update({
                        allergen: allergen_ingredient
                    })
                    for other_possible_ingredients in mapping.values():
                        if type(other_possible_ingredients) == set:
                            try:
                                other_possible_ingredients.remove(allergen_ingredient)
                            except KeyError:
                                pass


def count_safe_ingredients(foods, allergen_ingredients):
    count = 0
    for ingredients, allergens in foods:
        safe_ingredients = ingredients - allergen_ingredients
        count += len(safe_ingredients)

    return count


def get_ingredients_sorted_by_allergen(mapping):
    allergen_list = [
        {
            'allergen': allergen,
            'ingredient': ingredient
        } for allergen, ingredient in mapping.items()
    ]

    allergen_list = sorted(allergen_list, key=lambda allergen: allergen['allergen'])

    return ','.join([
        allergen['ingredient'] for allergen in allergen_list
    ])


with open('input.txt', 'r') as f:
    lines = f.readlines()

foods = [
    parse_food(line) for line in lines
]
allergen_mapping = {}

for ingredients, allergens in foods:
    for allergen in allergens:
        if allergen not in allergen_mapping:
            # Find all foods that have allergen. Then find all common ingredients in those foods.
            possible_ingredients = None
            for ingredients, allergens in foods:
                if allergen in allergens:
                    possible_ingredients = ingredients if possible_ingredients is None else possible_ingredients & ingredients
            allergen_mapping.update({
                allergen: possible_ingredients
            })

determine_allergens(allergen_mapping)

# Part 1
print(count_safe_ingredients(foods, set(allergen_mapping.values())))

# Part 2
print(get_ingredients_sorted_by_allergen(allergen_mapping))
