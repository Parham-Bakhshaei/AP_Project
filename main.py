class File:
    def __init__(self, name, content=""):
        self.name = name
        self.content = content

    def touch(self):
        pass

    def rm(self):
        pass

    def new_file_txt(self):
        pass

    def append(self):
        pass

    def edit_line(self):
        pass

    def deline(self):
        pass

    def cat(self):
        pass

    def mv(self):
        pass

    def cp(self):
        pass

    def rename(self):
        pass


class Directory:
    def __init__(self, name):
        self.name = name
        self.contents = {}

    def mkdir(self):
        pass

    def rmdir(self):
        pass

    def mv(self):
        pass

    def cp(self):
        pass

    def rename(self):
        pass

    def ls(self):
        pass


class VirtualFileSystem:
    def __init__(self):
        self.root = Directory("/")
        self.current = self.root
        self.path = []

    def cd(self):
        pass


class CommandPrommt:
    def __init__(self, user):
        self.commands = {}
        self.user = user

    def read_line(self):
        pass


if __name__ == "__main__":
    pass
