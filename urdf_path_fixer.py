import sys
import os


# Replaces package relative path with absolute path
def fix_urdf_path(in_file):
    with open(in_file, 'r+') as file:
        # Replace with \ if Windows, else /
        rep_char = '\\' if os.name == 'nt' else '/'
        text = file.read().replace('package://', os.path.dirname(os.path.abspath(in_file)) + rep_char)
        file.seek(0)
        file.write(text)
        file.truncate()


if __name__ == '__main__':
    file = sys.argv[1]
    fix_urdf_path(file)
