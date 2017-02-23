#
# cssettingswindow
# Paul Norton
#

### Imports ###
from tkinter import *
import pickle
from modules.csinstagram import CSInstagram

### CSSettingsWindow - Toplevel Class Extension ###
# Handles the settings of the CrowdShare app
class CSSettingsWindow(Toplevel):
    def __init__(self, master):
        Toplevel.__init__(self, master)

        self.title('Preferences')

        self.lift(master)

        try:
            config = pickle.load( open( "config.p", "rb" ) )
        except:
            config = {
                    'app_key': '',
                    'app_secret': '',
                    'oauth_token': '',
                    'oauth_token_secret': '',
                    'client_id': '',
                    'client_secret' : '',
                    'access_token': '',
                    'hashtag': '',
                    'aws_access_key_id': '',
                    'aws_secret_access_key': ''
            }

        self.frame = Frame(self)
        self.frame.pack(fill=BOTH, expand=1, padx=20, pady=20)

        self.row = 0
        self.instagram = CSInstagram("")

        # Twitter
        twitter_title = CSTitle(self.frame, 'Twitter', self.next_row())

        self.app_key = CSEntry(self.frame, 'Consumer Key', config['app_key'], self.next_row())
        self.app_secret = CSEntry(self.frame, 'Consumer Secret', config['app_secret'], self.next_row())
        self.oauth_token = CSEntry(self.frame, 'Access Token', config['oauth_token'], self.next_row())
        self.oauth_token_secret = CSEntry(self.frame, 'Access Token Secret', config['oauth_token_secret'], self.next_row())

        sep1 = CSSeparator(self.frame, self.next_row())

        # Instagram
        instagram_title = CSTitle(self.frame, 'Instagram', self.next_row())

        self.client_id = CSEntry(self.frame, 'Client ID', config['client_id'], self.next_row())
        self.client_secret = CSEntry(self.frame, 'Client Secret', config['client_secret'], self.next_row(), "Generate URL", self.generate_url)
        self.url = CSEntry(self.frame, 'URL', '', self.next_row())
        self.code = CSEntry(self.frame, 'Code', '', self.next_row(), "Get access token", self.get_access_token)
        self.access_token = CSEntry(self.frame, 'Access Token', config['access_token'], self.next_row())

        sep2 = CSSeparator(self.frame, self.next_row())

        # AWS
        aws_title = CSTitle(self.frame, 'Amazon Web Services', self.next_row())

        self.aws_access_key_id = CSEntry(self.frame, 'Access Key ID', config['aws_access_key_id'], self.next_row())
        self.aws_secret_access_key = CSEntry(self.frame, 'Secret Access Key', config['aws_secret_access_key'], self.next_row())

        sep3 = CSSeparator(self.frame, self.next_row())

        # Hashtag
        hashtag_title = CSTitle(self.frame, 'Event Hashtag', self.next_row())

        self.hashtag = CSEntry(self.frame, 'Hashtag', config['hashtag'], self.next_row())

        sep4 = CSSeparator(self.frame, self.next_row())

        apply_button = Button(self.frame, text="Apply", command=self.apply)
        apply_button.grid(row=self.next_row(), columnspan=2, sticky=E)

    def next_row(self):
        self.row += 1
        return self.row

    def apply(self):
        data = {
                'app_key': self.app_key.entry.get(),
                'app_secret': self.app_secret.entry.get(),
                'oauth_token': self.oauth_token.entry.get(),
                'oauth_token_secret': self.oauth_token_secret.entry.get(),
                'client_id': self.client_id.entry.get(),
                'client_secret' : self.client_secret.entry.get(),
                'access_token': self.access_token.entry.get(),
                'hashtag': self.hashtag.entry.get(),
                'aws_access_key_id': self.aws_access_key_id.entry.get(),
                'aws_secret_access_key': self.aws_secret_access_key.entry.get()
        }

        pickle.dump( data, open( "config.p", "wb" ) )

        self.destroy()

    def generate_url(self):
        url = self.instagram.generate_url(self.client_id.entry.get())
        self.url.entry.delete(0, END)
        self.url.entry.insert(0, url)

    def get_access_token(self):
        access_token = self.instagram.get_access_token(self.client_id.entry.get(), self.client_secret.entry.get(), self.code.entry.get())
        self.access_token.entry.delete(0, END)
        self.access_token.entry.insert(0, access_token)

class CSEntry():
    def __init__(self, master, text, value, row, button_text=None, button_command=None):
        self.label = Label(master, text=text)
        self.label.grid(row=row, sticky=W)
        self.entry = Entry(master, width=50)
        self.entry.grid(row=row, column=1)
        self.entry.insert(0, value)

        if button_text:
            self.button = Button(master, text=button_text, command=button_command)
            self.button.grid(row=row, column=2, sticky=W)

class CSTitle():
    def __init__(self, master, text, row):
        self.label = Label(master, text=text, font=("Helvetica", 18, 'bold'), pady=10)
        self.label.grid(row=row, columnspan=2, sticky=W)

class CSSeparator():
    def __init__(self, master, row):
        self.canvas = Canvas(master, width=400, height=10)
        self.canvas.grid(row=row, columnspan=2)
