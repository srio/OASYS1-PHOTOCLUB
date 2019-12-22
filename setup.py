#! /usr/bin/env python3

import imp
import os
import sys
import subprocess

NAME = 'OASYS1-PHOTOCLUB'

VERSION = '0.0.1'
ISRELEASED = False

DESCRIPTION = 'WIDGETS DEVELOPED BY M. SANCHEZ DEL RIO FOR PROCESSING PHOTOGRAPHIES'
README_FILE = os.path.join(os.path.dirname(__file__), 'README.md')
LONG_DESCRIPTION = open(README_FILE).read()
AUTHOR = 'Manuel Sanchez del Rio'
AUTHOR_EMAIL = 'msanchezdelrio@gmail.com'
URL = 'https://github.com/srio/OASYS1-PHOTOCLUB'
DOWNLOAD_URL = 'https://github.com/srio/OASYS1-PHOTOCLUB'
LICENSE = 'MIT'

KEYWORDS = (
    'photography',
    'pillow',
    'oasys1',
)

CLASSIFIERS = (
    'Development Status :: 4 - Beta',
    'Environment :: X11 Applications :: Qt',
    'Environment :: Console',
    'Environment :: Plugins',
    'Programming Language :: Cython',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Intended Audience :: Science/Research',
)


SETUP_REQUIRES = (
                  'setuptools',
                  )

INSTALL_REQUIRES = (
                    'setuptools',
                   )

if len({'develop', 'release', 'bdist_egg', 'bdist_rpm', 'bdist_wininst',
        'install_egg_info', 'build_sphinx', 'egg_info', 'easy_install',
        'upload', 'test'}.intersection(sys.argv)) > 0:
    import setuptools
    extra_setuptools_args = dict(
        zip_safe=False,  # the package can run out of an .egg file
        include_package_data=True,
        install_requires=INSTALL_REQUIRES
    )
else:
    extra_setuptools_args = dict()

from setuptools import find_packages, setup

PACKAGES = find_packages(exclude = ('*.tests', '*.tests.*', 'tests.*', 'tests'), )

PACKAGE_DATA = {
    "orangecontrib.photoclub.widgets.tools":["icons/*.png", "icons/*.jpg"],
}

NAMESPACE_PACAKGES = ["orangecontrib","orangecontrib.photoclub", "orangecontrib.photoclub.widgets"]

ENTRY_POINTS = {
    'oasys.addons' : ("PHOTO CLUB = orangecontrib.photoclub", ),
    'oasys.widgets' : (
        "Photo Club Tools = orangecontrib.photoclub.widgets.tools",
    ),
    'oasys.menus' : ("photoclubmenu = orangecontrib.photoclub.menu",)
}

if __name__ == '__main__':
    is_beta = False

    try:
        import PyMca5, PyQt4

        is_beta = True
    except:
        setup(
              name = NAME,
              version = VERSION,
              description = DESCRIPTION,
              long_description = LONG_DESCRIPTION,
              author = AUTHOR,
              author_email = AUTHOR_EMAIL,
              url = URL,
              download_url = DOWNLOAD_URL,
              license = LICENSE,
              keywords = KEYWORDS,
              classifiers = CLASSIFIERS,
              packages = PACKAGES,
              package_data = PACKAGE_DATA,
              setup_requires = SETUP_REQUIRES,
              install_requires = INSTALL_REQUIRES,
              entry_points = ENTRY_POINTS,
              namespace_packages=NAMESPACE_PACAKGES,
              include_package_data = True,
              zip_safe = False,
              )

    if is_beta: raise NotImplementedError("This version of Photo CLub doesn't work with Oasys1 beta.\nPlease install OASYS1 final release")
