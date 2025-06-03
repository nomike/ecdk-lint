# Copyright (C) 2023 Adrien Vergé
# Copyright (C) 2025 nomike Postmann
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Use this rule to report stacks where the "Parameters" section is missing.
"""

import os.path

from ecdklint.linter import LintProblem

ID = "stackname-too-long"
TYPE = "file"
CONF: dict[str, str] = {
    'max-length': int
}
DEFAULT: dict[str, str] = {
    'max-length': 128
}


def check(conf, data, filepath):
    stackname = os.path.basename(filepath).replace(".json", "")
    if len(stackname) > conf['max-length']:
        yield LintProblem(1, 1, f'Stack name is too long (max {conf['max-length']} characters)')
    