import unittest
from unittest import TestCase

import re

from function_parser.lexis.lexis_analyzer import LexisAnalyzer
from function_parser.lexis.lexis_element import LexisElement


class LexisAnalyzerTests(TestCase):
    def test_analyze(self):
        # arrange
        analyzer = LexisAnalyzer(
            [
                lambda s: [LexisElement('sin', 'function name')] if s.startswith('sin') else [],
                lambda s: [LexisElement('(', 'opening brace')] if s.startswith('(') else [],
                lambda s: [LexisElement(')', 'closing brace')] if s.startswith(')') else [],
                lambda s: [LexisElement(l[0], 'constant value') for l in re.findall(r'^([\d]+(.[\d]+)?)', s)]
            ]
        )

        # act
        data = analyzer.analyze("sin(1)")

        # assert
        self.assertEqual(data, [
            [LexisElement("sin", "function name")],
            [],
            [],
            [LexisElement("(", "opening brace")],
            [LexisElement("1", "constant value")],
            [LexisElement(")", "closing brace")],
        ])

if __name__ == "__main__":
    unittest.main()