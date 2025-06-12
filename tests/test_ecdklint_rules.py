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
        conf = "region-missing: enable"
        self.check(
            self.get_test_file_content("region-missing.json"),
            conf,
            problem=(1, 1, "no region in stack config", "region-missing")
        )

    def test_empty_json(self):
        conf = "region-missing: enable"
        self.check(
            self.get_test_file_content("empty.json"),
            conf,
            problem=(1, 1, "syntax error: Empty strings are not legal JSON5", "syntax"),
        )

    def test_parameters_missing(self):
        conf = "parameters-missing: enable"
        self.check(
            self.get_test_file_content("parameters-missing.json"),
            conf,
            problem=(1, 1, "Parameters section is missing", "parameters-missing")
        )

    def test_stackname_too_long(self):
        conf = "stackname-too-long: enable"
        self.check(
            self.get_test_file_content("stack-name-too-long-test-file-1234567890-1234567890-1234567890-1234567890-1234567890-1234567890-1234567890-1234567890-1234567890-1234567890-1234567890-1234567890-1234567890-1234567890.json"),
            conf,
            problem1=(1, 1, "stack name is too long", "stackname-too-long"),
            filepath="tests/test_files/stack-name-too-long-test-file-1234567890-1234567890-1234567890-1234567890-1234567890-1234567890-1234567890-1234567890-1234567890-1234567890-1234567890-1234567890-1234567890-1234567890.json"
        )
    
    def test_stack_class_missing(self):
        conf = "stack-class-missing: enable"
        self.check(
            self.get_test_file_content("empty-dict.json"),
            conf,
            problem=(1, 1, "stack has no stack class", "stack-class-missing")
        )

    def test_stack_module_missing(self):
        conf = "stack-module-missing: enable"
        self.check(
            self.get_test_file_content("empty-dict.json"),
            conf,
            problem=(1, 1, "stack has no stack module", "stack-module-missing")
        )

    def test_stackname_doesnt_match_module_and_class(self):
        conf = "stackname-doesnt-match-module-and-class: enable"
        self.check(
            self.get_test_file_content("stackname-doesnt-match-module-and-class.json"),
            conf,
            problem=(1, 1, "stack name does not match module and class name", "stackname-doesnt-match-module-and-class"),
            filepath="tests/test_files/stackname-doesnt-match-module-and-class.json"
        )

    def test_json5_fileextension_deprecated(self):
        conf = "json5-file-extension-deprecated: enable"
        self.check(
            "{}",
            conf,
            problem=(1, 1, ".json5 file extension is deprecated, use .json instead", "json5-file-extension-deprecated"),
            filepath="tests/test_files/test.json5"
        )

    def test_region_mismatch_stack_tags(self):
        conf = "region-mismatch-stack-tags: enable"
        self.check(
            self.get_test_file_content("region-mismatch-stack-tags.json"),
            conf,
            problem=(1, 1, "Region in parameters and tags differ.", "region-mismatch-stack-tags"),
        )
