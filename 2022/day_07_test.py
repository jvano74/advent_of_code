from typing import NamedTuple


class Puzzle:
    """
    --- Day 7: No Space Left On Device ---
    You can hear birds chirping and raindrops hitting leaves as the expedition proceeds.
    Occasionally, you can even hear much louder sounds in the distance; how big do the
    animals get out here, anyway?

    The device the Elves gave you has problems with more than just its communication
    system. You try to run a system update:

    $ system-update --please --pretty-please-with-sugar-on-top
    Error: No space left on device

    Perhaps you can delete some files to make space for the update?

    You browse around the filesystem to assess the situation and save the resulting
    terminal output (your puzzle input). For example:

    $ cd /
    $ ls
    dir a
    14848514 b.txt
    8504156 c.dat
    dir d
    $ cd a
    $ ls
    dir e
    29116 f
    2557 g
    62596 h.lst
    $ cd e
    $ ls
    584 i
    $ cd ..
    $ cd ..
    $ cd d
    $ ls
    4060174 j
    8033020 d.log
    5626152 d.ext
    7214296 k

    The filesystem consists of a tree of files (plain data) and directories (which can
    contain other directories or files).

    The outermost directory is called /.

    You can navigate around the filesystem, moving into or out of directories and
    listing the contents of the directory you're currently in.

    Within the terminal output, lines that begin with $ are commands you executed,
    very much like some modern computers:

    cd means change directory. This changes which directory is the current directory,
    but the specific result depends on the argument:

    cd x moves in one level: it looks in the current directory for the directory named
    x and makes it the current directory.

    cd .. moves out one level: it finds the directory that contains the current
    directory, then makes that directory the current directory.

    cd / switches the current directory to the outermost directory, /.

    ls means list. It prints out all of the files and directories immediately contained
    by the current directory:

    123 abc means that the current directory contains a file named abc with size 123.
    dir xyz means that the current directory contains a directory named xyz.

    Given the commands and output in the example above, you can determine that the
    filesystem looks visually like this:

    - / (dir)
        - a (dir)
            - e (dir)
                - i (file, size=584)
            - f (file, size=29116)
            - g (file, size=2557)
            - h.lst (file, size=62596)
        - b.txt (file, size=14848514)
        - c.dat (file, size=8504156)
        - d (dir)
            - j (file, size=4060174)
            - d.log (file, size=8033020)
            - d.ext (file, size=5626152)
            - k (file, size=7214296)

    Here, there are four directories: / (the outermost directory), a and d (which
    are in /), and e (which is in a). These directories also contain files of
    various sizes.

    Since the disk is full, your first step should probably be to find directories that
    are good candidates for deletion. To do this, you need to determine the total size
    of each directory. The total size of a directory is the sum of the sizes of the
    files it contains, directly or indirectly. (Directories themselves do not count
    as having any intrinsic size.)

    The total sizes of the directories above can be found as follows:

    The total size of directory e is 584 because it contains a single file i of size
    584 and no other directories.

    The directory a has total size 94853 because it contains files
    f (size 29116), g (size 2557), and h.lst (size 62596), plus
    file i indirectly (a contains e which contains i).

    Directory d has total size 24933642.

    As the outermost directory, / contains every file. Its total size is 48381165, the
    sum of the size of every file.

    To begin, find all of the directories with a total size of at most 100000, then
    calculate the sum of their total sizes. In the example above, these directories
    are a and e; the sum of their total sizes is 95437 (94853 + 584).

    (As in this example, this process can count files more than once!)

    Find all of the directories with a total size of at most 100000. What is the sum
    of the total sizes of those directories?


    --- Part Two ---
    Now, you're ready to choose a directory to delete.

    The total disk space available to the filesystem is 70000000. To run the update,
    you need unused space of at least 30000000. You need to find a directory you can
    delete that will free up enough space to run the update.

    In the example above, the total size of the outermost directory (and thus the total
    amount of used space) is 48381165; this means that the size of the unused space
    must currently be 21618835, which isn't quite the 30000000 required by the update.
    Therefore, the update still requires a directory with total size of at least
    8381165 to be deleted before it can run.

    To achieve this, you have the following options:

    Delete directory e, which would increase unused space by 584.
    Delete directory a, which would increase unused space by 94853.
    Delete directory d, which would increase unused space by 24933642.
    Delete directory /, which would increase unused space by 48381165.

    Directories e and a are both too small; deleting them would not free
    up enough space. However, directories d and / are both big enough! Between these,
    choose the smallest: d, increasing unused space by 24933642.

    Find the smallest directory that, if deleted, would free up enough space on the
    filesystem to run the update. What is the total size of that directory?
    """


