#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Data Structures
===============

Defines various data structures classes:

-   :class:`CaseInsensitiveMapping`: A case insensitive mapping allowing values
    retrieving from keys while ignoring the key case.
"""

from __future__ import division, unicode_literals

from collections import Mapping, MutableMapping

__author__ = 'Colour Developers'
__copyright__ = 'Copyright (C) 2013-2017 - Colour Developers'
__license__ = 'New BSD License - http://opensource.org/licenses/BSD-3-Clause'
__maintainer__ = 'Colour Developers'
__email__ = 'colour-science@googlegroups.com'
__status__ = 'Production'

__all__ = ['CaseInsensitiveMapping']


class CaseInsensitiveMapping(MutableMapping):
    """
    Implements a case-insensitive mutable mapping / *dict* object.

    Allows values retrieving from keys while ignoring the key case.
    The keys are expected to be unicode or string-like objects supporting the
    :meth:`str.lower` method.

    Parameters
    ----------
    data : dict
        *dict* of data to store into the mapping at initialisation.

    Other Parameters
    ----------------
    \**kwargs : dict, optional
        Key / Value pairs to store into the mapping at initialisation.

    Methods
    -------
    __setitem__
    __getitem__
    __delitem__
    __contains__
    __iter__
    __len__
    __eq__
    __ne__
    __repr__
    copy
    lower_items

    Warning
    -------
    The keys are expected to be unicode or string-like objects.

    References
    ----------
    .. [3]  Reitz, K. (n.d.). CaseInsensitiveDict. Retrieved from
            https://github.com/kennethreitz/requests/\
blob/v1.2.3/requests/structures.py#L37

    Examples
    --------
    >>> methods = CaseInsensitiveMapping({'McCamy': 1, 'Hernandez': 2})
    >>> methods['mccamy']
    1
    """

    def __init__(self, data=None, **kwargs):
        self._data = dict()

        self.update({} if data is None else data, **kwargs)

    @property
    def data(self):
        """
        Property for **self.data** attribute.

        Returns
        -------
        dict
            :class:`ArbitraryPrecisionMapping` data structure.

        Warning
        -------
        :attr:`ArbitraryPrecisionMapping.data` is read only.
        """

        return self._data

    @data.setter
    def data(self, value):
        """
        Setter for **self.data** attribute.

        Parameters
        ----------
        value : object
            Attribute value.
        """

        raise AttributeError('"{0}" attribute is read only!'.format('data'))

    def __setitem__(self, item, value):
        """
        Sets given item with given value.

        The item is stored as lower in the mapping while the original name and
        its value are stored together as the value in a *tuple*:

        {"item.lower()": ("item", value)}

        Parameters
        ----------
        item : object
            Attribute.
        value : object
            Value.

        Notes
        -----
        -   Reimplements the :meth:`MutableMapping.__setitem__` method.
        """

        self._data[item.lower()] = (item, value)

    def __getitem__(self, item):
        """
        Returns the value of given item.

        The item value is retrieved using its lower name in the mapping.

        Parameters
        ----------
        item : unicode
            Item name.

        Returns
        -------
        object
            Item value.

        Notes
        -----
        -   Reimplements the :meth:`MutableMapping.__getitem__` method.
        """

        return self._data[item.lower()][1]

    def __delitem__(self, item):
        """
        Deletes the item with given name.

        The item is deleted from the mapping using its lower name.

        Parameters
        ----------
        item : unicode
            Item name.

        Notes
        -----
        -   Reimplements the :meth:`MutableMapping.__delitem__` method.
        """

        del self._data[item.lower()]

    def __contains__(self, item):
        """
        Returns if the mapping contains given item.

        Parameters
        ----------
        item : unicode
            Item name.

        Returns
        -------
        bool
            Is item in mapping.

        Notes
        -----
        -   Reimplements the :meth:`MutableMapping.__contains__` method.
        """

        return item.lower() in self._data

    def __iter__(self):
        """
        Iterates over the items names in the mapping.

        The item names returned are the original input ones.

        Returns
        -------
        generator
            Item names.

        Notes
        -----
        -   Reimplements the :meth:`MutableMapping.__iter__` method.
        """

        return (item for item, value in self._data.values())

    def __len__(self):
        """
        Returns the items count.

        Returns
        -------
        int
            Items count.

        Notes
        -----
        -   Reimplements the :meth:`MutableMapping.__iter__` method.
        """

        return len(self._data)

    def __eq__(self, item):
        """
        Returns the equality with given object.

        Parameters
        ----------
        item
            Object item.

        Returns
        -------
        bool
            Equality.

        Notes
        -----
        -   Reimplements the :meth:`MutableMapping.__eq__` method.
        """

        if isinstance(item, Mapping):
            item = CaseInsensitiveMapping(item)
        else:
            return NotImplemented

        return dict(self.lower_items()) == dict(item.lower_items())

    def __ne__(self, item):
        """
        Returns the inequality with given object.

        Parameters
        ----------
        item
            Object item.

        Returns
        -------
        bool
            Inequality.

        Notes
        -----
        -   Reimplements the :meth:`MutableMapping.__ne__` method.
        """

        return not (self == item)

    def __repr__(self):
        """
        Returns the mapping representation with the original item names.

        Returns
        -------
        unicode
            Mapping representation.

        Notes
        -----
        -   Reimplements the :meth:`MutableMapping.__repr__` method.
        """

        return '{0}({1})'.format(self.__class__.__name__, dict(self.items()))

    def copy(self):
        """
        Returns a copy of the mapping.

        Returns
        -------
        CaseInsensitiveMapping
            Mapping copy.

        Notes
        -----
        -   The :class:`CaseInsensitiveMapping` class copy returned is a simple
            *copy* not a *deepcopy*.
        """

        return CaseInsensitiveMapping(self._data.values())

    def lower_items(self):
        """
        Iterates over the lower items names.

        Returns
        -------
        generator
            Lower item names.
        """

        return ((item, value[1]) for (item, value) in self._data.items())
