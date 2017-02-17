#
# cspost
# Paul Norton
#

### CSPost - Custom Class ###
# Contains all information about an image
class CSPost:
    def __init__(self, id, user_name, platform, file_name, url, text):
        self.id = id
        self.user_name = user_name
        self.platform = platform
        self.file_name = file_name
        self.url = url
        
        # Remove potentially bad characters (emojis, etc.)
        text = text.encode('ascii', 'ignore').decode().strip()
        self.text = (text[:75] + '...') if len(text) > 75 else text
        
        # Build message for image caption
        self.message = '"' + self.text + '" - ' + self.user_name + ' via ' + self.platform