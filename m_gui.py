# Writing the UI buttons

from tkinter import *

# this is part of the popup code, but i dont think we actually need it
import sys

# import popups
import m_popups

class Application(Frame):
    """ A GUI application with threee buttons """

    def __init__(self, master):
        """ Initialise the frame """
        super(Application, self).__init__(master)
        self.grid()
        self.widgets = []
        
        self.create_widgets()        

        self.output_text = []

        # component variables
        self.add_comp_b = False
        self.add_comp_g = False
        self.add_comp_p = False
        self.add_comp_r = False
        self.add_comp_y = False

        # delete variable
        self.delete = False

        # rotation variables
        self.rot_y_pos = False
        self.rot_y_neg = False

        self.rot_x_pos = False
        self.rot_x_neg = False

        self.rot_z_pos = False
        self.rot_z_neg = False

        self.mov_z_pos = False
        self.mov_z_neg = False

        # Export handling
        self.wants_to_export = False

    def create_widgets(self):
        """ Adds all the buttons to the user interface """
        # buttons to add components
        self.bttn_b = Button(self, text = "Blue Component", command = self.add_comp_b)
        self.bttn_b.grid(row=0, column=0, sticky=W)
        self.widgets.append(self.bttn_b)
        
        self.bttn_g = Button(self, text = "Green Component", command = self.add_comp_g)
        self.bttn_g.grid(row=1, column=0, sticky=W)
        self.widgets.append(self.bttn_g)
        
        self.bttn_p = Button(self, text = "Pink Component", command = self.add_comp_p)
        self.bttn_p.grid(row=2, column=0, sticky=W)
        self.widgets.append(self.bttn_p)
        
        self.bttn_r = Button(self, text = "Red Component", command = self.add_comp_r)
        self.bttn_r.grid(row=3, column=0, sticky=W)
        self.widgets.append(self.bttn_r)
        
        self.bttn_y = Button(self, text = "Yellow Component", command = self.add_comp_y)
        self.bttn_y.grid(row=4, column=0, sticky=W)
        self.widgets.append(self.bttn_y)

        # buttons to delete component
        self.bttn_delete = Button(self, text = "Delete", command = self.delete_comp)
        self.bttn_delete.grid(row=4, column=2, sticky=W)
        self.widgets.append(self.bttn_delete)

        # buttons to control camera rotation
        # y rotation
        self.bttn_rot_y_pos = Button(self, text = "Rotate Y clockwise", command = self.rot_y_pos)
        self.bttn_rot_y_pos.grid(row=1, column=2, sticky=W)
        self.widgets.append(self.bttn_rot_y_pos)

        self.bttn_rot_y_neg = Button(self, text = "Rotate Y anti-clockwise", command = self.rot_y_neg)
        self.bttn_rot_y_neg.grid(row=1, column=3, sticky=W)
        self.widgets.append(self.bttn_rot_y_neg)

        # x rotation
        self.bttn_rot_x_neg = Button(self, text = "Rotate X anti-clockwise", command = self.rot_x_neg)
        self.bttn_rot_x_neg.grid(row=0, column=3, sticky=W)
        self.widgets.append(self.bttn_rot_x_neg)

        self.bttn_rot_x_pos = Button(self, text = "Rotate X clockwise", command = self.rot_x_pos)
        self.bttn_rot_x_pos.grid(row=0, column=2, sticky=W)
        self.widgets.append(self.bttn_rot_x_pos)

        # z rotation
        self.bttn_rot_z_pos = Button(self, text = "Rotate Z anti-clockwise", command = self.rot_z_pos)
        self.bttn_rot_z_pos.grid(row=2, column=2, sticky=W)
        self.widgets.append(self.bttn_rot_z_pos)

        self.bttn_rot_z_neg = Button(self, text = "Rotate Z clockwise", command = self.rot_z_neg)
        self.bttn_rot_z_neg.grid(row=2, column=3, sticky=W)
        self.widgets.append(self.bttn_rot_z_neg)

        # z movement
        self.bttn_mov_z_pos = Button(self, text = "Zoom In", command = self.mov_z_pos)
        self.bttn_mov_z_pos.grid(row=3, column=2, sticky=W)
        self.widgets.append(self.bttn_mov_z_pos)

        self.bttn_mov_z_neg = Button(self, text = "Zoom Out", command = self.mov_z_neg)
        self.bttn_mov_z_neg.grid(row=3, column=3, sticky=W)
        self.widgets.append(self.bttn_mov_z_neg)

        # Text display
        self.text_display = Text(self, width=35, height=20, wrap=WORD)
        self.text_display.grid(row=0, column=1, rowspan=5, sticky=W)

        # Export button
        self.bttn_export = Button(self, text = "Export", command = self.export)
        self.bttn_export.grid(row=4, column=3, sticky=W)
        self.widgets.append(self.bttn_export)
        

    # Adding components
    def add_comp_b(self):
        """ add a blue component """
        #self.update_text("Adding blue component")
        self.add_comp_b = True

    def add_comp_g(self):
        """ add a green component """
        #self.update_text("Adding green component")
        self.add_comp_g = True

    def add_comp_p(self):
        """ add a pink component """
        #self.update_text("Adding pink component")
        self.add_comp_p = True

    def add_comp_r(self):
        """ add a red component """
        #self.update_text("Adding red component")
        self.add_comp_r = True

    def add_comp_y(self):
        """ add a yellow component """
        #self.update_text("Adding yellow component")
        self.add_comp_y = True

    # deleting components
    def delete_comp(self):
        """ delete a component """
        #self.update_text("deleting component")
        self.delete = True

    # camera rotation
    def rot_y_pos(self):
        """ rotate clockwise about the y axis """
        #self.update_text("rotating y+")
        self.rot_y_pos = True

    def rot_y_neg(self):
        """ rotate anti-clockwise about the y axis """
        #self.update_text("rotating y-")
        self.rot_y_neg = True

    def rot_x_neg(self):
        """ rotate anti-clockwise about the x axis """
        #self.update_text("rotating x-")
        self.rot_x_neg = True

    def rot_x_pos(self):
        """ rotate clockwise about the x axis """
        #self.update_text("rotating x+")
        self.rot_x_pos = True

    def rot_z_neg(self):
        """ rotate clockwise about the z axis """
        #self.update_text("rotating z-")
        self.rot_z_neg = True

    def rot_z_pos(self):
        """ rotate anti-clockwise about the z axis """
        #self.update_text("rotating z+")
        self.rot_z_pos = True

    # camera movement
    def mov_z_neg(self):
        """ moves in outward z, zooms out """
        #self.update_text("zoom out")
        self.mov_z_neg = True

    def mov_z_pos(self):
        """ moves in inward z, zooms in"""
        #self.update_text("zoom in")
        self.mov_z_pos = True

    def export(self):
        """ exports the final design """
        self.update_text("exporting")
        self.wants_to_export = True

    def update_text(self, message):
        """ prints out the display text """
        self.output_text.append(message)
        if len(self.output_text) > 20:
            del self.output_text[0]
        output = ""
        for line in self.output_text:
            output += line
            output += "\n"

        self.text_display.delete(0.0, END)
        self.text_display.insert(0.0, output)

    def create_joining_popup(self):
        """ birth a pop up to choose the joining method """
        window = m_popups.JoiningPopup(self)
        for widget in self.widgets:
            widget["state"] = "disabled"
        self.wait_window(window.top)
        for widget in self.widgets:
            widget["state"] = "normal"
        return window.return_value

    def create_export_popup(self):
        """ allow the user to choose whether to exit or not """
        window = m_popups.ExportPopup(self)
        for widget in self.widgets:
            widget["state"] = "disabled"
        self.wait_window(window.top)
        for widget in self.widgets:
            widget["state"] = "normal"
        return window.answer

    def create_save_popup(self):
        """ create a popup to get a file name """
        window = m_popups.SavePopup(self)
        for widget in self.widgets:
            widget["state"] = "disabled"
        self.wait_window(window.top)
        for widget in self.widgets:
            widget["state"] = "normal"
        return window.filename

    def export_error_popup(self):
        m_popups.export_error()

# main
##root = Tk()
##root.title("Assembly Design Interface")
##root.geometry("700x400")
##
##app = Application(root)
##root.mainloop()


