#
# csframe
# Paul Norton
#

### Imports ###
from tkinter import *
from PIL import ImageTk, Image
import io
from modules.csclient import CSClient

### CSFrame - Frame Class Extension ###
# Handles the display of the CrowdShare app
class CSFrame(Frame):
    def __init__(self, master):
        Frame.__init__(self, master, bg='black')
        
        # Configure initial display
        self.columnconfigure(0,weight=1)
        self.rowconfigure(0,weight=1)

        self.original = Image.open('media/logo.jpg')
        self.image = ImageTk.PhotoImage(self.original)
        self.text = ''

        self.display = Canvas(self, bd=0, highlightthickness=0, bg='black', width=800, height=600)
        self.display.create_image(0, 0, image=self.image, anchor=CENTER, tags='IMG')
        self.display.grid(row=0, sticky=W+E+N+S)

        self.start_button = Label(self, text='Start!', fg='white', bg='black', font=('Helvetica', 24, 'bold'))
        self.start_button.bind('<Button-1>', self.start)
        self.start_button.grid(row=1, pady=20)

        self.pack(fill=BOTH, expand=1)
        
        # Binds window resizing to CrowdShare.resize_event
        self.bind('<Configure>', self.resize_event)
        
        # Start callback cycle
        # self.id = self.after(3000, self.callback)

    def start(self, e):
        self.start_button.grid_forget()
        self.client = CSClient()
        self.callback()

    # callback: main event, gets called every three seconds
    def callback(self):
        # Call various social media APIs
        self.client.search_media()
        
        # Rotate image
        image = self.client.get_next_image()

        if image['success']:
            # Set image and text and call resize
            self.original = Image.open(io.BytesIO(image['bytes']))
            self.image = ImageTk.PhotoImage(self.original)
            self.text = image['message']
            self.resize(self.display.winfo_width(), self.display.winfo_height())
        
        # Continue callback cycle
        self.id = self.after(3000, self.callback)

    # resize_event: called when window is resized
    def resize_event(self, event):
        # Pass values to resize method
        self.resize(event.width, event.height)

    # resize: changes image size to match size of window
    def resize(self, width, height):
        # Adjust for window margins
        width -= 40
        height -= 120
        
        # Calculate maximum size at the original aspect ratio
        if height/width > self.original.height/self.original.width:
            size = (width, int(width*self.original.height/self.original.width))
        else:
            size = (int(height*self.original.width/self.original.height), height)
            
        # Resize image and set up image and caption label
        resized = self.original.resize(size,Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(resized)
        self.display.delete('IMG')
        self.display.delete('TEXT')
        self.display.create_image(width/2+20, height/2+20, image=self.image, anchor=CENTER, tags='IMG')
        self.display.create_text(width/2+20, height+100, anchor=S, text=self.text, tags='TEXT', fill='white', font=("Helvetica", 18), width=width, justify=CENTER)
