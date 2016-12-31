#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
CTL Render
==========

Defines *ctlrender* related objects:

-   :func:`clr_render`
"""

from __future__ import division, unicode_literals

import subprocess

__author__ = 'ACES Developers'
__copyright__ = 'Copyright (C) 2016-2017 A.M.P.A.S'
__maintainer__ = 'Academy of Motion Picture Arts and Sciences'
__email__ = 'acessupport@oscars.org'
__status__ = 'Production'

__all__ = ['CTL_RENDER',
           'CTL_DEFAULT_ARGUMENTS',
           'ctl_render']

CTL_RENDER = 'ctlrender'
"""
*ctlrender* executable name.

CTL_RENDER : unicode
"""

CTL_DEFAULT_ARGUMENTS = ['-verbose', '-force']
"""
*ctlrender* invocation default arguments.

CTL_DEFAULT_ARGUMENTS : list
"""


def ctl_render(image_i, image_o, ctls, ctl_args=CTL_DEFAULT_ARGUMENTS):
    """
    Calls *ctlrender* with given input and output image paths and arguments.

    Parameters
    ----------
    image_i : unicode
        Input image for *ctlrender*.
    image_o : unicode
        Output image for *ctlrender*.
    ctls : array_like
        *CTL* files to include.
    ctl_args : array_like
        Arguments to pass to *ctlrender*.

    Returns
    -------
    unicode :
        *stdout* output.

    Raises
    ------
    CalledProcessError
        If the exit code was non-zero.

    Examples
    --------
    >>> ctl_render(  # doctest: +SKIP
    ...     'path/to/input/image.exr',
    ...     'path/to/output/image.exr',
    ...     ['path/to/first/ctl/file.ctl',
    ...      'path/to/second/ctl/file.ctl'])
    global ctl parameters:

    destination format: exr
           input scale: default
          output scale: default

       ctl script file: ...
         function name: main
       input arguments:
                   rIn: float (varying)
                   gIn: float (varying)
                   bIn: float (varying)
                   aIn: float (varying)
      output arguments:
                  rOut: float (varying)
                  gOut: float (varying)
                  bOut: float (varying)
                  aOut: float (varying)
    """

    ctls_arguments = []
    for ctl in ctls:
        ctls_arguments.append('-ctl')
        ctls_arguments.append(ctl)

    output = subprocess.check_output(
        [CTL_RENDER] + ctl_args + [image_i, image_o] + ctls_arguments)

    return output
