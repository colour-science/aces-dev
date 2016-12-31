#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Common Utilities
================

Defines common utilities objects that don't fall in any specific category.
"""

from __future__ import division, unicode_literals

from copy import deepcopy
import sys

__author__ = 'Colour Developers'
__copyright__ = 'Copyright (C) 2013-2016 - Colour Developers'
__license__ = 'New BSD License - http://opensource.org/licenses/BSD-3-Clause'
__maintainer__ = 'Colour Developers'
__email__ = 'colour-science@googlegroups.com'
__status__ = 'Production'

__all__ = ['filter_kwargs']


def filter_kwargs(function, **kwargs):
    """
    Filters keyword arguments incompatible with the given function signature.

    Parameters
    ----------
    function : callable
        Callable to filter the incompatible keyword arguments.

    Other Parameters
    ----------------
    \**kwargs : dict, optional
        Keywords arguments.

    Returns
    -------
    dict
        Filtered keyword arguments.

    Examples
    --------
    >>> def fn_a(a):
    ...     return a
    >>> def fn_b(a, b=0):
    ...     return a, b
    >>> def fn_c(a, b=0, c=0):
    ...     return a, b, c
    >>> fn_a(1, **filter_kwargs(fn_a, b=2, c=3))
    1
    >>> fn_b(1, **filter_kwargs(fn_b, b=2, c=3))
    (1, 2)
    >>> fn_c(1, **filter_kwargs(fn_c, b=2, c=3))
    (1, 2, 3)
    """

    kwargs = deepcopy(kwargs)
    if sys.version_info[0] >= 3:
        args = function.__code__.co_varnames
    else:
        args = function.func_code.co_varnames

    args = set(kwargs.keys()) - set(args)
    for key in args:
        kwargs.pop(key)

    return kwargs
