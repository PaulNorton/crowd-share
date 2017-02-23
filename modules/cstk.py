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
        self.fullscreen = False

        menu = Menu(self)

        filemenu = Menu(menu, tearoff=False)
        filemenu.add_command(label="Preferences", command=self.open_settings_window, accelerator="Command-.")
        menu.add_cascade(label="File", menu=filemenu)

        self.viewmenu = Menu(menu, tearoff=0)
        self.fs_cmd = self.viewmenu.add_command(label="Enter Full Screen", command=self.toggle_fullscreen, accelerator="Control-Command-f")
        menu.add_cascade(label="View", menu=self.viewmenu)

        self.config(menu=menu)

        try:
            open( "config.p", "rb" )
        except:
            self.open_settings_window()

        # Bind key events to fullscreen
        self.bind('<Command-Control-f>', self.toggle_fullscreen)
        self.bind('<Command-.>', self.open_settings_window)
        self.frame.mainloop()
    
    # enter_fullscreen: go to fullscreen
    def toggle_fullscreen(self, e=None):
        if self.fullscreen:
            self.fullscreen = False
            self.attributes('-fullscreen', False)
            self.viewmenu.entryconfigure(1, label='Enter Full Screen')
        else:
            self.fullscreen = True
            self.attributes('-fullscreen', True)
            self.viewmenu.entryconfigure(1, label='Exit Full Screen')
    
    # exit_fullscreen: go back to previous size
    def exit_fullscreen(self, e):
        self.attributes('-fullscreen', False)

    def open_settings_window(self, e=None):
        self.settings_window = CSSettingsWindow(self)
