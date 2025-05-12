from termcolor import colored

class File:
    def __init__(self, name, content="", parent=None):
        if not name.endswith(".txt"):
            raise ValueError("File name must end with .txt")
        self.name = name
        self.content = content
        self.parent = parent



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

class Directory:
    def __init__(self, name, parent=None):
        self.name = name
        self.contents = {}
        self.parent = parent



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

    def rm(self,path):
        if not isinstance(path,Directory) or not isinstance(path,File):
            path = self.current.contents[path]
        del path.parent.contents[path.name]

    #TODO
    def cp(self):
        new_name = self.name.replace(".txt", "_copy.txt")
        copied_file = File(new_name, self.content)
        print(f"File '{self.name}' copied to '{new_name}'")
        return copied_file

    #TODO
    def mv(self):
        pass


    #TODO
    def new_file_txt(self, new_content):
        self.content = ""
        self.content += new_content

    def touch(self,name,path=""):
        if not name.endswith(".txt"):
            raise ValueError("File name must end with .txt")
        if path == "":
            new_file = File(name, "",self.current)
            self.current.contents[name] = new_file
        else:
            new_file = File(name, "",path)
            path.contents[name] = new_file

        return new_file


    def rename(self, path,name):
        if path.name in path.parent.contents:
            path.parent.contents[name] = path.parent.contents.pop(path.name)

class CommandPrommt:
    def __init__(self, user, file_system:VirtualFileSystem):
        self.commands = {"mkdir":file_system.mkdir,"cd":file_system.cd,"ls":file_system.ls,"touch":file_system.touch,"rm":file_system.rm,"rename":file_system.rename}
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
