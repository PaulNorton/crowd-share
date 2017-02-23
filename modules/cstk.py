#
# cstk
# Paul Norton
#

### Imports ###
from tkinter import *
import pickle
from modules.csframe import CSFrame
from modules.cssettingswindow import CSSettingsWindow

### CSTk - Tk Class Extension ###
# Gives Tkinter window ability to enter or exit full screen when user presses 'f' or 'esc'
class CSTk(Tk):
    def __init__(self, master=None):
        Tk.__init__(self, master)

        self.title('CrowdShare')

        self.frame = CSFrame(self)

        menu = Menu(self)

        filemenu = Menu(menu, tearoff=False)
        filemenu.add_command(label="Preferences", command=self.open_settings_window, accelerator="Command-.")
        menu.add_cascade(label="File", menu=filemenu)

        self.config(menu=menu)

        try:
            open( "config.p", "rb" )
        except:
            self.open_settings_window()

        # Bind key events to settings window
        self.bind('<Command-.>', self.open_settings_window)

        self.frame.mainloop()
    
    def open_settings_window(self, e=None):
        self.settings_window = CSSettingsWindow(self)
