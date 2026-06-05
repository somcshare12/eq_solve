import math
import os
import tempfile
import unittest

from sparser import Code_Parser


class CodeParserTest(unittest.TestCase):
    def make_parser(self, source):
        fd, path = tempfile.mkstemp(text=True)
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(source)
        self.addCleanup(os.remove, path)
        return Code_Parser(path)

    def test_parse_assignments_in_order(self):
        parser = self.make_parser("x=1; y = x + 2; f = y^2 + sin(pi);")

        variables = parser.parse()

        self.assertEqual(variables["x"], 1)
        self.assertEqual(variables["y"], 3)
        self.assertAlmostEqual(parser.get_vaLue("f"), 9 + math.sin(math.pi))

    def test_parser_instances_do_not_share_variables(self):
        first = self.make_parser("x=1;")
        second = self.make_parser("y=2;")

        first.parse()
        second.parse()

        self.assertIn("x", first.variables)
        self.assertNotIn("x", second.variables)

    def test_invalid_assignment_raises_error(self):
        parser = self.make_parser("x + 1;")

        with self.assertRaises(ValueError):
            parser.parse()


if __name__ == "__main__":
    unittest.main()