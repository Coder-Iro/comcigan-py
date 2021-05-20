# comcigan-py
[![Travis (.com)](https://img.shields.io/travis/com/Team-IF/comcigan-py?logo=travis&style=flat-square)](https://www.travis-ci.com/github/Team-IF/comcigan-py) [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/comcigan?logo=python&style=flat-square)](https://pypi.org/project/comcigan/) [![PyPI](https://img.shields.io/pypi/v/comcigan?logo=python&style=flat-square)](https://pypi.org/project/comcigan/) [![PyPI - Downloads](https://img.shields.io/pypi/dm/comcigan?style=flat-square)](https://pypi.org/project/comcigan/) [![Codecov](https://img.shields.io/codecov/c/github/Team-IF/comcigan-py?logo=codecov&style=flat-square)](https://app.codecov.io/gh/Team-IF/comcigan-py)  
Comcigan-py is a parser for korean school timetable service "comcigan" made with python.
## Installation
Install and update using [pip](https://pip.pypa.io/en/stable/quickstart/):
```sh
$ pip install comcigan
```
## Example
A simple example for synced version
```python
from comcigan import School

myschool = School("schoolname")
# "schoolname" doesn't have to be the full name of the school.
# comcigan-py automatically recognizes "schoolname" as a search query.
# If there is only one school searched, an instance of that school is created.
# If there are more than two schools searched, ValueError is raised.
# If there is no school searched, NameError is raised.

print(myschool.name)
# This may not be the same as "schoolname".

print(myschool[2][3][4][3])
# This returns Thursday 3rd period in the 2nd grade 3rd class.
```

## License
This project is under the GNU Lesser General Public License version 3.0 or later (LGPL v3.0+).
