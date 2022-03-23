from tkinter import *
import model


# the plan here will be to open another window with Toplevel() and provide the appropriate output after parsing the text
# the text for all of these will be parsed on-the-fly when each function is called
def feasible_objects(attributes_text, constraints_text, preferences_text, preferences_type):
    attributes = model.load_binary_attributes(attributes_text)
    # test attributes to make sure they are loading and converting to clasp correctly
    for a in attributes:
        print(a)
        print(model.convert_attribute_to_clasp((a, 'off')))
        print(model.convert_attribute_to_clasp((a, 'on')))
    hard_constraints = model.load_hard_constraints(constraints_text)
    # test attributes to make sure they are loading and converting to clasp correctly
    for c in hard_constraints:
        print(c)
        print(c.convert_to_clasp(attributes))

    attribute_combinations = model.generate_attribute_combinations(attributes)
    for combination in attribute_combinations:
        print(combination)
    pass


def exemplification(attributes_text, constraints_text, preferences_text, preferences_type):
    pass


def optimization(attributes_text, constraints_text, preferences_text, preferences_type):
    pass


def omni_optimization(attributes_text, constraints_text, preferences_text, preferences_type):
    pass
