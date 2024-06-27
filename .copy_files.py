"""
This python file copys all the cached build files
"""
# relevance that gives files to copy:
# number of files whose(name of it ends with ".bes" AND name of it contains "pdate") of folders whose(name of it contains ".bigfix.") of folders "Library\AutoPkg\Cache" of folders of folders "/Users"

import glob
import os
import shutil
import sys


def main():
    print("main()")

    file_paths = glob.glob('/Users/*/Library/AutoPkg/Cache/*.bigfix.*/*pdate*.bes')

    print(f"num files to copy: {len(file_paths)}")

    dest_folder = os.path.abspath(glob.glob('./Fixlets/Updates')[0])

    print(dest_folder)

    for item in file_paths:
        shutil.copy(item, dest_folder)

    return 0

if __name__ == "__main__":
    sys.exit(main())
