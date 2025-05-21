from termcolor import colored


class File:
    def __init__(self, name, content="", parent=None):
        if not name.endswith(".txt"):
            raise ValueError("File name must end with .txt")
        self.name = name
        self.content = content
        self.parent = parent
        self.size = len(content)

    def append(self, new_content):
        self.content += "" + new_content
        self.size += len(new_content) + 1

    def edit_line(self, edited_line, edited_content):
        content_list = self.content.splitlines()
        if 0 <= edited_line - 1 < len(content_list):
            content_list[edited_line - 1] = edited_content
            self.content = '\n'.join(content_list)
            self.size = len(self.content)
        else:
            print("your line does not exist ! ")

    def deline(self, del_line):
        content_list = self.content.splitlines()
        if 0 <= del_line - 1 < len(content_list):
            content_list.pop(del_line - 1)
            self.content = '\n'.join(content_list)
            self.size = len(self.content)
        else:
            print("your line does not exist ! ")

    def cat(self):
        if self.content:
            print(self.content)
        else:
            print("your file is empty! ")

    def get_size(self):
        return self.size


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

    def mkdir(self, prameters: list):
        path = prameters[0]
        name = prameters[1]
        if path == "":
            new_dir = Directory(name, self.current)
            self.current.contents[name] = new_dir
        else:
            new_dir = Directory(name, path)
            path.contents[name] = new_dir

    def cd(self, prameters : list):
        path = prameters[0]
        if path == "":
            if prameters[1] == "..":
                if self.current.parent is not None:
                    self.current = self.current.parent
                    self.path.pop()
            else:
                self.current = self.current.contents[prameters[1]]
                self.path.append(prameters[1])
        else:
            self.current = path
            self.path.append(path.name)

    def ls(self,prameters:list):
        for dirc in self.current.contents:
            print(colored(dirc, "blue"), end="\t")
        print()
    
    def rm(self, prameters : list):
        path = prameters[0]
        if path:
            if isinstance(path, Directory):
                path.contents.clear()
            if path.name in path.parent.contents:
                del path.parent.contents[path.name]
            else:
                print("Path does not exist or is invalid.")
        else:
            print("Invalid path.")

    def cp(self, prameters : list):
        source_path = prameters[0]
        print(source_path)
        destination_path = prameters[1]
        print(destination_path)
        if source_path and destination_path and isinstance(destination_path, Directory):
            if isinstance(source_path, Directory):
                deep_copy = Directory(source_path.name + "_copy", parent=destination_path)
                deep_copy.contents = {name: item for name, item in source_path.contents.items()}
            else:
                deep_copy = File(source_path.name.replace(".txt", "") + "_copy.txt", content=source_path.content,parent=destination_path)
            destination_path.contents[deep_copy.name] = deep_copy
        else:
            print("Invalid source or destination path.")

    def mv(self, prameters : list):
        source_path = prameters[0]
        destination_path = [1]

        if source_path and destination_path and isinstance(destination_path, Directory):
            if source_path.name in source_path.parent.contents:
                del source_path.parent.contents[source_path.name]
            source_path.parent = destination_path
            destination_path.contents[source_path.name] = source_path
        else:
            print("Invalid source or destination path.")

    def new_file_txt(self, prameters : list):
        path = prameters[0]
        if path and isinstance(path, File):
            print("Enter new content for the file (type 'EOF' on a new line to finish):")
            new_content = []
            while True:
                line = input()
                if line == "EOF":
                    break
                new_content.append(line)
            path.content = "\n".join(new_content)
            path.size = len(path.content)
        else:
            print("Invalid path or the specified path is not a file.")

    def touch(self, prameters: list):
        path = prameters[0]
        name = prameters[1]

        if not name.endswith(".txt"):
            raise ValueError("File name must end with .txt")

        folder = path if path else self.current

        if folder and isinstance(folder, Directory):
            if name in folder.contents:
                print("File already exists.")
            else:
                new_file = File(name, "", folder)
                folder.contents[name] = new_file
        else:
            print("Invalid path or folder does not exist.")

    def rename(self, prameters : list):
        path = prameters[0]
        new_name = prameters[1]
        if path and path.name in path.parent.contents:
            if "/" in new_name:
                print("Invalid name: '/' is not allowed in names.")
                return
            path.parent.contents[new_name] = path.parent.contents.pop(path.name)
            path.name = new_name
        else:
            print("Invalid path or the specified path does not exist.")

    def append_text(self, prameters : list):
        print(prameters)
        path = prameters[0]
        if isinstance(path, File):
            print("Enter text to append to the file (type 'EOF' on a new line to finish):")
            new_content = []
            while True:
                line = input()
                if line == "EOF":
                    break
                new_content.append(line)
            path.append("\n".join(new_content))
        else:
            print("Invalid path or the specified path is not a file.")

    def edit_line(self, prameters : list):
        path = prameters[0]
        line_number = prameters[1]
        new_content = prameters[2]
        if path and isinstance(path, File):
            path.edit_line(line_number, new_content)
        else:
            print("Invalid path or the specified path is not a file.")

    def delete_line(self, prameters : list):
        path = prameters[0]
        line_number = prameters[1]
        if isinstance(path, File):
            path.deline(int(line_number))
        else:
            print("Invalid path or the specified path is not a file.")

    def cat(self, prameters : list):
        path = prameters[0]
        if path and isinstance(path, File):
            path.cat()
        else:
            print("Invalid path or the specified path is not a file.")

    def cls(self,prameters:list):
        print("\033c", end="")


class CommandPrommt:
    def __init__(self, user, file_system: VirtualFileSystem):
        self.commands = {
            "mkdir": file_system.mkdir,
            "cd": file_system.cd,
            "ls": file_system.ls,
            "touch": file_system.touch,
            "rm": file_system.rm,
            "rename": file_system.rename,
            "cp": file_system.cp,
            "mv": file_system.mv,
            "nwfiletxt": file_system.new_file_txt,
            "appendtxt": file_system.append_text,
            "editline": file_system.edit_line,
            "deline": file_system.delete_line,
            "cat": file_system.cat,
            "cls": file_system.cls,
        }
        self.user = user
        self.file_system = file_system

    def _path_parser(self, path):
        folder = self.file_system.root
        if path[:5] == "/root":
            for name in (path.split("/"))[2:]:
                if name not in folder.contents:
                    raise KeyError(f"Path does not exist: {path}")
                folder = folder.contents[name]      
        else:
            full_path =file_system.path[1:]
            full_path.reverse()
            for dirc in full_path:
                path = "/"+dirc+path
            try:
                for name in (path.split("/"))[1:]:
                    if name not in folder.contents:
                        raise KeyError(f"Path does not exist: {path}")
                    folder = folder.contents[name]
            except KeyError:
                print(f"Path does not exist: {path}")
                return None
        return folder


    def read_line(self):
        command = input(colored(f"{'/'.join(self.file_system.path)} {self.user} >", "green"))
        commands = command.split(" ")
        func = self.commands.get(commands[0])

        if len(commands) >=3 and commands[1].startswith("/") and commands[2].startswith("/"):
            commands[1]=self._path_parser(commands[1])
            commands[2]=self._path_parser(commands[2])
        elif len(commands) >=2 and commands[1].startswith("/"):
            commands[1]=self._path_parser(commands[1])
        else:
            commands.insert(1,"")


        if func:
            func(commands[1:])
        else:
            print(colored("Invalid Command!","red"))


if __name__ == "__main__":
    file_system = VirtualFileSystem()
    command_prommt = CommandPrommt("Admin", file_system)
    while True:
        command_prommt.read_line()
