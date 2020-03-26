

class NetMode:
    def __init__(self):
        self.net_mode="auto"
        print "__net_mode__init___"

    def set_mode(self,mode):
        self.net_mode=mode


net_mode_class = NetMode()