
class Level:
    parent = None
    characters = None

    def __init__(self, parent):
        self.parent = parent
        self.characters = []

    def append_item(self, x):
        self.characters.append(x)

    def add_parentheses_around_additions(self):
        # If there is only one expression, evaluate levels and continue.
        if len(self.characters) <= 3:
            for item in self.characters:
                if isinstance(item, Level):
                    item.add_parentheses_around_additions()
            return

        index = 0
        while index < len(self.characters):
            expression = self.characters[index:index + 3]
            for item in expression:
                if isinstance(item, Level):
                    item.add_parentheses_around_additions()
            if len(expression) < 3:
                return

            if expression[1] == '+':
                new_level = Level(None)
                for i in range(3):
                    new_level.append_item(expression[i])
                before_index = max(0, index)
                self.characters = self.characters[:before_index] + [new_level] + self.characters[index + 3:]
            else:
                index += 2

    def __str__(self):
        return '{}{}{}'.format(
            '(',
            ''.join([ c.__str__() for c in self.characters]),
            ')'
        )

    def evaluate(self):
        index = 0
        current_expression = []
        value = None

        if len(self.characters) == 1:
            return self.characters[0].evaluate()

        while index < len(self.characters):
            while len(current_expression) < 3:
                next_character = self.characters[index]
                if isinstance(next_character, Level):
                    current_expression.append(next_character.evaluate())
                else:
                    current_expression.append(next_character)
                index += 1

            value = self.evaluate_expression(current_expression)
            current_expression = [value]

        return value

    @staticmethod
    def evaluate_expression(exp):
        if exp[1] == '+':
            return exp[0] + exp[2]
        else:
            return exp[0] * exp[2]


def parse_expression_string(e):
    top_level = Level(None)
    current_level = top_level

    for char in e:
        if char == ' ':
            continue
        if char == '(':
            new_level = Level(current_level)
            current_level.append_item(new_level)
            current_level = new_level
        elif char == ')':
            current_level = current_level.parent
        elif char in ['*', '+']:
            current_level.append_item(char)
        else:
            current_level.append_item(int(char))

    return top_level


with open('input.txt', 'r') as f:
    expression_strings = [
        line.split('\n')[0] for line in f.readlines()
    ]

# Part 1
expressions = [
    parse_expression_string(e) for e in expression_strings
]
values = [
    e.evaluate() for e in expressions
]
print(sum(values))

# Part 2
expressions = [
    parse_expression_string(e) for e in expression_strings
]
for e in expressions:
    e.add_parentheses_around_additions()

values = [
    e.evaluate() for e in expressions
]
print(sum(values))
