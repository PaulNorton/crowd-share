#
# cstk
# Paul Norton
#

### Imports ###
from tkinter import *

### CSTk - Tk Class Extension ###
# Gives Tkinter window ability to enter or exit full screen when user presses 'f' or 'esc'
class CSTk(Tk):
    def __init__(self, master=None):
        Tk.__init__(self, master)

        # Bind key events to fullscreen
        self.bind('<f>', self.enter_fullscreen)
        self.bind('<Escape>', self.exit_fullscreen)
    
    # enter_fullscreen: go to fullscreen
    def enter_fullscreen(self, e):
        self.attributes('-fullscreen', True)
    
    # exit_fullscreen: go back to previous size
    def exit_fullscreen(self, e):
        self.attributes('-fullscreen', False)