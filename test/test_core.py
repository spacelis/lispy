#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" A test moudule.

File: test_core.py
Author: SpaceLis
Email: Wen.Li@tudelft.nl
GitHub: http://github.com/spacelis
Description:

"""

from lispy.core import execute
from lispy.core import PlusOperator
from lispy.core import LambdaOperator as L
from lispy.core import symbolize
import unittest


class TestCore(unittest.TestCase):  # pylint: disable-msg=R0904

    """Docstring for TestCore. """

    def test_symbolize(self):
        """ test_symbolize. """
        code = (L(), 'x', 'y'), 'z'
        self.assertEqual(
            str(symbolize(code)),
            "[[<lambda>, 'x, 'y, NIL], 'z, NIL]")

    def test_lambda(self):
        """ test_lambda. """
        code = (L(), 'x', 'x'), 'z'
        self.assertEqual(
            execute(code).getLiterate(),  # pylint: disable-msg=E1103
            'z')

    def test_op(self):
        """ test_op. """
        code = (L(), 'x', L(), 'y', PlusOperator()), '1', '2'
        self.assertEqual(
            execute(code).getLiterate(),  # pylint: disable-msg=E1103
            3)

    def test_lambda_lambda(self):
        """ test_lambda_lambda. """
        code = (L(), '+', ('+', '1', '2')), (L(), 'x', L(), 'y',
                                             PlusOperator())
        self.assertEqual(
            execute(code).getLiterate(),  # pylint: disable-msg=E1103
            3)

    def test_lambda_lib(self):
        """ test_lambda_lib. """
        lib = (L(), 'code', (L(), '\\', L(), '+', 'code'),
               L(), (L(), 'x', L(), 'y', PlusOperator()))
        code = (lib, (('\\', 'a', '\\', 'b', '+', 'a', 'b'), '1', '2'))
        self.assertEqual(
            execute(code).getLiterate(),  # pylint: disable-msg=E1103
            3)


if __name__ == '__main__':
    unittest.main()
