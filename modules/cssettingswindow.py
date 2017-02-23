#
# cssettingswindow
# Paul Norton
#

### Imports ###
from tkinter import *
import io

### CSSettingsWindow - Toplevel Class Extension ###
# Handles the settings of the CrowdShare app
class CSSettingsWindow(Toplevel):
    def __init__(self, master):
        Toplevel.__init__(self, master)

        self.frame = Frame(self, bg='black', width=800, height=600)
        self.frame.pack(fill=BOTH, expand=1)
