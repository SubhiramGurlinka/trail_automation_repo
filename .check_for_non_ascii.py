# from Jimmy Glass
import os, re
# from tqdm import tqdm
from unidecode import unidecode


def scanNonAscii(contents):
    m = re.search("[^\x00-\x7F]+", contents)
    return m


total_bes_files = 0
total_invalid_files = 0
total_invalid_scanner_files = 0

build_folder = r"Fixlets/Oracle"

for dirpath, dirnames, filenames in os.walk(build_folder):
    # print(f"Processing {dirpath}")

    for filename in filenames:
        if filename.endswith(".bes"):
            this_path = os.path.join(dirpath, filename)
            total_bes_files += 1

            with open(this_path) as f:
                file_contents = f.read()

            if not file_contents.isascii():
                print(
                    f"Invalid: {dirpath} - {filename} contained non-ascii chars found by Python"
                )
                with open(this_path, "wt", encoding="utf-8") as this_fixlet_file:
                    this_fixlet_file.write(unidecode(file_contents))

                total_invalid_files += 1

print(f"    Total BES Files: {total_bes_files}")
print(f"Total Invalid Files: {total_invalid_files}")
