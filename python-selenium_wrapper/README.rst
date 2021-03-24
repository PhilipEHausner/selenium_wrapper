========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |appveyor| |requires|
        | |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/python-selenium_wrapper/badge/?style=flat
    :target: https://readthedocs.org/projects/python-selenium_wrapper
    :alt: Documentation Status

.. |travis| image:: https://api.travis-ci.com/PhilipEHausner/python-selenium_wrapper.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.com/github/PhilipEHausner/python-selenium_wrapper

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/PhilipEHausner/python-selenium_wrapper?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/PhilipEHausner/python-selenium_wrapper

.. |requires| image:: https://requires.io/github/PhilipEHausner/python-selenium_wrapper/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/PhilipEHausner/python-selenium_wrapper/requirements/?branch=master

.. |codecov| image:: https://codecov.io/gh/PhilipEHausner/python-selenium_wrapper/branch/master/graphs/badge.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/PhilipEHausner/python-selenium_wrapper

.. |version| image:: https://img.shields.io/pypi/v/selenium-wrapper.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/selenium-wrapper

.. |wheel| image:: https://img.shields.io/pypi/wheel/selenium-wrapper.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/selenium-wrapper

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/selenium-wrapper.svg
    :alt: Supported versions
    :target: https://pypi.org/project/selenium-wrapper

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/selenium-wrapper.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/selenium-wrapper

.. |commits-since| image:: https://img.shields.io/github/commits-since/PhilipEHausner/python-selenium_wrapper/v0.0.0.svg
    :alt: Commits since latest release
    :target: https://github.com/PhilipEHausner/python-selenium_wrapper/compare/v0.0.0...master



.. end-badges

A wrapper for Python's Selenium version"

* Free software: GNU Lesser General Public License v3 or later (LGPLv3+)

Installation
============

::

    pip install selenium-wrapper

You can also install the in-development version with::

    pip install https://github.com/PhilipEHausner/python-selenium_wrapper/archive/master.zip


Documentation
=============


https://python-selenium_wrapper.readthedocs.io/


Development
===========

To run all the tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