with open("day_07_input.txt") as fp:
    RAW_INPUT = fp.read()

RAW_SAMPLE = """$ cd /
    $ ls
    dir a
    14848514 b.txt
    8504156 c.dat
    dir d
    $ cd a
    $ ls
    dir e
    29116 f
    2557 g
    62596 h.lst
    $ cd e
    $ ls
    584 i
    $ cd ..
    $ cd ..
    $ cd d
    $ ls
    4060174 j
    8033020 d.log
    5626152 d.ext
    7214296 k"""


class File(NamedTuple):
    name: str
    size: int

    def get_size(self):
        return self.size


class Folder:
    def __init__(self, name) -> None:
        self.name = name
        self.size = None
        self.ls = []

    def get_size(self):
        if self.size is None:
            total = sum(f.get_size() for f in self.ls)
            self.size = total
        return self.size


def test_folders():
    file1 = File(name="a", size=123)
    file2 = File(name="b", size=321)
    file3 = File(name="c", size=111)
    folder1 = Folder(name="")
    folder2 = Folder(name="f1")
    folder3 = Folder(name="f2")
    folder1.ls = [file1, folder2, folder3]
    folder2.ls = [file2, file3]
    assert folder1.get_size() == 555


def parse_terminal_output(raw_output):
    root = Folder("/")
    folders = {"/": root}

    def get_folder(key, name):
        if key == "":
            key = "/"
        if key not in folders:
            new_folder = Folder(name)
            folders[key] = new_folder
        return folders[key]

    ls_mode = False
    cwd = [""]

    for hx, line in enumerate(raw_output.split("\n")):
        arg = line.strip().split(" ")
        if line == "$ cd /":
            cwd = [""]
            current_dir = root
            continue
        if arg[0] == "$":
            if ls_mode:
                current_dir.ls = ls
                ls_mode = False
            if arg[1] == "cd":
                if arg[2] == "..":
                    cwd = cwd[:-1]
                else:
                    cwd.append(arg[2])
                current_dir = get_folder("/".join(cwd), arg[2])
            elif arg[1] == "ls":
                ls_mode = True
                ls = []
        elif arg[0] == "dir":
            fdir = cwd[:]
            fdir.append(arg[1])
            dir = get_folder("/".join(fdir), arg[1])
            ls.append(dir)
        else:
            size = int(arg[0])
            ls.append(File(name=arg[1], size=size))
    # Check if we had a final ls to add
    if ls_mode:
        current_dir.ls = ls
        ls_mode = False

    return {k: f.get_size() for k, f in folders.items()}


def test_parse_terminal_output():
    dir_list = parse_terminal_output(RAW_SAMPLE)
    sample_dir_list = {"/": 48381165, "/a": 94853, "/d": 24933642, "/a/e": 584}
    # 70_000_000 >= dir_list["/"] + 30_000_000 - min_delete
    min_delete = dir_list["/"] + 30_000_000 - 70_000_000
    assert dir_list == sample_dir_list
    assert sum(s for s in dir_list.values() if s <= 100000) == 95437
    assert min(s for s in dir_list.values() if s >= min_delete) == 24933642

    dir_list = parse_terminal_output(RAW_INPUT)
    # 70_000_000 >= dir_list["/"] + 30_000_000 - min_delete
    min_delete = dir_list["/"] + 30_000_000 - 70_000_000
    assert sum(s for k, s in dir_list.items() if s <= 100000) == 1206825
    assert min(s for s in dir_list.values() if s >= min_delete) == 9608311
