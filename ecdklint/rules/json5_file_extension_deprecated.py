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
Using `.json5` as file extension is deprecated and support for it will be
removed in the next major release of ecdk.
"""

import os.path

from ecdklint.linter import LintProblem

ID = "json5-file-extension-deprecated"
TYPE = "file"
CONF: dict[str, str] = {
}
DEFAULT: dict[str, str] = {
}

def check(conf, data, filepath):
    if os.path.basename(filepath).endswith('.json5'):
        yield LintProblem(1, 1, '.json5 file extension is deprecated, use .json instead')
    