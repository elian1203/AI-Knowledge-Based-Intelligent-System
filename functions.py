from itertools import combinations
from math import comb
from random import randint
from tkinter import *
from xml.sax import parseString
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

    column = 1
    for a in attributes:
        label = Label(window, text=a.name, padx=10)
        label.grid(row=2, column=column)
        column += 1

    row = 3
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


def calculate_preferences(attributes, attribute_combinations, preferences_text, preferences_type):
    if preferences_type == 'Penalty':
        penalties = {}

        for preference in preferences_text.splitlines():
            constraint = preference.split(', ')[0]
            penalty = preference.split(', ')[1]
            constraint = model.Constraint(constraint)
            for attribute_combination in attribute_combinations:
                clasp = convert_combination_and_constraints_to_clasp(attribute_combination, attributes, [constraint])
                satisfied = clasp_wrapper.clasp(clasp)
                if not satisfied:
                    current_value = float(penalty)
                    if attribute_combination in penalties.keys():
                        current_value += penalties[attribute_combination]
                    penalties[attribute_combination] = current_value
        return penalties

    elif preferences_type == 'Possibilistic':
        penalties = {}

        for preference in preferences_text.splitlines():
            constraint = preference.split(', ')[0]
            penalty = preference.split(', ')[1]
            constraint = model.Constraint(constraint)
            for attribute_combination in attribute_combinations:
                clasp = convert_combination_and_constraints_to_clasp(attribute_combination, attributes, [constraint])
                satisfied = clasp_wrapper.clasp(clasp)
                current = 1
                if not satisfied:
                    current = 1 - float(penalty)
                in_penalties = 1
                if attribute_combination in penalties:
                    in_penalties = penalties[attribute_combination]
                if in_penalties > current:
                    penalties[attribute_combination] = current
        return penalties

    else:
        qualitative = {}
        for preference in preferences_text.splitlines():
            constraints = preference.split('IF')[0].strip()
            entry_constraint = preference.split('IF')[1].strip()
            entry_constraint = model.Constraint(entry_constraint)
            for attribute_combination in attribute_combinations:
                if entry_constraint.line != '':
                    clasp = convert_combination_and_constraints_to_clasp(attribute_combination, attributes, [entry_constraint])
                    satisfied = clasp_wrapper.clasp(clasp)
                else:
                    satisfied = True
                if satisfied:
                    order = 1
                    for constraint in constraints.split('BT'):
                        constraint = model.Constraint(constraint.strip())
                        clasp = convert_combination_and_constraints_to_clasp(attribute_combination, attributes, [constraint])
                        satisfied = clasp_wrapper.clasp(clasp)
                        if satisfied:
                            qualitative[(attribute_combination, preference)] = order 
                            break
                        else:
                            order += 1
                            qualitative[(attribute_combination, preference)] = 'INF'
                else:
                    qualitative[(attribute_combination, preference)] = 'INF'
        return qualitative


