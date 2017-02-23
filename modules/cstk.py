#
# cstk
# Paul Norton
#

### Imports ###
from tkinter import *
from modules.csframe import CSFrame
from modules.cssettingswindow import CSSettingsWindow

### CSTk - Tk Class Extension ###
# Gives Tkinter window ability to enter or exit full screen when user presses 'f' or 'esc'
class CSTk(Tk):
    def __init__(self, master=None):
        Tk.__init__(self, master)

        self.frame = CSFrame(self)

        menu = Menu(self)
        filemenu = Menu(menu, tearoff=0)
        filemenu.add_command(label="Preferences", command=self.open_settings_window)
        menu.add_cascade(label="File", menu=filemenu)
        self.config(menu=menu)

        try:
            file = open('config.json', 'r')
            file.close()
        except:
            self.open_settings_window()

        # Bind key events to fullscreen
        self.bind('<f>', self.enter_fullscreen)
        self.bind('<Escape>', self.exit_fullscreen)

        self.frame.mainloop()
    
    # enter_fullscreen: go to fullscreen
    def enter_fullscreen(self, e):
        self.attributes('-fullscreen', True)
    
    # exit_fullscreen: go back to previous size
    def exit_fullscreen(self, e):
        self.attributes('-fullscreen', False)

    def open_settings_window(self):
        window = CSSettingsWindow(self)