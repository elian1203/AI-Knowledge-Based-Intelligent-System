"""
AI Project 3
"""

from tkinter import *
from tkinter import filedialog, simpledialog

attributes_text_view = None
constraints_text_view = None
preferences_text_view = None

attributes_text = ""
constraints_text = ""
preferences_text = ""
preferences_type = ""


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
    window = Tk()
    window.title('AI Knowledge-Based Intelligent System')

    create_text_inputs()

    # keep window alive
    window.mainloop()


if __name__ == '__main__':
    create_gui()
