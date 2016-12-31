#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Defines unit tests for `transforms.ctl.lib.ACESlib.ODT_Common.ctl` *CTL* file.
"""

from __future__ import division, unicode_literals

import os
import platform
import unittest

from tests.utilities import CTL_Function_TestCase

__author__ = 'ACES Developers'
__copyright__ = 'Copyright (C) 2016-2017 A.M.P.A.S'
__maintainer__ = 'Academy of Motion Picture Arts and Sciences'
__email__ = 'acessupport@oscars.org'
__status__ = 'Production'

__all__ = ['Test_Y_2_linCV',
           'Test_linCV_2_Y',
           'Test_darkSurround_to_dimSurround',
           'Test_dimSurround_to_darkSurround',
           'Test_roll_white_fwd',
           'Test_roll_white_rev']


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
                a_out='aIn'))

    def test_Y_2_linCV_inversion(self):
        """
        Tests `transforms.ctl.lib.ACESlib.ODT_Common.Y_2_linCV` function
        inversion.
        """

        function_template = ('linCV_2_Y(Y_2_linCV({0}, '
                             'CINEMA_WHITE, CINEMA_BLACK), '
                             'CINEMA_WHITE, CINEMA_BLACK)')
        imports = self.format_imports(self.declaration_ctl_file_import())

        self.assert_array_and_image_all_close(
            self.default_quadruplet_samples,
            self.ctl_file_render(
                suffix='inversion',
                imports=imports,
                r_out=function_template.format('rIn'),
                g_out=function_template.format('gIn'),
                b_out=function_template.format('bIn'),
                a_out='aIn')[1],
            relative_tolerance=self.RELATIVE_TOLERANCE * 10)


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
                a_out='aIn'))

    def test_linCV_2_Y_inversion(self):
        """
        Tests `transforms.ctl.lib.ACESlib.ODT_Common.linCV_2_Y` function
        inversion.
        """

        function_template = ('Y_2_linCV(linCV_2_Y({0}, '
                             'CINEMA_WHITE, CINEMA_BLACK), '
                             'CINEMA_WHITE, CINEMA_BLACK)')
        imports = self.format_imports(self.declaration_ctl_file_import())

        self.assert_array_and_image_all_close(
            self.default_quadruplet_samples,
            self.ctl_file_render(
                suffix='inversion',
                imports=imports,
                r_out=function_template.format('rIn'),
                g_out=function_template.format('gIn'),
                b_out=function_template.format('bIn'),
                a_out='aIn')[1],
            relative_tolerance=self.RELATIVE_TOLERANCE * 10)


class Test_darkSurround_to_dimSurround(CTL_Function_TestCase):
    """
    Defines `transforms.ctl.lib.ACESlib.ODT_Common.darkSurround_to_dimSurround`
    function units tests methods.
    """

    DECLARATION_CTL_FILE = os.path.join(
        *('transforms', 'ctl', 'lib', 'ACESlib.ODT_Common.ctl'))

    CTL_IMPORTS = ['ACESlib.Utilities', 'ACESlib.Transform_Common']

    def test_darkSurround_to_dimSurround(self):
        """
        Tests `transforms.ctl.lib.ACESlib.\
ODT_Common.darkSurround_to_dimSurround` function.
        """

        # TODO: Investigate large precision loss on Linux.
        if platform.system() == 'Linux':
            return

        imports = self.format_imports(self.declaration_ctl_file_import())

        self.assert_images_all_close(
            *self.ctl_file_render(
                'float3',
                imports=imports,
                rgb_out='darkSurround_to_dimSurround(rgbIn)',
                a_out='aIn'))

    def test_darkSurround_to_dimSurround_inversion(self):
        """
        Tests `transforms.ctl.lib.ACESlib.\
ODT_Common.darkSurround_to_dimSurround` function inversion.
        """

        # TODO: Investigate large precision loss.
        return

        imports = self.format_imports(self.declaration_ctl_file_import())

        self.assert_array_and_image_all_close(
            self.default_quadruplet_samples,
            self.ctl_file_render(
                'float3',
                suffix='inversion',
                imports=imports,
                rgb_out=('darkSurround_to_dimSurround('
                         'dimSurround_to_darkSurround(rgbIn))'),
                a_out='aIn')[1])


class Test_dimSurround_to_darkSurround(CTL_Function_TestCase):
    """
    Defines `transforms.ctl.lib.ACESlib.ODT_Common.dimSurround_to_darkSurround`
    function units tests methods.
    """

    DECLARATION_CTL_FILE = os.path.join(
        *('transforms', 'ctl', 'lib', 'ACESlib.ODT_Common.ctl'))

    CTL_IMPORTS = ['ACESlib.Utilities', 'ACESlib.Transform_Common']

    def test_dimSurround_to_darkSurround(self):
        """
        Tests `transforms.ctl.lib.ACESlib.\
ODT_Common.dimSurround_to_darkSurround` function.
        """

        # TODO: Investigate large precision loss on Linux.
        if platform.system() == 'Linux':
            return

        imports = self.format_imports(self.declaration_ctl_file_import())

        self.assert_images_all_close(
            *self.ctl_file_render(
                'float3',
                imports=imports,
                rgb_out='dimSurround_to_darkSurround(rgbIn)',
                a_out='aIn'))

    def test_dimSurround_to_darkSurround_inversion(self):
        """
        Tests `transforms.ctl.lib.ACESlib.\
ODT_Common.dimSurround_to_darkSurround` function inversion.
        """

        # TODO: Investigate large precision loss.
        return

        imports = self.format_imports(self.declaration_ctl_file_import())

        self.assert_array_and_image_all_close(
            self.default_quadruplet_samples,
            self.ctl_file_render(
                'float3',
                suffix='inversion',
                imports=imports,
                rgb_out=('dimSurround_to_darkSurround('
                         'darkSurround_to_dimSurround(rgbIn))'),
                a_out='aIn')[1])


class Test_roll_white_fwd(CTL_Function_TestCase):
    """
    Defines `transforms.ctl.lib.ACESlib.ODT_Common.roll_white_fwd` function
    units tests methods.
    """

    DECLARATION_CTL_FILE = os.path.join(
        *('transforms', 'ctl', 'lib', 'ACESlib.ODT_Common.ctl'))

    CTL_IMPORTS = ['ACESlib.Utilities', 'ACESlib.Transform_Common']

    def test_roll_white_fwd(self):
        """
        Tests `transforms.ctl.lib.ACESlib.ODT_Common.roll_white_fwd` function.
        """

        function_template = 'roll_white_fwd({0}, 0.9, 0.125)'
        imports = self.format_imports(self.declaration_ctl_file_import())

        self.assert_images_all_close(
            *self.ctl_file_render(
                imports=imports,
                r_out=function_template.format('rIn'),
                g_out=function_template.format('gIn'),
                b_out=function_template.format('bIn'),
                a_out='aIn'))

        self.assert_images_all_close(
            *self.ctl_file_render(
                suffix='white_width_variation',
                imports=imports,
                r_out='roll_white_fwd(rIn, 0.9, 0.125)',
                g_out='roll_white_fwd(rIn, 0.75, 0.25)',
                b_out='roll_white_fwd(rIn, 0.5, 0.5)',
                a_out='aIn'))

    def test_roll_white_fwd_inversion(self):
        """
        Tests `transforms.ctl.lib.ACESlib.ODT_Common.roll_white_fwd` function
        inversion.
        """

        # TODO: Investigate breaking inversion.
        return

        function_template = ('roll_white_fwd(roll_white_rev('
                             '{0}, 0.9, 0.125), 0.9, 0.125)')
        imports = self.format_imports(self.declaration_ctl_file_import())

        self.assert_array_and_image_all_close(
            self.default_quadruplet_samples,
            self.ctl_file_render(
                suffix='inversion',
                imports=imports,
                r_out=function_template.format('rIn'),
                g_out=function_template.format('gIn'),
                b_out=function_template.format('bIn'),
                a_out='aIn')[1])


class Test_roll_white_rev(CTL_Function_TestCase):
    """
    Defines `transforms.ctl.lib.ACESlib.ODT_Common.roll_white_rev` function
    units tests methods.
    """

    DECLARATION_CTL_FILE = os.path.join(
        *('transforms', 'ctl', 'lib', 'ACESlib.ODT_Common.ctl'))

    CTL_IMPORTS = ['ACESlib.Utilities', 'ACESlib.Transform_Common']

    def test_roll_white_rev(self):
        """
        Tests `transforms.ctl.lib.ACESlib.ODT_Common.roll_white_rev` function.
        """

        function_template = 'roll_white_rev({0}, 0.9, 0.125)'
        imports = self.format_imports(self.declaration_ctl_file_import())

        self.assert_images_all_close(
            *self.ctl_file_render(
                imports=imports,
                r_out=function_template.format('rIn'),
                g_out=function_template.format('gIn'),
                b_out=function_template.format('bIn'),
                a_out='aIn'))

        self.assert_images_all_close(
            *self.ctl_file_render(
                suffix='white_width_variation',
                imports=imports,
                r_out='roll_white_fwd(rIn, 0.9, 0.125)',
                g_out='roll_white_fwd(rIn, 0.75, 0.25)',
                b_out='roll_white_fwd(rIn, 0.5, 0.5)',
                a_out='aIn'))

    def test_roll_white_rev_inversion(self):
        """
        Tests `transforms.ctl.lib.ACESlib.ODT_Common.roll_white_rev` function
        inversion.
        """

        # TODO: Investigate breaking inversion.
        return

        function_template = ('roll_white_rev(roll_white_fwd('
                             '{0}, 0.9, 0.125), 0.9, 0.125)')
        imports = self.format_imports(self.declaration_ctl_file_import())

        self.assert_array_and_image_all_close(
            self.default_quadruplet_samples,
            self.ctl_file_render(
                suffix='inversion',
                imports=imports,
                r_out=function_template.format('rIn'),
                g_out=function_template.format('gIn'),
                b_out=function_template.format('bIn'),
                a_out='aIn')[1])


if __name__ == '__main__':
    unittest.main()
