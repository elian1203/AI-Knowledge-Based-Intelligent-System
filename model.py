import itertools


class BinaryAttribute:
    def __init__(self, name, off_value, on_value, attribute_number):
        self.name = name
        self.off_value = off_value
        self.on_value = on_value
        self.attribute_number = attribute_number

    def __str__(self):
        return 'Attribute: %s | %s : %s | %d' % (self.name, self.off_value, self.on_value, self.attribute_number)

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

    for c in attribute_combinations:
        # remove combinations where the same binary attribute shows up more than once
        if c[0][0] == c[1][0] or c[0][0] == c[2][0] or c[0][0] == c[3][0] \
                or c[1][0] == c[2][0] or c[1][0] == c[3][0] \
                or c[2][0] == c[3][0]:
            continue
        combinations_list.append((c, combination_number))
        combination_number += 1

    return combinations_list


def convert_attribute_to_clasp(attribute_combination):
    attribute, switch = attribute_combination
    clasp_string = ''
    if switch == 'off':
        clasp_string += '-'
    clasp_string += str(attribute.attribute_number) + ' 0\n'
    return clasp_string


def get_binary_attribute_from_value(attributes, value):
    for attribute in attributes:
        if attribute.off_value == value or attribute.on_value == value:
            return attribute
    # none found
    raise Exception('Invalid constraint specified! Attribute not found for value ' + value)


class Constraint:
    def __init__(self, line):
        self.line = line

    def __str__(self):
        return "Constraint: %s" % self.line

    def convert_to_clasp(self, attributes):
        clasp_string = ""
        for expr in self.line.split('AND'):
            for value in expr.strip().split('OR'):
                value = value.strip()

                negated = False
                if value.startswith('NOT'):
                    value = value[4:]
                    negated = True

                attribute = get_binary_attribute_from_value(attributes, value)

                if attribute.off_value == value:
                    negated = not negated

                if negated:
                    clasp_string += "-"
                clasp_string += str(attribute.attribute_number) + " "
            clasp_string += "0\n"
        return clasp_string


def load_hard_constraints(constraints_text):
    constraints = []

    for line in constraints_text.splitlines():
        constraints.append(Constraint(line))

    return constraints
