"""
AI Project 3
"""

from tkinter import *
from tkinter import filedialog, simpledialog

root = None

attributes_text_view = None
constraints_text_view = None
preferences_text_view = None

attributes_text = ""
constraints_text = ""
preferences_text = ""
preferences_type = ""


class Choices:

    def __init__(self, parent, choicelist):
        Label(parent, text="Select an item:").grid(row=0, column=0, sticky="W")

        self.var = StringVar()
        self.var.set('No data')  # default option
        popupMenu = OptionMenu(parent, self.var, *choicelist)
        popupMenu.grid(sticky=N + S + E + W, row=1, column=0)

        Button(parent, text='Done', command=self.buttonfn).grid(row=2, column=0)

    def buttonfn(self):
        print(self.var.get())


def set_preferences_type(type, popup):
    global preferences_type, preferences_text
    preferences_type = type

    if preferences_type == '':
        return

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
    filename = filedialog.askopenfile(title="Select %s file" % filetype, filetypes=(("Text files",
                                                                                     "*.txt*"),
                                                                                    ("All files",
                                                                                     "*.*")))
    if filename is None:
        return

    file = open(filename.name)

    if filetype == 'attributes':
        global attributes_text
        attributes_text = file.read()
        attributes_text_view.delete(1.0, END)
        attributes_text_view.insert(END, attributes_text)
    elif filetype == 'constraints':
        global constraints_text
        constraints_text = file.read()
        constraints_text_view.delete(1.0, END)
        constraints_text_view.insert(END, constraints_text)
    elif filetype == 'preferences':
        global preferences_text
        preferences_text = file.read()
        preferences_text_view.delete(1.0, END)
        preferences_text_view.insert(END, preferences_text)
        get_preferences_type()

    file.close()


def manual_entry(filetype):
    text = simpledialog.askstring(title="Manually enter %s" % filetype,
                                  prompt="Please paste or type the %s text." % filetype)

    if text is None:
        return

    if filetype == 'attributes':
        global attributes_text, attributes_text_view
        attributes_text = text
        attributes_text_view.delete(1.0, END)
        attributes_text_view.insert(END, attributes_text)
    elif filetype == 'constraints':
        global constraints_text
        constraints_text = text
        constraints_text_view.delete(1.0, END)
        constraints_text_view.insert(END, constraints_text)
    elif filetype == 'preferences':
        global preferences_text
        preferences_text = text
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


def create_gui():
    global root
    root = Tk()
    root.title('AI Knowledge-Based Intelligent System')

    create_text_inputs()

    # keep window alive
    root.mainloop()


if __name__ == '__main__':
    create_gui()
