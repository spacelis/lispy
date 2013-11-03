#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
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


def test_symbolize():
    code = (PlusOperator(), '1', '2')
    print symbolize(code)


def test_op():
    code = ((PlusOperator(), '1'), '2')
    print execute(code)


def test_op2():
    code = (PlusOperator(), '1', '2')
    print execute(code)


def test_lambda():
    code = ((LambdaOperator(), 'a', LambdaOperator(), 'b',
             PlusOperator(), 'a', 'b'), '3', '1')
    print execute(code)


def test_lambda_lambda():
    code = (LambdaOperator(), 'add', (('add', '1'), '2')), PlusOperator()
    print execute(code)


def test_lambda_lib():
    lib = (L(), 'code', ((L(), '\\', L(), '+', 'code'), L(), PlusOperator()))
    code = (lib, (('\\', 'a', '\\', 'b', '+', 'a', 'b'), '1', '2'))
    print execute(code)


if __name__ == '__main__':
    #test_symbolize()
    #test_op()
    #test_op2()
    #test_lambda()
    #test_lambda_lambda()
    test_lambda_lib()
