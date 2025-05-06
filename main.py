from termcolor import colored

class File:
    def __init__(self, name, content=""):
        if not name.endswith(".txt"):
            raise ValueError("File name must end with .txt")
        self.name = name
        self.content = content

    @staticmethod
    def touch(name, content=""):
        if not name.endswith(".txt"):
            raise ValueError("File name must end with .txt")
        new_file = File(name, content)
        print(f"new file with {new_file.name} name has been created")
        return new_file

    def rm(self):
        print(f"file with {self.name} name was deleted.")
        self.name = None
        self.content = None

    def new_file_txt(self, new_content):
        self.content = ""
        self.content += new_content

    def append(self, new_content):
        self.content += "\n" + new_content

    def edit_line(self, edited_line, edited_content):
        content_list = self.content.split("\n")
        if 0 < edited_line <= len(content_list):
            content_list[edited_line-1] = edited_content
            self.content = '\n'.join(content_list)
        else:
            print("your line does not exist ! ")

    def deline(self, del_line):
        content_list = self.content.split("\n")
        if 0 < del_line <= len(content_list):
            content_list.pop(del_line - 1)
            self.content = '\n'.join(content_list)
        else:
            print("your line does not exist ! ")

    def cat(self):
        if self.content is not None:
            print(self.content)
        else:
            print("your file not found ! ")

    def cp(self):
        new_name = self.name.replace(".txt", "_copy.txt")
        copied_file = File(new_name, self.content)
        print(f"File '{self.name}' copied to '{new_name}'")
        return copied_file

    def rename(self, new_name):
        if not new_name.endswith(".txt"):
            print("File name must end with .txt")
        else:
            print(f"File renamed from '{self.name}' to '{new_name}'")
            self.name = new_name


class Directory:
    def __init__(self, name, parent=None):
        self.name = name
        self.contents = {}
        self.parent = parent

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
        self.root = Directory("root")
        self.current = self.root
        self.path = ["root"]

    def mkdir(self,name,path=""):
        new_dir = Directory(name, self.current)
        if path == "":
            self.current.contents[name] = new_dir
        else:
            path.contents[name] = new_dir

        print("New Directory created!")

    def cd(self,path):
        if path == "..":
            if self.current.parent is not None:
                self.current = self.current.parent
                self.path.pop()      
        else:
            self.current = self.current.contents[path]
            self.path.append(path)


    def ls(self):
        for dirc in self.current.contents :
            print(colored(dirc,"blue"))
class CommandPrommt:
    def __init__(self, user, file_system:VirtualFileSystem):
        self.commands = {"mkdir":file_system.mkdir,"cd":file_system.cd,"ls":file_system.ls}
        self.user = user


    def _path_parser(self,path):
        if path[0] == "/":
            folder =file_system.root
            for name in (path.split("/"))[1:]:
                folder= folder.contents[name]
            return folder
        else:
            return path

    def read_line(self):
        command = input(colored(f"{'/'.join(file_system.path)} {self.user} >","green"))
        command = command.split(" ")
        func = self.commands.get(command[0])
        if func:
            if len(command)==1:
                func()
            elif len(command) == 2 :
                func(self._path_parser(command[1]))
            else:
                func(self._path_parser(command[1]),self._path_parser(command[2]))
        else:
            print("Invalid Command!")
        



if __name__ == "__main__":
    file_system = VirtualFileSystem()
    command_prommt = CommandPrommt("Admin",file_system)
    while True:
        command_prommt.read_line()
