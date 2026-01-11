#!/usr/bin/env python3
"""
Simple script to auto-generate the README.md file for a til project.
NOTE: Someone who wanted to be fancy would actually use a template engine
for this, but this seemed like a task for which it is best to only require
python.  This is not a general purpose script, but tailored for the format
being used for "Today I Learned" repos.
Apply as a git hook by running the following command in linux:
    cd .git/hooks/ && ln -s ../../.scripts/createReadme.py pre-commit && cd -
"""
import os
import sys
from time import gmtime, strftime

# Add the script directory to the path to allow imports
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

from static_text import HEADER, FOOTER

def get_list_of_categories():
    """
    Walk the current directory and get a list of all subdirectories at that
    level.  These are the "categories" in which there are TILs.
    """
    try:
        dirs = [x for x in os.listdir('.') if os.path.isdir(x) and not x.startswith('.')]
        return dirs
    except OSError as e:
        print(f'Error listing directories: {e}', file=sys.stderr)
        return []

def get_title(til_file):
    """
    Read the file until we hit the first line that starts with a #
    indicating a title in markdown.  We'll use that as the title for this
    entry.
    """
    try:
        with open(til_file, 'r', encoding='utf-8') as _file:
            for line in _file:
                line = line.strip()
                if line.startswith('#'):
                    return line[1:].lstrip()  # text after # and whitespace
    except (OSError, UnicodeDecodeError) as e:
        print(f'Error reading file {til_file}: {e}', file=sys.stderr)
    return None

def get_tils(category):
    """
    For a given category, get the list of TIL titles.
    """
    try:
        til_files = [x for x in os.listdir(category)]
    except OSError as e:
        print(f'Error listing files in category {category}: {e}', file=sys.stderr)
        return []
    
    titles = []
    for filename in til_files:
        fullname = os.path.join(category, filename)
        try:
            if (os.path.isfile(fullname)) and fullname.endswith('.md'):
                title = get_title(fullname)
                if title:  # Only add if we successfully got a title
                    titles.append((title, fullname.replace(".md","")))
        except OSError as e:
            print(f'Error processing file {fullname}: {e}', file=sys.stderr)
            continue
    return titles

def get_category_dict(category_names):
    categories = {}
    count = 0
    for category in category_names:
        titles = get_tils(category)
        categories[category] = titles
        count += len(titles)
    return count, categories


def print_file(category_names, count, categories):
    """
    Now we have all the information, print it out in markdown format.
    """
    try:
        with open('README.md', 'w', encoding='utf-8') as file_:
            file_.write('''
# Categories

''')
            # print the list of categories with links
            for category in sorted(category_names):
                file_.write('* [{0}](#{1})\n'.format(category, category))
            # print the section for each category
            file_.write('''
---

''')
            for category in sorted(category_names):
                file_.write('## {0}\n'.format(category))
                tils = categories[category]
                for (title, filename) in sorted(tils):
                    file_.write('* [{0}]({1})\n'.format(title, filename))
                file_.write('\n')

            file_.write(FOOTER)
            file_.write('\n\n')
            # add the line for current year as follows  &copy; 2020 Wayne Arthurton
            file_.write('&copy; {0} Wayne Arthurton'.format(strftime("%Y", gmtime())))

            file_.write('\n\n')
            file_.write('_{0} TILs and counting..._'.format(count))
                    
        print('readme updated with {0} tils!'.format(count))
    except OSError as e:
        print(f'Error writing README.md: {e}', file=sys.stderr)
        sys.exit(1)   

def create_readme():
    """
    Create a TIL README.md file with a nice index for using it directly
    from github.
    """
    # Change to the repository root directory (parent of .scripts)
    repo_root = os.path.dirname(script_dir)
    if repo_root:
        try:
            os.chdir(repo_root)
        except OSError as e:
            print(f'Error changing to repository root: {e}', file=sys.stderr)
            sys.exit(1)
    
    category_names = get_list_of_categories()
    if not category_names:
        print('Warning: No categories found', file=sys.stderr)
    
    count, categories = get_category_dict(category_names)
    print_file(category_names, count, categories)


if __name__ == '__main__':
    create_readme()
    os.system('git add README.md')