import itertools


class BinaryAttribute:
    def __init__(self, name, off_value, on_value):
        self.name = name
        self.off_value = off_value
        self.on_value = on_value

    @staticmethod
    def load_from_line(line):
        name = line.split(': ')[0]
        values = line.split(': ')[1]

        off_value = values.split(', ')[0]
        on_value = values.split(', ')[1]

        return BinaryAttribute(name, off_value, on_value)


def load_binary_attributes(attributes_text):
    attributes = []

    for line in attributes_text.split('\n'):
        attributes.append(BinaryAttribute.load_from_line(line))

    return attributes


def generate_attribute_combinations(attributes):
    distinct_attributes = []

    # generate distinct attributes
    for attribute in attributes:
        distinct_attributes.append((attribute, 'off'))
        distinct_attributes.append((attribute, 'on'))

    attribute_combinations = itertools.combinations(distinct_attributes, len(attributes))

    combinations_list = []
    combination_number = 1

    for combination in attribute_combinations:
        combinations_list.append((combination, combination_number))
        combination_number += 1

    return combinations_list
