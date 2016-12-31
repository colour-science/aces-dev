#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Defines unit tests for `transforms.ctl.rrt.RRT.ctl` *CTL* file.
"""

from __future__ import division, unicode_literals

import os
import unittest

from tests.utilities import CTL_File_TestCase

__author__ = 'ACES Developers'
__copyright__ = 'Copyright (C) 2016-2017 A.M.P.A.S'
__maintainer__ = 'Academy of Motion Picture Arts and Sciences'
__email__ = 'acessupport@oscars.org'
__status__ = 'Production'

__all__ = ['Test_RRT']


class Test_RRT(CTL_File_TestCase):
    """
    Defines `transforms.ctl.rrt.RRT.ctl` file units tests methods.
    """

    CTL_FILE = os.path.join(
        *('transforms', 'ctl', 'rrt', 'RRT.ctl'))

    GENERATE_REFERENCE_IMAGE_DATA = True

    def test_RRT(self):
        """
        Tests `transforms.ctl.rrt.RRT.ctl` file.
        """

        self.assert_images_all_close(
            *self.ctl_file_render(
                space='log10',
                start=(2 ** -14, 2 ** -14, 2 ** -14),
                end=(65504, 65504, 65504)))


if __name__ == '__main__':
    unittest.main()
