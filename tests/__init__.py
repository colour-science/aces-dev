#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
ACES - CTL - Unit Tests
=======================

*ACES - CTL - Unit Tests* is a *Python* package implementing unit tests support
for the *ACES* *CTL* codebase.

Subpackages
-----------
-   transforms: Unit tests for the *CTL* codebase.
-   utilities: Objects implementing support for the unit tests.
"""

from __future__ import absolute_import

from .utilities import *  # noqa
from . import utilities  # noqa

__author__ = 'ACES Developers'
__copyright__ = 'Copyright (C) 2016-2017 A.M.P.A.S'
__maintainer__ = 'Academy of Motion Picture Arts and Sciences'
__email__ = 'acessupport@oscars.org'
__status__ = 'Production'

__all__ = []
__all__ += utilities.__all__
