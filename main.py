class File:
    def __init__(self, name, content=""):
        self.name = name
        self.content = content


class Directory:
    def __init__(self, name):
        self.name = name
        self.contents = {}  

class VirtualFileSystem:
    def __init__(self):
        self.root = Directory("/")
        self.current = self.root
        self.path = []


class CommandPrommt:
    def __init__(self,user):
        self.commands = {}
        self.user = user

    def read_line(self):
        pass