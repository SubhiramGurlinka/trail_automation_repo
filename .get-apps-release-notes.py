import datetime
import os
import re
import subprocess


def validate_filepath(filepath=""):
    """validate string is filepath or URL"""
    if os.path.isfile(filepath) and os.access(filepath, os.R_OK):
        return filepath
    else:
        raise ValueError(filepath)


def get_latest_previous_version_tag():
    """get newest tag from GIT"""
    run_cmd = ["git", "tag", "-l", "--sort=-version:refname", "v*"]
    git_output = subprocess.check_output(run_cmd).decode()
    # print(git_output)
    matches = re.search(r"^(?P<latest>v.+)\n(?P<previous>v.+)\n", git_output)
    return matches.group("latest"), matches.group("previous")


def get_all_tags():
    """get all tags from GIT"""
    run_cmd = ["git", "tag", "-l", "--sort=-version:refname", "v*"]
    git_output = subprocess.check_output(run_cmd).decode()
    matches = re.findall(r"(v.+)", git_output)
    return matches


def get_count_items_in_all_tags():
    """get the count of all items in all tags. This will undercount the real value."""
    tags = get_all_tags()

    count = 0

    for i in range(len(tags)):
        try:
            count += len(
                get_files_changed_between_git_tags(
                    tags[i], tags[i + 1], diff_filter="CMRTUXBA"
                )
            )
        except IndexError:
            break

    return count


def get_files_changed_between_git_tags(
    first_tag, second_tag, re_filter=".bes$", diff_filter=""
):
    """get the list of files changed between tags"""
    run_cmd = [
        "git",
        "diff",
        f"tags/{first_tag}",
        f"tags/{second_tag}",
        "--name-only",
        f"--diff-filter={diff_filter.upper()}",
    ]
    git_output = subprocess.check_output(run_cmd).decode()
    # print(git_output)
    # return array of file paths that meet filter
    return [val for val in git_output.split("\n") if re.search(re_filter, val)]


def get_regex_from_file(filepath, pattern):
    """get first regex group or full regex from bes file"""
    # print(filepath)
    if not validate_filepath(filepath):
        raise FileNotFoundError

    with open(filepath, "r") as f:
        filetext = f.read()
        try:
            return re.search(pattern, filetext).group(1)
        except IndexError:
            return re.search(pattern, filetext).group()
        except AttributeError:
            return "Unknown"


def get_title_part_from_bes_file(filepath, pattern="<Title>(.+)</Title>"):
    """get title part from bes_file"""
    return get_regex_from_file(filepath, pattern)


def get_vendor_from_bes_file(
    filepath, pattern=r"<Value><!\[CDATA\[?cpe:2.3:a:([\w\d\.]+):"
):
    """get vendor from bes file"""
    vendor = get_regex_from_file(filepath, pattern)
    if vendor.islower():
        vendor = vendor.capitalize()
    return vendor


def main():
    """Execution Starts Here"""
    # example: https://forum.bigfix.com/t/content-modification-updates-for-windows-applications-published-2022-04-12/41302
    # this step will be skipped in both ACT and GITHUB_ACTIONS
    if not "GITHUB_ACTIONS" in os.environ:
        print("\nINFO: fetching remote tags on local execution.")
        run_cmd = ["git", "fetch", "--all", "--tags"]
        print(subprocess.check_output(run_cmd).decode())
        # print(get_count_items_in_all_tags())

    latest, previous = get_latest_previous_version_tag()

    # previous = "v5"

    # print("Previous Site:", previous, "\nCurrent Site:", latest)
    print("[Changelog](../../compare/" + previous + "..." + latest + ")\n")
    print(
        "## Content Modification: Updates for Linux Applications Middleware published "
        + str(datetime.date.today())
    )
    print(
        "BigFix has modified content in the Updates for Linux Applications Middleware site, which is available to customers with BigFix Compliance."
    )

    # get added:
    added_items = get_files_changed_between_git_tags(previous, latest, diff_filter="A")
    if added_items and len(added_items) > 0:
        print("\n## New Items:")
        for item in added_items:
            title_part = get_title_part_from_bes_file(item)
            # vendor = get_vendor_from_bes_file(item)
            print(f"- {title_part}")

    # get updated:
    updated_items = get_files_changed_between_git_tags(
        previous, latest, diff_filter="CMRTUXB"
    )
    if updated_items and len(updated_items) > 0:
        print("\n## Modified Items:")
        for item in updated_items:
            title_part = get_title_part_from_bes_file(item)
            # vendor = get_vendor_from_bes_file(item)
            print(f"- {title_part}")

    # get deleted:
    deleted_items = get_files_changed_between_git_tags(
        previous, latest, diff_filter="D"
    )
    if deleted_items and len(deleted_items) > 0:
        print("\n## Deleted Items:")
        for item in deleted_items:
            file_part = re.search(".+/(.+).bes", item).group(1)
            print(f"- { file_part }")

    # # get all items:
    # all_items = get_files_changed_between_git_tags("v0", latest, diff_filter="CMRTUXBA")

    # # print(all_items)
    # if all_items and len(all_items) > 0:
    #     print("\n## All Items:")
    #     for item in all_items:
    #         title_part = get_title_part_from_bes_file(item)
    #         # vendor = get_vendor_from_bes_file(item)
    #         print(f"- {title_part}")

    print("\n## Reason for Update:")
    print("- New Software Releases from Vendors")
    print("\n## Actions to Take:")
    print("- Review new content and deploy as needed.")
    print("- For oracle db, you must run the following as policy actions:")
    print("  - Update Oracle Patch List and update script - ASM")
    print("  - Update Oracle Patch List and update script")
    print("")
    print(
        "More Info: https://forum.bigfix.com/t/what-are-the-updates-for-applications-middleware-sites/42258"
    )

    # read additional action items from file:
    if os.path.exists("release-notes-actions-to-take.md"):
        with open("release-notes-actions-to-take.md", "r") as f:
            print(f.read())
    else:
        print("\n")

    print("## Published Site Version:")
    print("- Updates for Linux Applications Middleware, Version: " + latest)
    print("\n## Additional Links:")
    print("- None")
    print(
        """\n–
Application Engineering Team
HCL BigFix\n"""
    )

    # get unchanged files
    # print("get all:")
    # bes_files = set([])
    # for file in glob.glob("fixlets/*.bes", recursive=True):
    #     bes_files.add(file)
    # print(len(bes_files))
    # for item in updated_items:
    #     bes_files.discard(item)
    # print(len(bes_files))
    # print(updated_items)
    # print(bes_files)


if __name__ == "__main__":
    exit(main())
