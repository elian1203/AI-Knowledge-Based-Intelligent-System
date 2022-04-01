"""
AI Project 3
"""

from tkinter import *
from tkinter import filedialog, simpledialog

import functions

root = None

attributes_text_view = None
constraints_text_view = None
preferences_text_view = None

attributes_text = ""
constraints_text = ""
preferences_text = ""
preferences_type = ""


def set_preferences_type(type, popup):
    global preferences_type, preferences_text
    preferences_type = type

    if preferences_type == '':
        return
    functions.load_all(attributes_text, constraints_text, preferences_text, preferences_type)

    global root
    popup.destroy()
    root.deiconify()


def get_preferences_type():
    popup = Toplevel()
    popup.title('Preferences Type')

    choice_list = ['Penalty', 'Possibilistic', 'Qualitative']

    Label(popup, text="Select preference type:").grid(row=0, column=0)

    type = StringVar()
    type.set('')

    menu = OptionMenu(popup, type, *choice_list)
    menu.config(width=15)
    menu.grid(row=1, column=0, columnspan=4)

    Button(popup, text='Done', command=lambda: set_preferences_type(type.get(), popup)).grid(row=2)

    global root
    root.withdraw()
    popup.mainloop()


def browse_files(filetype):
    global attributes_text, constraints_text, preferences_text
    filename = filedialog.askopenfile(title="Select %s file" % filetype, filetypes=(("Text files",
                                                                                     "*.txt"),
                                                                                    ("All files",
                                                                                     "*.*")))
    if filename is None:
        return

    file = open(filename.name)

    if filetype == 'attributes':
        attributes_text = file.read()
        functions.load_all(attributes_text, constraints_text, preferences_text, preferences_type)
        attributes_text_view.delete(1.0, END)
        attributes_text_view.insert(END, attributes_text)
    elif filetype == 'constraints':
        constraints_text = file.read()
        functions.load_all(attributes_text, constraints_text, preferences_text, preferences_type)
        constraints_text_view.delete(1.0, END)
        constraints_text_view.insert(END, constraints_text)
    elif filetype == 'preferences':
        preferences_text = file.read()
        # functions.load_all(attributes_text, constraints_text, preferences_text, preferences_type)
        preferences_text_view.delete(1.0, END)
        preferences_text_view.insert(END, preferences_text)
        get_preferences_type()

    file.close()


def manual_entry(filetype):
    global attributes_text, attributes_text_view, constraints_text, constraints_text_view, preferences_text, preferences_text_view
    text = simpledialog.askstring(title="Manually enter %s" % filetype,
                                  prompt="Please paste or type the %s text." % filetype)

    if text is None:
        return

    if filetype == 'attributes':
        attributes_text = text
        functions.load_all(attributes_text, constraints_text, preferences_text, preferences_type)
        attributes_text_view.delete(1.0, END)
        attributes_text_view.insert(END, attributes_text)
    elif filetype == 'constraints':
        constraints_text = text
        functions.load_all(attributes_text, constraints_text, preferences_text, preferences_type)
        constraints_text_view.delete(1.0, END)
        constraints_text_view.insert(END, constraints_text)
    elif filetype == 'preferences':
        preferences_text = text
        # functions.load_all(attributes_text, constraints_text, preferences_text, preferences_type)
        preferences_text_view.delete(1.0, END)
        preferences_text_view.insert(END, preferences_text)
        get_preferences_type()


def create_text_inputs():
    attributes_label = Label(text='Attributes Entry')
    attributes_file = Button(text='Upload File', command=lambda: browse_files('attributes'))
    attributes_entry = Button(text='Manual Entry', command=lambda: manual_entry('attributes'))
    global attributes_text_view
    attributes_text_view = Text(height=5, width=60)
    # make text box read only
    attributes_text_view.bind("<Key>", lambda e: "break")

    attributes_label.grid(column=1, columnspan=2, row=1)
    attributes_file.grid(column=1, row=2)
    attributes_entry.grid(column=2, row=2)
    attributes_text_view.grid(column=3, row=1, columnspan=2, rowspan=2, pady=5)

    constraints_label = Label(text='Constraints Entry')
    constraints_file = Button(text='Upload File', command=lambda: browse_files('constraints'))
    constraints_entry = Button(text='Manual Entry', command=lambda: manual_entry('constraints'))
    global constraints_text_view
    constraints_text_view = Text(height=5, width=60)
    # make text box read only
    constraints_text_view.bind("<Key>", lambda e: "break")

    # shift the row down by 2 from the above
    constraints_label.grid(column=1, columnspan=2, row=3)
    constraints_file.grid(column=1, row=4)
    constraints_entry.grid(column=2, row=4)
    constraints_text_view.grid(column=3, row=3, columnspan=2, rowspan=2, pady=5)

    preferences_label = Label(text='Preferences Entry')
    preferences_file = Button(text='Upload File', command=lambda: browse_files('preferences'))
    preferences_entry = Button(text='Manual Entry', command=lambda: manual_entry('preferences'))
    global preferences_text_view
    preferences_text_view = Text(height=5, width=60)
    # make text box read only
    preferences_text_view.bind("<Key>", lambda e: "break")

    # shift the row down by 2 from the above
    preferences_label.grid(column=1, columnspan=2, row=5)
    preferences_file.grid(column=1, row=6)
    preferences_entry.grid(column=2, row=6)
    preferences_text_view.grid(column=3, row=5, columnspan=2, rowspan=2, pady=5)


def create_function_buttons():
    feasible_objects = Button(text='Feasible Objects',
                              command=lambda: functions.feasible_objects(attributes_text, constraints_text,
                                                                         preferences_text, preferences_type))
    exemplification = Button(text='Exemplification',
                             command=lambda: functions.exemplification(attributes_text, constraints_text,
                                                                       preferences_text, preferences_type))
    optimization = Button(text='Optimization',
                          command=lambda: functions.optimization(attributes_text, constraints_text,
                                                                 preferences_text, preferences_type))
    omni_optimization = Button(text='Omni-Optimization',
                               command=lambda: functions.omni_optimization(attributes_text, constraints_text,
                                                                           preferences_text, preferences_type))

    feasible_objects.grid(column=1, row=7, pady=5, padx=5)
    feasible_objects.config(width=15)
    exemplification.grid(column=2, row=7, pady=5, padx=5)
    exemplification.config(width=15)
    optimization.grid(column=1, row=8, pady=5, padx=5)
    optimization.config(width=15)
    omni_optimization.grid(column=2, row=8, pady=5, padx=5)
    omni_optimization.config(width=15)


def create_gui():
    global root
    root = Tk()
    root.title('AI Knowledge-Based Intelligent System')

    create_text_inputs()
    create_function_buttons()

    # keep window alive
    root.mainloop()


if __name__ == '__main__':
    create_gui()
