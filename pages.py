

class BasePage:
    def __init__(self,touchpad, port):
        self.touchpad = touchpad
        self.port = port
        self.page = touchpad.port[port] # allias for port commands
        self.channels = self.page.channel # allias for channels
        self.buttons = self.page.button # allias for buttons
        self.channel = self.button

    def render(self):
        raise NotImplementedError
    
    