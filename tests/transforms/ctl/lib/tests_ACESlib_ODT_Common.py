#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Defines unit tests for `transforms.ctl.lib.ACESlib.ODT_Common.ctl` *CTL* file.
"""

from __future__ import division, unicode_literals

import os
import unittest

from tests.utilities import CTL_Function_TestCase

__author__ = 'ACES Developers'
__copyright__ = 'Copyright (C) 2016-2017 A.M.P.A.S'
__maintainer__ = 'Academy of Motion Picture Arts and Sciences'
__email__ = 'acessupport@oscars.org'
__status__ = 'Production'

__all__ = ['Test_Y_2_linCV',
           'Test_linCV_2_Y',
           'Test_darkSurround_to_dimSurround']


class Test_Y_2_linCV(CTL_Function_TestCase):
    """
    Defines `transforms.ctl.lib.ACESlib.ODT_Common.Y_2_linCV` function units
    tests methods.
    """

    DECLARATION_CTL_FILE = os.path.join(
        *('transforms', 'ctl', 'lib', 'ACESlib.ODT_Common.ctl'))

    CTL_IMPORTS = ['ACESlib.Utilities', 'ACESlib.Transform_Common']

    def test_Y_2_linCV(self):
        """
        Tests `transforms.ctl.lib.ACESlib.ODT_Common.Y_2_linCV` function.
        """

        function_template = 'Y_2_linCV({0}, CINEMA_WHITE, CINEMA_BLACK)'
        imports = self.format_imports(self.declaration_ctl_file_import())

        self.assert_images_all_close(
            *self.ctl_file_render(
                imports=imports,
                r_out=function_template.format('rIn'),
                g_out=function_template.format('gIn'),
                b_out=function_template.format('bIn'),
                a_out='aIn',
                start=(0, -1, 2 ** -14),
                end=(1, 1, 65504)))


class Test_linCV_2_Y(CTL_Function_TestCase):
    """
    Defines `transforms.ctl.lib.ACESlib.ODT_Common.linCV_2_Y` function units
    tests methods.
    """

    DECLARATION_CTL_FILE = os.path.join(
        *('transforms', 'ctl', 'lib', 'ACESlib.ODT_Common.ctl'))

    CTL_IMPORTS = ['ACESlib.Utilities', 'ACESlib.Transform_Common']

    def test_linCV_2_Y(self):
        """
        Tests `transforms.ctl.lib.ACESlib.ODT_Common.linCV_2_Y` function.
        """

        function_template = 'linCV_2_Y({0}, CINEMA_WHITE, CINEMA_BLACK)'
        imports = self.format_imports(self.declaration_ctl_file_import())

        self.assert_images_all_close(
            *self.ctl_file_render(
                imports=imports,
                r_out=function_template.format('rIn'),
                g_out=function_template.format('gIn'),
                b_out=function_template.format('bIn'),
                a_out='aIn',
                start=(0, -1, 2 ** -14),
                end=(1, 1, 65504)))


class Test_darkSurround_to_dimSurround(CTL_Function_TestCase):
    """
    Defines `transforms.ctl.lib.ACESlib.ODT_Common.darkSurround_to_dimSurround`
    function units tests methods.
    """

    DECLARATION_CTL_FILE = os.path.join(
        *('transforms', 'ctl', 'lib', 'ACESlib.ODT_Common.ctl'))

    CTL_IMPORTS = ['ACESlib.Utilities', 'ACESlib.Transform_Common']

    GENERATE_REFERENCE_IMAGE_DATA = True

    def test_darkSurround_to_dimSurround(self):
        """
        Tests `transforms.ctl.lib.ACESlib.\
ODT_Common.darkSurround_to_dimSurround` function.
        """

        imports = self.format_imports(self.declaration_ctl_file_import())

        self.assert_images_all_close(
            *self.ctl_file_render(
                'float3',
                imports=imports,
                rgb_out='darkSurround_to_dimSurround(rgbIn)',
                a_out='aIn',
                start=(0, -1, 2 ** -14),
                end=(1, 1, 65504)))


if __name__ == '__main__':
    unittest.main()
