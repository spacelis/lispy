#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: test_core.py
Author: SpaceLis
Email: Wen.Li@tudelft.nl
GitHub: http://github.com/spacelis
Description:

"""

from lispy.core import execute, PlusOperator, LambdaOperator


def test_op():
    code = (PlusOperator(), '1', '2')
    print execute(code)


def test_lambda():
    code = (((LambdaOperator(), ('a', 'b'),
              (PlusOperator(), 'a'), 'b'), '3'), '1')
    print execute(code)


def test_lambda_lambda():
    code = (LambdaOperator(), ('add',), (('add', '1'), '2')), PlusOperator()
    print execute(code)


def test_lambda_complex():
    code = ((LambdaOperator(), ('code',),
             ((LambdaOperator(), ('define',), 'code'),
              (LambdaOperator(), ('n', 'b', 'c'),
               (LambdaOperator(), ('n',), 'c'), 'b'))),
            ('define', 'add',
             (LambdaOperator(), ('a', 'b'), (PlusOperator(), 'a'), 'b'),
             (('add', '1'), '2')))
    print execute(code)


if __name__ == '__main__':
    #test_lambda_lambda()
    test_lambda_complex()
    #test_lambda()
