# -*- coding: utf-8 -*-

import os
import sys

from codecs import open

__version__ = "0.0.1"
__author__ = "SkyLothar"
__email__ = "allothar@gmail.com"
__url__ = "https://github.com/skylothar/super-gauge"


try:
    import setuptools
except ImportError:
    from distutils.core import setuptools


if sys.argv[-1] == "publish":
    os.system("python setup.py sdist upload")
    sys.exit()


with open("requirements.txt", "r", "utf-8") as f:
    requires = f.read()


packages = ["supergauge", "supergauge.plugins"]


with open("README.rst", "r", "utf-8") as f:
    readme = f.read()


setuptools.setup(
    name="supergauge",
    version=__version__,
    description="supervisor process gauge eventlistener",
    long_description=readme,
    author=__author__,
    author_email=__email__,
    install_requires=requires,
    dependency_links=[
        "https://github.com/Supervisor/supervisor/archive/master.tar.gz#egg=supervisor-4.0.0dev"
    ],
    url=__url__,
    entry_points={
        "console_scripts": [
            "supergauge = supergauge.eventlistener:runforever"
        ],
    },
    packages=packages,
    package_dir={
        "supergauge": "supergauge"
    },
    include_package_data=True,
    zip_safe=False
)
