#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Array Utilities
===============

Defines array utilities objects.
"""

from __future__ import division, unicode_literals

import numpy as np

__author__ = 'Colour Developers'
__copyright__ = 'Copyright (C) 2013-2017 - Colour Developers'
__license__ = 'New BSD License - http://opensource.org/licenses/BSD-3-Clause'
__maintainer__ = 'Colour Developers'
__email__ = 'colour-science@googlegroups.com'
__status__ = 'Production'

__all__ = ['tstack',
           'tsplit']


def tstack(a):
    """
    Stacks arrays in sequence along the last axis (tail).

    Rebuilds arrays divided by :func:`tsplit`.

    Parameters
    ----------
    a : array_like
        Array to perform the stacking.

    Returns
    -------
    ndarray

    See Also
    --------
    tsplit

    Examples
    --------
    >>> a = 0
    >>> tstack((a, a, a))
    array([0, 0, 0])
    >>> a = np.arange(0, 6)
    >>> tstack((a, a, a))
    array([[0, 0, 0],
           [1, 1, 1],
           [2, 2, 2],
           [3, 3, 3],
           [4, 4, 4],
           [5, 5, 5]])
    >>> a = np.reshape(a, (1, 6))
    >>> tstack((a, a, a))
    array([[[0, 0, 0],
            [1, 1, 1],
            [2, 2, 2],
            [3, 3, 3],
            [4, 4, 4],
            [5, 5, 5]]])
    >>> a = np.reshape(a, (1, 1, 6))
    >>> tstack((a, a, a))
    array([[[[0, 0, 0],
             [1, 1, 1],
             [2, 2, 2],
             [3, 3, 3],
             [4, 4, 4],
             [5, 5, 5]]]])
    """

    a = np.asarray(a)

    return np.concatenate([x[..., np.newaxis] for x in a], axis=-1)


def tsplit(a):
    """
    Splits arrays in sequence along the last axis (tail).

    Parameters
    ----------
    a : array_like
        Array to perform the splitting.

    Returns
    -------
    ndarray

    See Also
    --------
    tstack

    Examples
    --------
    >>> a = np.array([0, 0, 0])
    >>> tsplit(a)
    array([0, 0, 0])
    >>> a = np.array([[0, 0, 0],
    ...               [1, 1, 1],
    ...               [2, 2, 2],
    ...               [3, 3, 3],
    ...               [4, 4, 4],
    ...               [5, 5, 5]])
    >>> tsplit(a)
    array([[0, 1, 2, 3, 4, 5],
           [0, 1, 2, 3, 4, 5],
           [0, 1, 2, 3, 4, 5]])
    >>> a = np.array([[[0, 0, 0],
    ...                [1, 1, 1],
    ...                [2, 2, 2],
    ...                [3, 3, 3],
    ...                [4, 4, 4],
    ...                [5, 5, 5]]])
    >>> tsplit(a)
    array([[[0, 1, 2, 3, 4, 5]],
    <BLANKLINE>
           [[0, 1, 2, 3, 4, 5]],
    <BLANKLINE>
           [[0, 1, 2, 3, 4, 5]]])
    """

    a = np.asarray(a)

    return np.array([a[..., x] for x in range(a.shape[-1])])
