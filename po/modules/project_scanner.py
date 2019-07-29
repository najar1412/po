__author__ = 'Rory Jarrel'
__version__ = '2019.0.1'

"""
Script to scan predined folder that saves out a text file containing all folders that exceede 255 characters.
"""

# TODO: remove hardcodings
# TODO: catch networking/encoding errors


from pathlib import Path
from collections import defaultdict
import os


# GLOBALS
FOLDER_LOCATION = 'z:/'
OUTPUT_LOCATION = 'd:/project_output.txt'
MAX_CHARACTER_COUNT = 253
IGNORED_LOCATIONS = ['visualhouse', '#recycle', '.TemporaryItems']

def get_folders(location):
    return [x for x in Path(location).iterdir() if x.is_dir()]

def scan_folder(path):
    bad_projects = defaultdict(set)
    if path.name not in IGNORED_LOCATIONS:
        for x in path.glob('**/*'):
            if len(x.as_uri()) > MAX_CHARACTER_COUNT:
                bad_projects[path.name].add(x.parent.as_posix())

        if bad_projects:
            return dict(bad_projects)

def check_output(location, data):
    if Path(location).exists():
        print('Output file already exists, please rename it or delete it.')
    else:
        with open(location, mode='x', encoding='UTF-8', buffering=1) as f:
            for k, v in data.items():
                f.write(f'--------\n{k}\n--------')
                for addy in v:
                    f.write(f'\n\t{addy}')
                f.write(f'\n')

def run_report(folder):
    bad_projects = {}

    project = scan_folder(folder)
    if project:
        for k, v in project.items():
            bad_projects[k] = v

        return bad_projects

    return False

def runner():
    print(f':: Scanning projects drive. {FOLDER_LOCATION} ...')
    bad_projects = {}
    projects = get_folders(FOLDER_LOCATION)

    for folder in projects:
        project = scan_folder(folder)
        
        if project:
            for k, v in project.items():
                bad_projects[k] = v

    print(bad_projects)

    print(f':: Saving out text file to {OUTPUT_LOCATION} ...')
    check_output(OUTPUT_LOCATION, bad_projects)
    print(f':: Finished!')


"""
if __name__ == "__main__":
    runner()
"""