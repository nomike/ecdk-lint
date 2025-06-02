# Copyright (C) 2016 Adrien Vergé
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

import os
import unittest

import yaml

from ecdklint import linter
from ecdklint.config import ECdkLintConfig


# Miscellaneous stuff:
class RuleTestCase(unittest.TestCase):
    def get_test_file_path(self, filename) -> str:
        return os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "test_files", filename
        )

    def get_test_file_content(self, filename) -> str:
        with open(self.get_test_file_path(filename), "r") as file:
            return file.read()

    def build_fake_config(self, conf):
        print(f"#####{conf}#####")
        if conf is None:
            conf = {}
        else:
            conf = yaml.safe_load(conf)
        conf = {"extends": "default", "rules": conf}
        return ECdkLintConfig(yaml.safe_dump(conf))

    def check(self, source, conf, **kwargs):
        expected_problems = []
        for key in kwargs:
            assert key.startswith("problem")
            if len(kwargs[key]) > 3:
                if kwargs[key][3] == "syntax":
                    rule_id = None
                else:
                    rule_id = kwargs[key][3]
            else:
                rule_id = self.rule_id
            expected_problems.append(
                linter.LintProblem(
                    kwargs[key][0], kwargs[key][1], desc=kwargs[key][2], rule=rule_id
                )
            )
        expected_problems.sort()
        real_problems = list(linter.run(source, self.build_fake_config(conf)))
        print(real_problems)
        self.assertEqual(real_problems, expected_problems)
