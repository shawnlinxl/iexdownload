from setuptools import setup

import versioneer

DISTNAME = "iexdownload"
DESCRIPTION = "iexdownload retrieves and archives iexcloud data in databases"
MAINTAINER = "Shawn Lin"
MAINTAINER_EMAIL = "shawnlin.xl@gmail.com"
AUTHOR = "Shawn Lin"
AUTHOR_EMAIL = "shawnlin.xl@gmail.com"
URL = "https://github.com/shawnlinxl/iexdownload"
LICENSE = "MIT"

classifiers = [
    "Development Status :: 1 - Planning",
    "Programming Language :: Python :: 3.7",
    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    "Intended Audience :: Science/Research",
    "Topic :: Office/Business :: Financial",
    "Topic :: Scientific/Engineering",
    "Operating System :: OS Independent",
]

install_reqs = ["iexcloud>=0.0.1", "pandas>=1.0.0"]

if __name__ == "__main__":
    setup(
        name=DISTNAME,
        description=DESCRIPTION,
        maintainer=MAINTAINER,
        maintainer_email=MAINTAINER_EMAIL,
        license=LICENSE,
        classifiers=classifiers,
        install_requires=install_reqs,
        url=URL,
        packages=["iexdownload"],
        version=versioneer.get_version(),
        cmdclass=versioneer.get_cmdclass(),
    )
