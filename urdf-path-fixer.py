import sys
import os


def fix_urdf_path(in_file):
    with open(in_file, 'r+') as file:
        text = file.read().replace('package://', os.path.dirname(os.path.abspath(in_file)) + '/')
        file.seek(0)
        file.write(text)
        file.truncate()


if __name__ == '__main__':
    in_file = sys.argv[1]
    fix_urdf_path(in_file)
