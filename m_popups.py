# creating some importable popups for things

from tkinter import *
from tkinter.messagebox import showinfo

class JoiningPopup(object):
    def __init__(self, master):
        self.top = Toplevel(master)
        self.create_widgets()

    def create_widgets(self):
        """ creating the pop up widgets """
        # create an instruction label
        Label(self.top,
              text = "Choose a joining method"
              ).grid(row = 0, column = 0, sticky = W)

        # create a variable to hold the chosen joining method
        self.chosen_method = StringVar()
        self.chosen_method.set(None)

        #  create the radio buttons for the joining methods
        joining_methods = ["welding", "gluing", "sticky tape", "blu tac"]
        row = 1
        for method in joining_methods:
            Radiobutton(self.top,
                        text = method,
                        variable = self.chosen_method,
                        value = method
                        ).grid(row = row, column = 0, sticky = W)
            row += 1

        # create a submit button
        Button(self.top,
               text = "Submit Choice",
               command = self.cleanup,
               ).grid(row = len(joining_methods)+1, column = 0, sticky = W)

    def cleanup(self):
        self.return_value = self.chosen_method.get()
        self.top.destroy()
        
class ExportPopup(object):
    def __init__(self, master):
        self.top = Toplevel(master)
        self.create_widgets()

    def create_widgets(self):
        """ Creating pop up widgets """
        Label(self.top,
              text = "Are you ready to save and export?"
              ).grid(row = 0, column=0, columnspan = 2, sticky = W)

        Button(self.top,
               text = "Yes",
               command = self.cleanup_yes,
               ).grid(row = 1, column = 0, sticky = W)

        Button(self.top,
               text = "No",
               command = self.cleanup_no
               ).grid(row = 1, column = 1, sticky = W)

    def cleanup_yes(self):
        self.answer = True
        self.top.destroy()

    def cleanup_no(self):
        self.answer = False
        self.top.destroy()

class SavePopup(object):
    def __init__(self, master):
        """ creates the pop up """
        self.top = Toplevel(master)
        self.create_widgets()

    def create_widgets(self):
        """ creates the widgets """
        Label(self.top,
              text = "Enter a filename to save"
              ).grid(row=0, column=0, sticky=W)

        self.filename_entry = Entry(self.top)
        self.filename_entry.grid(row=1, column=0, sticky=W)

        Button(self.top,
               text="Save",
               command=self.cleanup
               ).grid(row=2, column=0)

    def cleanup(self):
        self.filename = self.filename_entry.get()
        self.top.destroy()

def export_error():
    showinfo("Error!", "The current assembly is not ready to export")
