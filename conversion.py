from os import walk, makedirs, chdir
from os.path import join, basename
from subprocess import run


# Compile list of all directories with relevant data
def compile_dirs(parent_dir, relevant_child, relevant_grandchild):
    compiled_dirs = {"parent": parent_dir, "children": {}}
    for child in relevant_child:
        compiled_dirs["children"][child] = []
        for grandchild in relevant_grandchild:
            compiled_dirs["children"][child].append(grandchild)
    return compiled_dirs


# Convert files fitting specified criteria and save to different location
def convert_data(orig_dirs, time, converter):
    print("Converting .DAT files to .CSV. "
          f"This may take a few minutes...\n{'='*80}")
    converted_dir = orig_dirs["parent"] + " CSV"
    for child, grandchildren in orig_dirs["children"].items():
        print(f"Inside {child} directory...")
        for grandchild in grandchildren:
            print(f"\t--> Inside {grandchild} directory...")
            for root, _, files in walk(join(orig_dirs["parent"],
                                            child,
                                            grandchild)):
                # Create directories for converted files
                if files:
                    new_dir = join(converted_dir,
                                   child,
                                   grandchild,
                                   basename(root))
                    makedirs(new_dir, exist_ok=True)
                    chdir(root)

                    # Only convert files for specified time
                    for file in files:
                        if file.endswith(time):
                            new_file = join(new_dir, file.rstrip('.DAT'))
                            run([converter, file, new_file])
    print(f"{'='*80}\nConversion complete.")
    return converted_dir
