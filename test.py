import unittest
from format import format as _


class TestFormat(unittest.TestCase):
    def test_format(self):
        k1 = 'val1'
        k2 = 'val2'

        class A:
            a = 'class'
        k4 = A()

        asserts = (
            ('val1 & val2', _('{k1} & {k2}')),
            ('val1val2', _('{k1}{k2}')),
            ('val1', _('{k1}{k3}')),
            ('class+val2', _('{k4.a}+{k2}')),
        )

        for expected, value in asserts:
            print(expected, value)
            self.assertEqual(expected, value)


if __name__ == '__main__':
    unittest.main()
