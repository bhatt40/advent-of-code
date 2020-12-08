from collections import Counter


def get_image_layers(image, height, width):
    layer_size = height * width
    return [
        image[i:i + layer_size] for i in range(0, len(image), layer_size)
    ]


def render_image(layers):
    aggregated_layers = list(zip(*layers))
    return [
        determine_pixel_value(layer_values) for layer_values in aggregated_layers
    ]


def determine_pixel_value(layer_values):
    return list(filter(lambda x: x != 2, layer_values))[0]


def print_image(image, height, width):
    line_number = 0
    while line_number < height:
        line_first_pixel_index = line_number * width
        line = ''.join(
            [
                '{} '.format(pixel_value)
                for pixel_value in image[line_first_pixel_index: line_first_pixel_index + width]
            ]
        )
        print(line)
        line_number += 1


with open('input.txt', 'r') as f:
    nums = f.readline().split('\n')[0]
    image = [
        int(x) for x in nums
    ]


IMAGE_HEIGHT = 6
IMAGE_WIDTH = 25

layers = get_image_layers(image, IMAGE_HEIGHT, IMAGE_WIDTH)

# Part 1
layer_counters = [
    Counter(layer) for layer in layers
]
layer_number_of_zeroes = [
    layer_counter[0] for layer_counter in layer_counters
]
val, index = min((val, index) for (index, val) in enumerate(layer_number_of_zeroes))

counter = layer_counters[index]
print(counter[1] * counter[2])

# Part 2
rendered_image = render_image(layers)
print_image(rendered_image, IMAGE_HEIGHT, IMAGE_WIDTH)
