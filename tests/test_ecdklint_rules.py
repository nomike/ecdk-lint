# Copyright (C) 2016 Adrien Vergé
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

from tests.common import RuleTestCase


class ECdkLintRulesTestCase(RuleTestCase):
    def test_region_missing(self):
        conf = "region_missing: enable"
        self.check(
            self.get_test_file_content("region_missing.json"),
            conf,
            problem1=(1, 1, "no region in stack config", "region_missing"),
            problem2=(1, 1, "stack has no stack module", "stack_module_missing"),
        )
