#!/usr/bin/env python3


# Copyright 2018 The Meson development team

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

'''Renames test case directories using Git from this:

1 something
3 other
3 foo
3 bar

to this:

1 something
2 other
3 foo
4 bar

This directory must be run from source root as it touches run_unittests.py.
'''

import os, sys, subprocess

from glob import glob

def get_entries():
    entries = []
    for e in glob('*'):
        if not os.path.isdir(e):
            sys.exit('Current directory must not contain any files.')
        (number, rest) = e.split(' ', 1)
        try:
            number = int(number)
        except ValueError:
            sys.exit('Dir name %d does not start with a number.' % e)
        entries.append((number, rest))
    entries.sort()
    return entries

def replace_source(sourcefile, replacements):
    with open(sourcefile, 'r') as f:
        contents = f.read()
    for old_name, new_name in replacements:
        contents = contents.replace(old_name, new_name)
    with open(sourcefile, 'w') as f:
        f.write(contents)

def condense(dirname):
    curdir = os.getcwd()
    os.chdir(dirname)
    entries = get_entries()
    replacements = []
    for _i, e in enumerate(entries):
        i = _i + 1
        if e[0] != i:
            old_name = str(e[0]) + ' ' + e[1]
            new_name = str(i) + ' ' + e[1]
            #print('git mv "%s" "%s"' % (old_name, new_name))
            subprocess.check_call(['git', 'mv', old_name, new_name])
            replacements.append((old_name, new_name))
    os.chdir(curdir)
    replace_source('run_unittests.py', replacements)
    replace_source('run_project_tests.py', replacements)

if __name__ == '__main__':
    if len(sys.argv) != 1:
        sys.exit('This script takes no arguments.')
    for d in glob('test cases/*'):
        condense(d)
