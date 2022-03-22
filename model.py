import itertools


class BinaryAttribute:
    def __init__(self, name, off_value, on_value, attribute_number):
        self.name = name
        self.off_value = off_value
        self.on_value = on_value
        self.attribute_number = attribute_number

    @staticmethod
    def load_from_line(line, line_number):
        name = line.split(': ')[0]
        values = line.split(': ')[1]

        off_value = values.split(', ')[0]
        on_value = values.split(', ')[1]

        return BinaryAttribute(name, off_value, on_value, line_number)


def load_binary_attributes(attributes_text):
    attributes = []

    line_number = 1
    for line in attributes_text.splitlines():
        attributes.append(BinaryAttribute.load_from_line(line, line_number))
        line_number += 1

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


def convert_attribute_to_clasp(attribute_combination):
    attribute, switch = attribute_combination
    clasp_string = ''
    if switch == 'off':
        clasp_string += '-'
    clasp_string += attribute.attribute_number + ' 0\n'


def get_binary_attribute_from_value(attributes, value):
    for attribute in attributes:
        if attribute.off_value == value or attribute.on_value == value:
            return attribute
    # none found
    raise Exception('Invalid constraint specified! Attribute not found for value ' + value)


class HardConstraint:
    def __init__(self, line):
        self.line = line

    def convert_to_clasp(self, attributes):
        clasp_string = ""
        for value in self.line.split('OR'):
            value = value.trim()

            negated = False
            if value.startswith('NOT'):
                value = value[4:]
                negated = True

            attribute = get_binary_attribute_from_value(attributes, value)

            if attribute.off_value:
                negated = not negated

            if negated:
                clasp_string += "-"
            clasp_string += attribute.attribute_number + " "
        clasp_string += "0\n"


def load_hard_constraints(constraints_text):
    constraints = []

    for line in constraints_text.splitlines():
        constraints.append(HardConstraint(line))

    return constraints
