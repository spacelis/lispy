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
from lispy.core import SubtractOperator
from lispy.core import MultiplyOperator
from lispy.core import DivideOperator
from lispy.core import CarOperator
from lispy.core import CdrOperator
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

    def test_plus(self):
        """ test_plux. """
        code = (L(), 'x', L(), 'y', PlusOperator()), '2', '3'
        self.assertEqual(
            execute(code).getLiterate(),  # pylint: disable-msg=E1103
            5)

    def test_subtract(self):
        """ test_subtract. """
        code = (L(), 'x', L(), 'y', SubtractOperator()), '7', '3'
        self.assertEqual(
            execute(code).getLiterate(),  # pylint: disable-msg=E1103
            4)

    def test_mul(self):
        """ test_mul. """
        code = (L(), 'x', L(), 'y', MultiplyOperator()), '3', '2'
        self.assertEqual(
            execute(code).getLiterate(),  # pylint: disable-msg=E1103
            6)

    def test_divide(self):
        """ test_op. """
        code = (L(), 'x', L(), 'y', DivideOperator()), '242', '11'
        self.assertEqual(
            execute(code).getLiterate(),  # pylint: disable-msg=E1103
            22)

    def test_car(self):
        """ test car. """
        code = CarOperator(), 'x', 'y', 'z'
        self.assertEqual(
            str(execute(code)),
            "'x")

    def test_cdr(self):
        """ test cdr. """
        code = CdrOperator(), 'x', 'y', 'z'
        self.assertEqual(
            str(execute(code)),
            "['y, 'z, NIL]")

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
