from tkinter import *
import model
import clasp_wrapper


def convert_combination_and_constraints_to_clasp(attribute_combination, attributes, constraints):
    clasp_string = 'p cnf %d %d\n' % (len(attribute_combination[0]), len(attribute_combination[0]) + len(constraints))
    clasp_string += model.convert_attribute_combination_to_clasp(attribute_combination)
    for constraint in constraints:
        clasp_string += constraint.convert_to_clasp(attributes)
    return clasp_string


# the plan here will be to open another window with Toplevel() and provide the appropriate output after parsing the text
# the text for all of these will be parsed on-the-fly when each function is called
def feasible_objects(attributes_text, constraints_text, preferences_text, preferences_type):
    attributes = model.load_binary_attributes(attributes_text)
    attribute_combinations = model.generate_attribute_combinations(attributes)
    hard_constraints = model.load_hard_constraints(constraints_text)

    attribute_combinations = [c for c in attribute_combinations
                              if clasp_wrapper.clasp(
            convert_combination_and_constraints_to_clasp(c, attributes, hard_constraints))]
    # objects = ""
    # for c in attribute_combinations:
    #     objects += " ".join(model.convert_attribute_combination_to_values(c)) + "\n"

    window = Toplevel()
    window.title('Feasible Objects')
    title = Label(window, text='Feasible Objects')
    title.grid(row=1, column=1, columnspan=len(attributes))

    row = 2
    for c in attribute_combinations:
        column = 1
        for value in model.convert_attribute_combination_to_values(c):
            label = Label(window, text=value, padx=10)
            label.grid(row=row, column=column)
            column += 1
        row += 1

    # view = Text(window)
    # view.bind("<Key>", lambda e: "break")
    # view.insert(END, objects)
    # view.grid(row=2, column=1)
    window.mainloop()


def exemplification(attributes_text, constraints_text, preferences_text, preferences_type):
    attributes = model.load_binary_attributes(attributes_text)
    # test attributes to make sure they are loading and converting to clasp correctly
    for a in attributes:
        print(a)
        print(model.convert_attribute_to_clasp((a, 'off')), end='')
        print(model.convert_attribute_to_clasp((a, 'on')), end='')
    hard_constraints = model.load_hard_constraints(constraints_text)
    # test constraints to make sure they are loading and converting to clasp correctly
    for c in hard_constraints:
        print(c)
        print(c.convert_to_clasp(attributes), end='')

    attribute_combinations = model.generate_attribute_combinations(attributes)
    # test combinations to make sure they are correct
    for combination in attribute_combinations:
        print(combination)
        print(model.convert_attribute_combination_to_clasp(combination), end='')


def optimization(attributes_text, constraints_text, preferences_text, preferences_type):
    pass


def omni_optimization(attributes_text, constraints_text, preferences_text, preferences_type):
    pass
