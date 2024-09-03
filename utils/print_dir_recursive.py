import os

EXCLUDED_DIRS = {'.idea', '.git', '.venv'}

def create_directory_tree(startpath, indent_level=0):
    for root, dirs, files in os.walk(startpath):
        # Exclude certain directories
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]

        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level + indent_level)
        print(f'{indent}{os.path.basename(root)}/')
        sub_indent = ' ' * 4 * (level + 1 + indent_level)
        for f in files:
            print(f'{sub_indent}{f}')
        # Only process the current directory
        break
    # Recurse into subdirectories
    for d in dirs:
        create_directory_tree(os.path.join(root, d), indent_level + 1)


if __name__ == "__main__":
    startpath = '..'  # Change this if you want to start from a different directory
    print("Project Directory Structure:")
    create_directory_tree(startpath)
