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
The region specified in the tags must match the stack-region.
"""

import os.path

from ecdklint.linter import LintProblem

ID = "region-mismatch-stack-tags"
TYPE = "file"
CONF: dict[str, str] = {
}
DEFAULT: dict[str, str] = {
}

def check(conf, data, filepath):
    if "Region" in data.keys() and "Tags" in data.keys() and "psc:Region" in data['Tags']:
        if data['Region'] != data['Tags']['psc:Region']:
            yield LintProblem(1, 1, 'Region in parameters and tags differ.')
    