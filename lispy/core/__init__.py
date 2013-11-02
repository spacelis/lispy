#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" The core module of lipy.

File: __init__.py
Author: SpaceLis
Email: Wen.Li@tudelft.nl
GitHub: http://github.com/spacelis
Description:

    This package is the core package of the python implementation
    of LISP. The following concepts are formalized. Everything is
    a function which means they can be APPLY_TO a list (an empty
    one or not). Symbols and SymbolLists are functions taking no
    arguments. LambdaOperator is indeed an operator for constructing
    a LambdaFunction. LambdaFunctions are the real function could and
    should be applied on later lists.

"""


class Function(object):  # pylint: disable-msg=R0903

    """ Function is the root entity of everything."""

    def apply_to(self, xs):
        """ A general method to apply a function.

        This will insure when function evaluated with no argument
        will give back it self.

        """
        if xs.isEmpty():
            return self
        else:
            return self.apply_to_one(xs)

    def apply_to_one(self, xs):
        """ The abstract method that need to be override in subclasses.

        Functions have the ability to be applied to some value. Hence,
        in lispy, that is usually a SymbolList.

        :returns: A new Funtion type (Symbol or SymbolList usually)

        """
        raise NotImplementedError

    def __repr__(self):
        """ A string representing this object for debug.

        :returns: a string representation

        """
        return "%s (%s)" % (self.__class__.__name__, self.__str__())


class Symbol(Function):

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

    def __str__(self):
        """ Symbol( x ).

        :returns: Symbol Name as Symbol( x )

        """
        return str(self._literate)


class SymbolList(Symbol):

    """ SymbolList is a list of Symbol.

    Symbolists are the core data structure for evaluation represented as both
    code and data. They are able to be applied to an argument which can also be
    a SymbolList.

    """

    def __init__(self, xs=()):
        """ Constructing a SymbolList for a literate list().

        :xs: A list() of Symbols.

        """
        super(SymbolList, self).__init__(xs)

    def apply_to(self, xs):
        if self.isAtom():
            return self.head().apply_to(NilSymbolList).apply_to(xs)
        return self.head().apply_to(self.tail()).apply_to(xs)

    def head(self):
        """ Return the head of the list.

        :returns: The first element

        """
        return self._literate[0]

    def tail(self):
        """ Return the tail of SymbolList.

        :returns: A new SymbolList with all elements but first.

        """
        return SymbolList(self._literate[1:])

    def replace(self, k, v):
        """ Replace all occurance of k in the list with v.

        :k: The target Symbol to be replaced
        :v: The replacement that will be replaced with
        :returns: A new SymbolList with replacements

        """
        return SymbolList([s.replace(k, v) for s in self._literate])

    def isEmpty(self):
        """ True when SymbolList contains no element.

        :returns: Whether this SymbolList is empty

        """
        return len(self._literate) == 0

    def isAtom(self):
        """ True when SymbolList contains only one element.

        :returns: Whether this SymbolList is atom

        """
        return len(self._literate) == 1

    def __str__(self):
        """ The string representation of SymbolList.

        :returns: A string

        """
        return '[%s]' % (', '.join([str(x) for x in self._literate]), )


# The empty SymbolList as a helper object.
NilSymbolList = SymbolList()


class AddXOperator(Symbol):  # pylint: disable-msg=R0903

    """Docstring for UniPlus. """

    def __init__(self, x):
        super(AddXOperator, self).__init__()
        self._X = x

    def apply_to_one(self, xs):
        """ Add held with to the evaluation of the rest.

        :returns: The added value.

        """
        return Symbol(self._X.getLiterate() +
                      xs.apply_to(NilSymbolList).getLiterate())

    def __str__(self):
        """ Representation of AddX.

        :returns: A string

        """
        return 'F_[Add_%s]' % (str(self._X), )


class PlusOperator(Symbol):  # pylint: disable-msg=R0903

    """ Mathimetical plus operator for numbers.

    This is a built-in functions to add up numbers.

    """

    def __init__(self):
        super(PlusOperator, self).__init__()

    def apply_to_one(self, xs):
        """ Return a new function that the held value to an argument.

        :returns: A function lambda a: x + a

        """
        return AddXOperator(xs.apply_to(NilSymbolList))

    def __str__(self):
        """ Representation of plus operator.

        :returns: A string

        """
        return 'F<+>'


#class OpCar(Function):
    #pass


#class OpCdr(Function):
    #pass


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
        if self._para.isEmpty():
            return self._body.apply_to(NilSymbolList)
        else:
            var = self._para.head().apply_to(NilSymbolList)
            nb = self._body.replace(var, xs.apply_to(NilSymbolList))
            return LambdaFunction(self._para.tail(), nb)

    def __str__(self):
        """ Representation of LambdaFunction.

        :returns: A string.

        """
        return 'L %s: %s' % (self._para, self._body)


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
        return LambdaFunction(xs.head(), xs.tail())

    def __str__(self):
        """ Representation of lambda operator.

        :returns: A string.

        """
        return 'lambda'


#class DefineOperator(Function):
    #""" define x y * = (lambda x: *) y"""
    #pass


# TODO make lispy version
def symbolize(source):
    """ Make symbol lists out of source.

    :source: A list of strings that can be translate to symbols
    :returns: A symbol list

    """
    code = list()
    for x in source:
        if isinstance(x, str):
            try:
                code.append(Symbol(int(x)))
            except ValueError:
                code.append(Symbol(x))
        elif isinstance(x, tuple):
            code.append(symbolize(x))
        else:
            code.append(x)
    return SymbolList(tuple(x for x in code))


def execute(source):
    """ Running the source code.

    :source: The unsymbolized source code to run.

    """
    return symbolize(source).apply_to(NilSymbolList)