def exemplification(attributes_text, constraints_text, preferences_text, preferences_type):
    attributes = model.load_binary_attributes(attributes_text)
    attribute_combinations = model.generate_attribute_combinations(attributes)
    hard_constraints = model.load_hard_constraints(constraints_text)

    attribute_combinations = [c for c in attribute_combinations
                              if clasp_wrapper.clasp(
            convert_combination_and_constraints_to_clasp(c, attributes, hard_constraints))]
    preferences = calculate_preferences(attributes, attribute_combinations, preferences_text, preferences_type)

    n1 = randint(0, len(attribute_combinations) - 1)
    n2 = randint(0, len(attribute_combinations) - 1)
    c1 = attribute_combinations[n1]
    c2 = attribute_combinations[n2]
    if preferences_type == 'Penalty':
        p1 = preferences[c1]
        p2 = preferences[c2]
        p1text = p1
        p2text = p2

        if p1 > p2:
            outcometext = 'The second object is better'
        elif p1 < p2:
            outcometext = 'The first object is better'
        else:
            outcometext = 'The objects are equal'

    elif preferences_type == 'Possibilistic':
        p1text = 1
        p2text = 1
        if c1 in preferences:
            p1text = '%.1f' % preferences[c1]
        if c2 in preferences:
            p2text = '%.1f' % preferences[c2]

        if p1text < p2text:
            outcometext = 'The second object is better'
        elif p1text > p2text:
            outcometext = 'The first object is better'
        else:
            outcometext = 'The objects are equal'

    window = Toplevel()
    window.title('Exemplification Objects')
    title = Label(window, text='Exemplification Objects')
    title.grid(row=1, column=1, columnspan=len(attributes) + 1)

    column = 1
    for a in attributes:
        label = Label(window, text=a.name, padx=10)
        label.grid(row=2, column=column)

        column += 1

    if preferences_type == 'Penalty':
        label = Label(window, text='Total Penalty', padx=10)
        label.grid(row=2, column=column)
    elif preferences_type == 'Possibilistic':
        label = Label(window, text='TD', padx=10)
        label.grid(row=2, column=column)
    else:
        for preference in preferences_text.splitlines():
            label = Label(window, text = preference, padx=10)
            label.grid(row=2, column=column)  
            column += 1

    column = 1
    for value in model.convert_attribute_combination_to_values(c1):
        label = Label(window, text=value, padx=10)
        label.grid(row=3, column=column)
        column += 1

    if preferences_type == 'Qualitative':
        for preference in preferences_text.splitlines():
            label = Label(window, text = preferences[(c1, preference)], padx=10)
            label.grid(row=3, column=column)
            column += 1
    else:
        label = Label(window, text=p1text, padx=10)
        label.grid(row=3, column=column)

    column = 1
    for value in model.convert_attribute_combination_to_values(c2):
        label = Label(window, text=value, padx=10)
        label.grid(row=4, column=column)
        column += 1

    if preferences_type == 'Qualitative':
        for preference in preferences_text.splitlines():
            label = Label(window, text = preferences[(c2, preference)], padx=10)
            label.grid(row=4, column=column)
            column += 1

    else:
        label = Label(window, text=p2text, padx=10)
        label.grid(row=4, column=column)

    outcome = Label(window, text=outcometext)
    outcome.grid(row=5, column=1, columnspan=len(attributes) + 1)


def compare_qualitative(c1, p1, c2, p2):
    better = None
    
    for i in range(len(p1)):
        print('for')
        preference1, value1 = p1[i]
        preference2, value2 = p2[i]
        print(value1)
        print(value2)

        if value1 == 'INF' and value2 != 'INF':
            if better == p1:
                print('nc')
                return 'nc'
            better = p2
        elif value1 != 'INF' and value2 == 'INF':
            if better == p2:
                print('nc')
                return 'nc'
            better = p1
        elif value1 > value2:
            if better == p1:
                print('nc')
                return 'nc'
            better = p2
        elif value1 < value2:
            if better == p2:
                print('nc')
                return 'nc'
            better = p1
    if better == p1:
        print('better')
        return 'better'
    elif better == p2:
        print('worse')
        return 'worse'
    else:
        print('equal')
        return 'equal'


def optimization(attributes_text, constraints_text, preferences_text, preferences_type):
    attributes = model.load_binary_attributes(attributes_text)
    attribute_combinations = model.generate_attribute_combinations(attributes)
    hard_constraints = model.load_hard_constraints(constraints_text)

    attribute_combinations = [c for c in attribute_combinations
                              if clasp_wrapper.clasp(
            convert_combination_and_constraints_to_clasp(c, attributes, hard_constraints))]
    preferences = calculate_preferences(attributes, attribute_combinations, preferences_text, preferences_type)
    if preferences_type == 'Penalty':
        min = 1000000
        for combination in preferences:
            penalty = preferences[combination]
            if penalty <= min:
                min = penalty
                p1text = penalty
                c = combination
        
    elif preferences_type == 'Possibilistic':
        max = -1
        for combination in preferences:
            penalty = preferences[combination]
            if penalty >= max:
                max = penalty
                p1text = penalty
                c = combination
        
    else:
        d = {}
        for combination, preference in preferences:
            value = preferences[(combination, preference)]
            if combination in d:
                list = d[combination]
                list.append((preference, value))
            else:
                list = [(preference, value)]
            d[combination] = list
        best = None
        for c1 in d:
            if best is None:
                best = c1
            else:
                result = compare_qualitative(c1, d[c1], best, d[best])
                if result == 'better':
                    best = c1
        c = best


    window = Toplevel()
    window.title('Optimization Objects')
    title = Label(window, text='Optimization Objects')
    title.grid(row=1, column=1, columnspan=len(attributes)+1)

    column = 1
    for a in attributes:
        label = Label(window, text=a.name, padx=10)
        label.grid(row=2, column=column)
        column += 1

    if preferences_type == 'Penalty':
        label = Label(window, text='Total Penalty', padx=10)
        label.grid(row=2, column=column)
    elif preferences_type == 'Possibilistic':
        label = Label(window, text='TD', padx=10)
        label.grid(row=2, column=column)
    else:
        for preference in preferences_text.splitlines():
            label = Label(window, text = preference, padx=10)
            label.grid(row=2, column=column)  
            column += 1

    column = 1
    for value in model.convert_attribute_combination_to_values((c)):
        label = Label(window, text=value, padx=10)
        label.grid(row=3, column=column)
        column += 1

    if preferences_type == 'Qualitative':
        for preference in preferences_text.splitlines():
            label = Label(window, text = preferences[(c, preference)], padx=10)
            label.grid(row=3, column=column)
            column += 1
    else:
        label = Label(window, text=p1text, padx=10)
        label.grid(row=3, column=column)
    

