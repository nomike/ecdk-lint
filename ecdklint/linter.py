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

import io
import re

import json5 as json

from ecdklint import decoder

PROBLEM_LEVELS = {
    0: None,
    1: "warning",
    2: "error",
    None: 0,
    "warning": 1,
    "error": 2,
}

DISABLE_RULE_PATTERN = re.compile(r"^# ecdklint disable( rule:\S+)*\s*$")
ENABLE_RULE_PATTERN = re.compile(r"^# ecdklint enable( rule:\S+)*\s*$")


class LintProblem:
    """Represents a linting problem found by ecdklint."""

    def __init__(self, line, column, desc="<no description>", rule=None):
        #: Line on which the problem was found (starting at 1)
        self.line = line
        #: Column on which the problem was found (starting at 1)
        self.column = column
        #: Human-readable description of the problem
        self.desc = desc
        #: Identifier of the rule that detected the problem
        self.rule = rule
        self.level = None

    @property
    def message(self):
        if self.rule is not None:
            return f"{self.desc} ({self.rule})"
        return self.desc

    def __eq__(self, other):
        return (
            self.line == other.line
            and self.column == other.column
            and self.rule == other.rule
        )

    def __lt__(self, other):
        return self.line < other.line or (
            self.line == other.line and self.column < other.column
        )

    def __repr__(self):
        return f"{self.line}:{self.column}: {self.message}"


def get_cosmetic_problems(buffer, conf, filepath):
    rules = conf.enabled_rules(filepath)

    file_rules = [r for r in rules if r.TYPE == "file"]

    cache = []
    try:
        data = json.loads(buffer)
    except ValueError as e:
        # If the file could not be parsed as a json5 document, there is no sense in checking additional rules.
        # As the json5 parsing problem is already reported by the get_syntax_error() function we can just return here.
        return
    for rule in file_rules:
        rule_conf = conf.rules[rule.ID]
        for problem in rule.check(rule_conf, data, filepath):
            problem.rule = rule.ID
            problem.level = rule_conf["level"]
            cache.append(problem)

        # This is the last token/comment/line of this line, let's flush the
        # problems found (but filter them according to the directives)
        for problem in cache:
            yield problem

        cache = []


def get_syntax_error(buffer):
    try:
        list(json.loads(buffer))
    except ValueError as e:
        problem = LintProblem(
            1, 1, "syntax error: " + ", ".join(e.args) + " (syntax)"
        )
        problem.level = "error"
        return problem


def _run(buffer, conf, filepath):
    assert hasattr(
        buffer, "__getitem__"
    ), "_run() argument must be a buffer, not a stream"
    if isinstance(buffer, bytes):
        buffer = decoder.auto_decode(buffer)

    # If the document contains a syntax error, save it and yield it at the
    # right line
    syntax_error = get_syntax_error(buffer)

    for problem in get_cosmetic_problems(buffer, conf, filepath):
        # Insert the syntax error (if any) at the right place...
        if (
            syntax_error
            and syntax_error.line <= problem.line
            and syntax_error.column <= problem.column
        ):
            yield syntax_error

            # Discard the problem since it is at the same place as the syntax
            # error and is probably redundant (and maybe it's just a 'warning',
            # in which case the script won't even exit with a failure status).
            syntax_error = None
            continue

        yield problem

    if syntax_error:
        yield syntax_error


def run(input, conf, filepath=None):
    """Lints an ecdk source.

    Returns a generator of LintProblem objects.

    :param input: buffer, string or stream to read from
    :param conf: ecdklint configuration object
    """
    if filepath is not None and conf.is_file_ignored(filepath):
        return ()

    if isinstance(input, (bytes, str)):
        return _run(input, conf, filepath)
    elif isinstance(input, io.IOBase):
        # We need to have everything in memory to parse correctly
        content = input.read()
        return _run(content, conf, filepath)
    else:
        raise TypeError("input should be a string or a stream")
