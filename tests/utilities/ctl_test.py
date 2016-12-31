#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
CTL Test
========

Defines the classes performing *CTL* unit tests:

-   :class:`CTL_File_TestCase`
-   :class:`CTL_Function_TestCase`
"""

from __future__ import division, unicode_literals

import inspect
import numpy as np
import os
import shutil
import tempfile
import textwrap
import unittest

from tests.utilities import (
    ctl_render,
    filter_kwargs,
    read_image,
    tstack,
    write_image)

__author__ = 'ACES Developers'
__copyright__ = 'Copyright (C) 2016-2017 A.M.P.A.S'
__maintainer__ = 'Academy of Motion Picture Arts and Sciences'
__email__ = 'acessupport@oscars.org'
__status__ = 'Production'

__all__ = ['AbstractCTL_TestCase',
           'CTL_File_TestCase',
           'CTL_Function_TestCase']


class AbstractCTL_TestCase(unittest.TestCase):
    """
    Defines the abstract base class for *CTL* unit tests.

    Attributes
    ----------
    ABSOLUTE_TOLERANCE
    CTL_ROOT_DIRECTORY
    GENERATE_REFERENCE_IMAGE_DATA
    RELATIVE_TOLERANCE
    temporary_directory

    Methods
    -------
    setUp
    tearDown
    write_ramp_image
    ramp_image_path
    reference_ramp_image_path
    assessment_ramp_image_path
    assert_images_all_close
    """

    CTL_ROOT_DIRECTORY = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', '..'))
    """
    *CTL* root directory (i.e. the directory containing the *ACES* code base
    *transforms* directory).
    """

    GENERATE_REFERENCE_IMAGE_DATA = False
    """
    By default unit tests will be performed in a temporary directory: generated
    test image will be written in the temporary directory. If set to `True`,
    the test image will be written as a reference image in the resources
    directory next to the current unit tests module.
    """

    RELATIVE_TOLERANCE = 0.0000001
    """
    Relative tolerance for image comparison.
    """

    ABSOLUTE_TOLERANCE = 0.0000001
    """
    Absolute tolerance for image comparison.
    """

    def setUp(self):
        """
        Initialises common tests attributes.
        """

        if os.environ.get('CTL_MODULE_PATH') is None:
            os.environ['CTL_MODULE_PATH'] = os.path.join(
                os.path.dirname(__file__),
                '..', '..', 'transforms', 'ctl', 'lib')

        self.temporary_directory = tempfile.mkdtemp()

    def tearDown(self):
        """
        After tests actions.
        """

        shutil.rmtree(self.temporary_directory)

    @staticmethod
    def write_ramp_image(
            path,
            space='Linear',
            start=(0, 0, 0),
            end=(1, 1, 1),
            samples=1024):
        """
        Generates a *linear*, *log2* or *log10* ramp image using given range
        and samples count.

        Parameters
        ----------
        path : unicode
            Path of the ramp image to write.
        space : unicode, optional
            **{'Linear', 'Log2', 'Log10'}**,
            Ramp space.
        start : array_like, optional
            *RGB* channels start value.
        end : array_like, optional
            *RGB* channels end value.
        samples : int, optional
            Ramp samples count.

        Returns
        -------
        bool
            Method success.
        """

        space = space.lower()

        if space == 'log2':
            a = tstack(
                [np.logspace(np.log2(start[i]),
                             np.log2(end[i]),
                             samples,
                             base=2)[np.newaxis, ...]
                 for i in range(3)])
        elif space == 'log10':
            a = tstack(
                [np.logspace(np.log10(start[i]),
                             np.log10(end[i]),
                             samples)[np.newaxis, ...]
                 for i in range(3)])
        else:
            a = tstack(
                [np.linspace(
                    start[i],
                    end[i],
                    samples)[np.newaxis, ...]
                 for i in range(3)])

        write_image(a, path)

        return True

    def ramp_image_path(
            self,
            space='linear',
            start=(0, 0, 0),
            end=(1, 1, 1),
            samples=1024,
            suffix=None):
        """
        Returns the path of the current unit tests generated ramp image.

        Parameters
        ----------
        space : unicode, optional
            **{'Linear', 'Log2', 'Log10'}**,
            Ramp space.
        start : array_like, optional
            *RGB* channels start value.
        end : array_like, optional
            *RGB* channels end value.
        samples : int, optional
            Ramp samples count.
        suffix : unicode, optional
            Path suffix.

        Returns
        -------
        unicode
            Path of the current unit tests generated ramp image.
        """

        space = space.lower()
        path = str(os.path.join(
            self.temporary_directory,
            '{0}_{1}_ramp{2}.exr'.format(
                self.__class__.__name__,
                space,
                '_{0}'.format(suffix) if suffix is not None else '')))

        self.write_ramp_image(path, space, start, end, samples)

        return path

    def reference_ramp_image_path(self, space='linear', suffix=None):
        """
        Returns the path of the reference ramp image.

        This is the image the test ramp image will be compared against.

        Parameters
        ----------
        space : unicode, optional
            **{'Linear', 'Log2', 'Log10'}**,
            Ramp space.
        suffix : unicode, optional
            Path suffix.

        Returns
        -------
        unicode
            Path of the reference ramp image.
        """

        space = space.lower()
        path = str(os.path.join(
            os.path.dirname(inspect.getfile(self.__class__)),
            'resources',
            '{0}_reference_{1}_ramp{2}.exr'.format(
                self.__class__.__name__,
                space,
                '_{0}'.format(suffix) if suffix is not None else '')))

        return path

    def assessment_ramp_image_path(self, space='linear', suffix=None):
        """
        Returns the path of the generated assessment / test ramp image.

        This is the image that will be compared to the reference ramp image.

        Parameters
        ----------
        space : unicode, optional
            **{'Linear', 'Log2', 'Log10'}**,
            Ramp space.
        suffix : unicode, optional
            Path suffix.

        Returns
        -------
        unicode
            Path of generated assessment / test ramp image.
        """

        space = space.lower()
        path = str(os.path.join(
            self.temporary_directory,
            '{0}_test_{1}_ramp{2}.exr'.format(
                self.__class__.__name__,
                space,
                '_{0}'.format(suffix) if suffix is not None else '')))

        return path

    def assert_images_all_close(self, image_path_1, image_path_2):
        """
        Asserts that both given image are close in given tolerances.

        Parameters
        ----------
        image_path_1 : unicode
            Path to first image.
        image_path_2
            Path to second image.
        """

        assert os.path.exists(image_path_1), (
            '"{0}" image file doesn\'t exists!'.format(image_path_1))

        assert os.path.exists(image_path_2), (
            '"{0}" image file doesn\'t exists!'.format(image_path_2))

        np.testing.assert_allclose(
            read_image(image_path_1),
            read_image(image_path_2),
            rtol=self.RELATIVE_TOLERANCE,
            atol=self.ABSOLUTE_TOLERANCE)


class CTL_File_TestCase(AbstractCTL_TestCase):
    """
    Defines the base class for *CTL* file unit tests.

    Attributes
    ----------
    CTL_FILE

    Methods
    -------
    ctl_file_path
    ctl_file_render
    """

    CTL_FILE = None
    """
    Relative path to :attr:`CTLTestCase.CTL_ROOT_DIRECTORY` class attribute of
    the *CTL* file being tested, must be reimplemented by each test sub-class.
    """

    def ctl_file_path(self):
        """
        Returns the absolute path of the *CTL* file being tested.

        Returns
        -------
        unicode
            Absolute path of the *CTL* file being tested.
        """

        path = os.path.join(self.CTL_ROOT_DIRECTORY, self.CTL_FILE)

        assert os.path.exists(path), (
            '"{0}" CTL file doesn\'t exists!'.format(path))

        return path

    def ctl_file_render(self, **kwargs):
        """
        Calls *ctlrender* for the *CTL* file being tested.

        Other Parameters
        ----------------
        space : unicode, optional
            **{'Linear', 'Log2', 'Log10'}**,
            Ramp image space.
        start : array_like, optional
            Ramp image *RGB* channels start value.
        end : array_like, optional
            Ramp image *RGB* channels end value.
        samples : int, optional
            Ramp image samples count.

        Returns
        -------
        tuple
            Reference and test image paths.
        """

        input_image_path = self.ramp_image_path(
            **filter_kwargs(
                self.ramp_image_path, **kwargs))
        reference_image_path = self.reference_ramp_image_path(
            space=kwargs.get('space', 'Linear'),
            suffix=kwargs.get('suffix'))
        test_image_path = (
            reference_image_path
            if self.GENERATE_REFERENCE_IMAGE_DATA else
            self.assessment_ramp_image_path(
                space=kwargs.get('space', 'Linear'),
                suffix=kwargs.get('suffix')))

        ctl_render(
            input_image_path,
            test_image_path,
            (self.ctl_file_path(),))

        return reference_image_path, test_image_path


class CTL_Function_TestCase(AbstractCTL_TestCase):
    """
    Defines the base class for *CTL* functions unit tests.

    Attributes
    ----------
    CTL_IMPORTS
    DECLARATION_CTL_FILE

    Methods
    -------
    declaration_ctl_file_path
    declaration_ctl_file_import
    assessment_ctl_file_path
    format_imports
    float_input_ctl_file_content
    float3_input_ctl_file_content
    ctl_file_render
    """

    DECLARATION_CTL_FILE = None
    """
    Relative path to :attr:`CTLTestCase.CTL_ROOT_DIRECTORY` class attribute of
    the *CTL* file declaring the function being tested, must be reimplemented
    by each test sub-class.
    """

    CTL_IMPORTS = []
    """
    Imports the *CTL* test file will need to invoke the tested *CTL* function
    successfully, must be reimplemented by each test sub-class.
    """

    def declaration_ctl_file_path(self):
        """
        Returns the absolute path of the *CTL* file containing the *CTL*
        function being tested.

        Returns
        -------
        unicode
            Absolute path of the *CTL* file containing the *CTL* function
            being tested.
        """

        path = os.path.join(self.CTL_ROOT_DIRECTORY, self.DECLARATION_CTL_FILE)

        assert os.path.exists(path), (
            '"{0}" CTL file doesn\'t exists!'.format(path))

        return path

    def declaration_ctl_file_import(self):
        """
        Returns the import name of the *CTL* file containing the *CTL*
        function being tested.

        Returns
        -------
        unicode
            Import name of the *CTL* file containing the *CTL* function
            being tested.
        """

        return os.path.splitext(
            os.path.basename(self.declaration_ctl_file_path()))[0]

    def assessment_ctl_file_path(self):
        """
        Returns the path of the generated assessment / test *CTL* file.

        Returns
        -------
        unicode
            Path of the generated assessment / test *CTL* file.
        """

        path = os.path.join(
            self.temporary_directory,
            '{0}.ctl'.format(self.__class__.__name__))

        return path

    def format_imports(self, *imports):
        """
        Formats instantiation time imports and given ones to *CTL* compliant
        representation.

        Parameters
        ----------
        imports : array_like, optional
            Imports to add to the instantiation time ones.

        Returns
        -------
        unicode
            *CTL* compliant representation imports.
        """

        return '\n'.join(
            ['import "{0}";'.format(import_)
             for import_ in self.CTL_IMPORTS + list(imports)])

    def float_input_ctl_file_content(
            self,
            imports,
            r_out,
            g_out,
            b_out,
            a_out):
        """
        Returns the *CTL* file content for an *RGBA* output image with *float*
        output function.

        Parameters
        ----------
        imports : unicode
            *CTL* compliant representation imports.
        r_out : unicode
            *CTL* compliant representation for red channel output.
        g_out : unicode
            *CTL* compliant representation for green channel output.
        b_out : unicode
            *CTL* compliant representation for blue channel output.
        a_out : unicode
            *CTL* compliant representation for alpha channel output.

        Returns
        -------
        unicode
            *CTL* file content for an *RGBA* output image with *float* output
            function.
        """

        ctl_file_content = """
        // {0} - "float" Output Function

        {1}

        void main
        (
            input varying float rIn,
            input varying float gIn,
            input varying float bIn,
            input varying float aIn,
            output varying float rOut,
            output varying float gOut,
            output varying float bOut,
            output varying float aOut
        )
        {{
            rOut = {2};
            gOut = {3};
            bOut = {4};
            aOut = {5};
        }}
        """[1:]

        ctl_file_content = textwrap.dedent(ctl_file_content).format(
            self.__class__.__name__, imports, r_out, g_out, b_out, a_out)

        return ctl_file_content

    def float3_input_ctl_file_content(
            self,
            imports,
            rgb_out,
            a_out):
        """
        Returns the *CTL* file content for an *RGBA* output image with *float3*
        output function.

        Parameters
        ----------
        imports : unicode
            *CTL* compliant representation imports.
        rgb_out : unicode
            *CTL* compliant representation for *RGB* channels output.
        a_out : unicode
            *CTL* compliant representation for alpha channel output.

        Returns
        -------
        unicode
            *CTL* file content for an *RGBA* output image with *float3*
            output function.
        """

        ctl_file_content = """
        // {0} - "float3" Output Function

        {1}

        void main
        (
            input varying float rIn,
            input varying float gIn,
            input varying float bIn,
            input varying float aIn,
            output varying float rOut,
            output varying float gOut,
            output varying float bOut,
            output varying float aOut
        )
        {{
            float rgbIn[3] = {{rIn, gIn, bIn}};

            float rgb[3];
            rgb = {2};

            rOut = rgb[0];
            gOut = rgb[1];
            bOut = rgb[2];
            aOut = {3};
        }}
        """[1:]

        ctl_file_content = textwrap.dedent(ctl_file_content).format(
            self.__class__.__name__, imports, rgb_out, a_out)

        return ctl_file_content

    def ctl_file_render(self, output_function_type='float', **kwargs):
        """
        Calls *ctlrender* for an *RGBA* output image with *float* or *float3*
        output function.

        Parameters
        ----------
        output_function_type : unicode, optional
            **{'float', 'float3'}***,
            Tested function output type.

        Other Parameters
        ----------------
        imports : unicode
            *CTL* compliant representation imports.
        r_out : unicode
            *CTL* compliant representation for red channel output.
        g_out : unicode
            *CTL* compliant representation for green channel output.
        b_out : unicode
            *CTL* compliant representation for blue channel output.
        rgb_out : unicode
            *CTL* compliant representation for *RGB* channels output.
        a_out : unicode
            *CTL* compliant representation for alpha channel output.
        space : unicode, optional
            **{'Linear', 'Log2', 'Log10'}**,
            Ramp image space.
        start : array_like, optional
            Ramp image *RGB* channels start value.
        end : array_like, optional
            Ramp image *RGB* channels end value.
        samples : int, optional
            Ramp image samples count.

        Returns
        -------
        tuple
            Reference and test image paths.
        """

        float_method = (
            self.float_input_ctl_file_content
            if output_function_type.lower() == 'float' else
            self.float3_input_ctl_file_content)
        temporary_ctl_file_content = float_method(
            **filter_kwargs(float_method, **kwargs))

        test_ctl_file_path = self.assessment_ctl_file_path()
        with open(test_ctl_file_path, 'w') as file_:
            file_.write(temporary_ctl_file_content)

        input_image_path = self.ramp_image_path(
            **filter_kwargs(
                self.ramp_image_path, **kwargs))
        reference_image_path = self.reference_ramp_image_path(
            space=kwargs.get('space', 'Linear'),
            suffix=kwargs.get('suffix'))
        test_image_path = (
            reference_image_path
            if self.GENERATE_REFERENCE_IMAGE_DATA else
            self.assessment_ramp_image_path(
                space=kwargs.get('space', 'Linear'),
                suffix=kwargs.get('suffix')))

        ctl_render(
            input_image_path,
            test_image_path,
            (test_ctl_file_path,))

        return reference_image_path, test_image_path