def omni_optimization(attributes_text, constraints_text, preferences_text, preferences_type):
    attributes = model.load_binary_attributes(attributes_text)
    attribute_combinations = model.generate_attribute_combinations(attributes)
    hard_constraints = model.load_hard_constraints(constraints_text)

    attribute_combinations = [c for c in attribute_combinations
                              if clasp_wrapper.clasp(
            convert_combination_and_constraints_to_clasp(c, attributes, hard_constraints))]
    preferences = calculate_preferences(attributes, attribute_combinations, preferences_text, preferences_type)
    list = []
    if preferences_type == 'Penalty':
        min = 1000000
        for combination in preferences:
            penalty = preferences[combination]
            if penalty < min:
                list.clear()
                list.append(combination)
                min = penalty
                p1text = penalty
            elif penalty == min:
                list.append(combination)
        
    elif preferences_type == 'Possibilistic':
        max = -1
        for combination in preferences:
            penalty = preferences[combination]
            if penalty > max:
                list.clear()
                list.append(combination)
                max = penalty
                p1text = penalty
            elif penalty == max:
                list.append(combination)
        
    else:
        d = {}
        for combination, preference in preferences:
            value = preferences[(combination, preference)]
            if combination in d:
                list = d[combination]
                list.append((preference, value))
            else:
                list = [(preference, value)]
            d[combination] = list
        best = None
        list = []
        for c in d:
            list.append(c)
        for c1 in list:
            for c2 in list:
                if c1 == c2:
                    continue
                result = compare_qualitative(c1, d[c1], c2, d[c2])
                if result == 'better':
                    list.remove(c2)
        # for c1 in d:
        #     if len(list) == 0:
        #         list.append(c1)
        #     else:
        #         for compare in list:
        #             result = compare_qualitative(c1, d[c1], compare, d[compare])
        #             if result == 'better':
        #                 list.remove(compare)
        #                 list.append(c1)
        #             elif result == 'equal' or result == 'nc':
        #                 if c1 == compare:
        #                     continue
        #                 if result == 'nc':
        #                     print('nc')
        #                 list.append(c1)
    
    window = Toplevel()
    window.title('Omni-Optimization Objects')
    title = Label(window, text='Omni-Optimization Objects')
    title.grid(row=1, column=1, columnspan=len(attributes)+1)

    column = 1
    for a in attributes:
        label = Label(window, text=a.name, padx=10)
        label.grid(row=2, column=column)
        column += 1

    if preferences_type == 'Penalty':
        label = Label(window, text='Total Penalty', padx=10)
        label.grid(row=2, column=column)
    elif preferences_type == 'Possibilistic':
        label = Label(window, text='TD', padx=10)
        label.grid(row=2, column=column)
    else:
        for preference in preferences_text.splitlines():
            label = Label(window, text = preference, padx=10)
            label.grid(row=2, column=column)  
            column += 1

    row = 3
    for c in list:
        column = 1
        for value in model.convert_attribute_combination_to_values((c)):
            label = Label(window, text=value, padx=10)
            label.grid(row=row, column=column)
            column += 1
        if preferences_type == 'Qualitative':
            for preference in preferences_text.splitlines():
                label = Label(window, text = preferences[(c, preference)], padx=10)
                label.grid(row=row, column=column)
                column += 1
        else:
            label = Label(window, text=p1text, padx=10)
            label.grid(row=row, column=column)
        row +=1