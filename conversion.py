from os import walk, makedirs, chdir
from os.path import join
from pathlib import Path
from subprocess import run


# Compile list of all directories with relevant data
'''def compile_dirs(parent_dir, relevant_child, relevant_grandchild):
    compiled_dirs = []
    for child in relevant_child:
        for grandchild in relevant_grandchild:
            select_path = join(parent_dir, child, grandchild)
            compiled_dirs.append(select_path)
    return compiled_dirs'''

def compile_dirs(parent_dir, relevant_child, relevant_grandchild):
    compiled_dirs = {"parent": parent_dir, "children": {}}
    for child in relevant_child:
        compiled_dirs["children"][child] = []
        for grandchild in relevant_grandchild:
            compiled_dirs["children"][child].append(grandchild)
    return compiled_dirs


# Convert files fitting specified criteria and save to different location
def convert_data(orig_dirs, time, converter):
    # Create directories for converted files
    for child, grandchildren in orig_dirs["children"].items():
        for grandchild in grandchildren:
            for root, _, files in walk(join(orig_dirs["parent"],
                                            child,
                                            grandchild)):
                if files:
                    makedirs(join(orig_dirs["parent"] + " CSV",
                             child,
                             grandchild,
                             Path(root).name))

    # Walk through specified directories
    for dir in orig_dirs:
        for root, _, files in walk(dir):
            chdir(root)
            for file in files:
                # Only convert files for specified time
                if file.endswith(time):
                    new_file = join(Path(dir).parent.parent,
                                    "Data CSV",
                                    Path(dir).parent.name,
                                    Path(dir).name,
                                    Path(root).name,
                                    file.rstrip('.DAT'))
                    # run([converter, file, new_file])
