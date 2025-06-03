# Copyright (C) 2023–2025 Jason Yundt
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

from ecdklint.rules import (dummy, parameters_missing, region_invalid,
                            region_missing, region_stackname_mismatch,
                            stack_module_missing, stackname_too_long)

_RULES = {
    region_missing.ID: region_missing,
    region_invalid.ID: region_invalid,
    region_stackname_mismatch.ID: region_stackname_mismatch,
    stack_module_missing.ID: stack_module_missing,
    dummy.ID: dummy,
    parameters_missing.ID: parameters_missing,
    stackname_too_long.ID: stackname_too_long,
}


def get(id):
    if id not in _RULES:
        raise ValueError(f'no such rule: "{id}"')

    return _RULES[id]
