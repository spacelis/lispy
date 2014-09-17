#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" The core module of lipy.

File: __init__.py
Author: SpaceLis
Email: Wen.Li@tudelft.nl
GitHub: http://github.com/spacelis
Description:

    This package is the core package of the python implementation
    of LISP. The following concepts are formalized.

    Everything is a function which means they can be APPLY_TO a list
    (an empty one or not). Symbols are basic stuctures for both code
    and data. LambdaOperator is indeed an operator for constructing a
    LambdaFunction from a list of code (SymbolList). LambdaFunctions are
    the constructed function could and should be applied on later lists.

    Following are the theroms.

    Nil(_) -> Nil
    x::xs(ys) -> x(xs)(ys)

    {lambda x: xs}(y::ys) -> {x->y}(xs)(ys)
    {lambda x: xs}(Nil) -> {lambda x: xs}

    op(x::xs) -> op(x)(xs)
    op(Nil) -> ERROR

    L(x::xs) -> {lambda x: xs}
    L(Nil) -> ERROR

"""


class Function(object):  # pylint: disable-msg=R0903

    """ Function is the root entity of everything."""

    def apply_to(self, xs):
        """ A general method to apply a function. """
        raise NotImplementedError

    def __repr__(self):
        """ A string representing this object for debug.

        :returns: a string representation

        """
        return self.__str__()


class Symbol(Function):  # pylint: disable-msg=W0223

    """ Symbol is the basic entity that wrapping values as a function.

    self._literate is the boxing value of a symbol. Whent the symbol
    is a non-args function which always returning it self.

    """

    def replace(self, k, v):
        """ Replacing self for another Symbol.

        This funciton is a helper function for LambdaFunction.

        :k: The target symbol to replace
        :v: The symbol being replaced with
        :return: v, in case that self==k else returns self

        """
        return v if self == k else self

    def __eq__(self, o):
        """ Compare two symbols whether they are equal.

        The equality is based on the Symbol Name return from object.__str__

        :o: @todo
        :returns: @todo

        """
        return repr(self) == repr(o)


class SymbolAtom(Symbol):

    """ Symbol is the basic entity that wrapping values as a function.

    self._literate is the boxing value of a symbol. Whent the symbol
    is a non-args function which always returning it self.

    """

    def __init__(self, literate=None):
        self._literate = literate

    def getLiterate(self):
        """ Return the literate value of this symbol.

        :returns: self._literate

        """
        return self._literate

    def apply_to(self, xs):
        """ Leave undefined.

        :xs: @todo
        :returns: @todo

        """
        if isinstance(xs, NilSymbolList):
            return self
        raise NotImplementedError

    def __str__(self):
        """ Representation of SymbolAtom.

        :returns: Symbol Name as 'x or number itself

        """
        if isinstance(self._literate, str):
            return "'" + str(self._literate)
        else:
            return str(self._literate)


class SymbolList(Symbol):

    """ SymbolList is a list of Symbol.

    Symbolists are the core data structure for evaluation represented as both
    code and data. They are able to be applied to an argument which can also be
    a SymbolList.

    """

    def __init__(self, head, tail):
        """ Constructing a SymbolList for a literate list().

        :head: A symbol as the first element.
        :tail: A list of symbol as the rest of list.

        """
        super(SymbolList, self).__init__()
        self._head = head
        self._tail = tail

    def apply_to(self, xs):
        return self.head().apply_to(self.tail()).apply_to(xs)

    def head(self):
        """ Return the head of the list.

        :returns: The first element

        """
        return self._head

    def tail(self):
        """ Return the tail of SymbolList.

        :returns: A new SymbolList with all elements but first.

        """
        return self._tail

    def replace(self, k, v):
        """ Replace all occurance of k in the list with v.

        :k: The target Symbol to be replaced
        :v: The replacement that will be replaced with
        :returns: A new SymbolList with replacements

        """
        return SymbolList(self._head.replace(k, v),
                          self._tail.replace(k, v))

    def __str__(self):
        """ The string representation of SymbolList.

        :returns: A string

        """
        return '[%s, %s]' % (str(self._head), str(self._tail)[1:-1])


# The empty SymbolList as a helper object.
class NilSymbolList(Symbol):  # pylint: disable-msg=R0903

    """ A symbol list contains nothing. """

    def __init__(self):
        """ Constructing a SymbolList for a literate list(). """
        super(NilSymbolList, self).__init__()

    def apply_to(self, xs):
        """ Return self as a NilSymbolList. """
        return self

    def replace(self, k, v):
        """ Return self as no elements will be replaced. """
        return self

    def __str__(self):
        """ Representation of NilSymbolList.

        :returns: NilSymbolList

        """
        return '[NIL]'


class LambdaFunction(Symbol):  # pylint: disable-msg=R0903

    """ The function objects that are constructed from lambda expression.

    This is the core structure for representing control flow of codes in lispy.

    """

    def __init__(self, para, body):
        """ Initialize with a list of parameters and a funciton body.

        :para: A list of symbols that used as indicator of future values.
        :body: A list of symbols representing the process on the parameters.
        :returns: A function object holding both the parameters and body.

        """
        super(LambdaFunction, self).__init__()
        self._para = para
        self._body = body

    def apply_to(self, xs):
        """ Apply the lambda function to one parameter.

        :xs: A Symbol as the first parameter to the function.
        :returns: A new function if the there is more parameters to fill in.
        Otherwise evaluates to the value.

        """
        if isinstance(xs, NilSymbolList):
            return self
        return self._body.replace(self._para, xs.head()).apply_to(xs.tail())

    def __str__(self):
        """ Representation of LambdaFunction.

        :returns: A string.

        """
        return '(%s -> %s)' % (self._para, self._body)


class LambdaOperator(Symbol):  # pylint: disable-msg=R0903

    """ LambdaOperator is an operator for defining a lambda funciton.

    LambdaOperator takes the head of its tail as a list of parameters
    and the tail of tail as body of the function.

    """

    def __init__(self):
        super(LambdaOperator, self).__init__()

    def apply_to(self, xs):
        """ Applying this operator will construct a lambda function object.

        :xs: the head of which is going to be a parameter list and
        the tail of which is going to be the body of the function

        """
        if isinstance(xs, NilSymbolList):
            raise ValueError('LambdaOperator requires a parameter.')
        return LambdaFunction(xs.head(), xs.tail())

    def __str__(self):
        """ Representation of lambda operator.

        :returns: A string.

        """
        return '<lambda>'


class BinaryOperator(Symbol):  # pylint: disable-msg=R0903

    """ Mathimetical plus operator for numbers.

    This is a built-in functions to add up numbers.

    """

    def __init__(self, x=None, y=None):
        super(BinaryOperator, self).__init__()
        self._x = x
        self._y = y
        self._op = None

    def apply_to(self, xs):
        """ Return a new function that the held value to an argument.

        :returns: A function lambda a: x + a

        """
        return SymbolAtom(self.op(self._x.getLiterate(),
                                  self._y.getLiterate())).apply_to(xs)

    def op(self, x, y):
        """ The abstract method for doing the operation

        :x: Left Oprand
        :y: Right Oprand
        :returns: x op y

        """
        raise NotImplementedError

    def replace(self, k, v):
        """ Add oprand to this operator.

        :k: Not used.
        :v: The oprand to this operator.
        :returns: a replace/original Operator function

        """
        if k == SymbolAtom('x'):
            return self.__class__(v, self._y)
        elif k == SymbolAtom('y'):
            return self.__class__(self._x, v)
        else:
            return self

    def __str__(self):
        """ Representation of plus operator.

        :returns: A string

        """
        return '<%s%s>' % \
            (self._op, ' '.join((str(i) for i in [self._x, self._y] if i)), )


class PlusOperator(BinaryOperator):

    """ Plus. """

    def __init__(self, x=None, y=None):
        """@todo: to be defined1. """
        super(PlusOperator, self).__init__(x, y)
        self._op = '+'

    def op(self, x, y):
        """ Add the two numbers

        :x: Left oprand.
        :y: Right oprand.
        :returns: @todo

        """
        return x + y


class SubtractOperator(BinaryOperator):

    """ Multiplication. """

    def __init__(self, x=None, y=None):
        """@todo: to be defined1. """
        super(SubtractOperator, self).__init__(x, y)
        self._op = '-'

    def op(self, x, y):
        """ Add the two numbers

        :x: Left oprand.
        :y: Right oprand.
        :returns: @todo

        """
        return x - y


class MultiplyOperator(BinaryOperator):

    """ Multiplication. """

    def __init__(self, x=None, y=None):
        """@todo: to be defined1. """
        super(MultiplyOperator, self).__init__(x, y)
        self._op = '*'

    def op(self, x, y):
        """ Add the two numbers

        :x: Left oprand.
        :y: Right oprand.
        :returns: @todo

        """
        return x * y


class DivideOperator(BinaryOperator):

    """ Multiplication. """

    def __init__(self, x=None, y=None):
        """@todo: to be defined1. """
        super(DivideOperator, self).__init__(x, y)
        self._op = '/'

    def op(self, x, y):
        """ Add the two numbers

        :x: Left oprand.
        :y: Right oprand.
        :returns: @todo

        """
        return x / y


class CarOperator(Symbol):

    """ car return the head of a list. """

    def __init__(self):
        """ __init__
        :returns: @todo

        """
        super(CarOperator, self).__init__()

    def apply_to(self, xs):
        """ Return the head of the list

        :xs: A given SymbolList
        :returns: @todo

        """
        return xs.head()


# TODO add quote sematics for car cdr cons operators
class CdrOperator(Symbol):

    """ cdr return the head of a list. """

    def __init__(self):
        """ __init__
        :returns: @todo

        """
        super(CdrOperator, self).__init__()

    def apply_to(self, xs):
        """ Return the tail of the list

        :xs: A given SymbolList
        :returns: @todo

        """
        return xs.tail()


# TODO make lispy version
def symbolize(source):
    """ Make symbol lists out of source.

    :source: A list of strings that can be translate to symbols
    :returns: A symbol list

    """
    if len(source) > 0:
        x = source[0]
        if isinstance(x, str):
            try:
                x = int(x)
            except ValueError:
                pass
            return SymbolList(SymbolAtom(x), symbolize(source[1:]))
        elif isinstance(x, tuple):
            return SymbolList(symbolize(x), symbolize(source[1:]))
        else:
            return SymbolList(x, symbolize(source[1:]))
    else:
        return NilSymbolList()


def execute(source):
    """ Running the source code.

    :source: The unsymbolized source code to run.

    """
    return symbolize(source).apply_to(NilSymbolList())
