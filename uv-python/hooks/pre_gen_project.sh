#!/bin/env python

import re
import sys

MODULE_REGEX = r'^[_a-zA-Z][_a-zA-Z0-9]+$'
project__module = '{{ cookiecutter.project__module }}'

if not re.match(MODULE_REGEX, project__module):
    print(f'ERROR: {project__module} is not a valid Python module name!')
    sys.exit(1)
