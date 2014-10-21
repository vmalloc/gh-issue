import os
import sys
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), "gh_issue", "__version__.py")) as version_file:
    exec(version_file.read()) # pylint: disable=W0122

_INSTALL_REQUIRES = [
    'click',
    'github3.py',
    'Logbook',
]

setup(name="gh-issue",
      classifiers = [
          "Programming Language :: Python :: 2.6",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3.3",
          "Programming Language :: Python :: 3.4",
          "Programming Language :: Python :: py",
          ],
      description="CLI Wrapper for Github issue workflows",
      license="BSD3",
      author="Rotem Yaari",
      author_email="vmalloc@gmail.com",
      version=__version__, # pylint: disable=E0602
      packages=find_packages(exclude=["tests"]),

      url="https://github.com/vmalloc/gh-issue",

      install_requires=_INSTALL_REQUIRES,
      entry_points=dict(
          console_scripts=[
              "gh-issue  = gh_issue.main:main",
          ]
      ),

      namespace_packages=[]
      )
