========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |requires|
        | |codecov|
        | |codacy|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|

.. |docs| image:: https://readthedocs.org/projects/auto-tune/badge/?style=flat
    :target: https://readthedocs.org/projects/auto-tune
    :alt: Documentation Status

.. |travis| image:: https://travis-ci.org/whitesmith/auto-tune.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/whitesmith/auto-tune

.. |requires| image:: https://requires.io/github/whitesmith/auto-tune/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/whitesmith/auto-tune/requirements/?branch=master

.. |codecov| image:: https://codecov.io/github/whitesmith/auto-tune/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/whitesmith/auto-tune

.. |codacy| image:: https://img.shields.io/codacy/REPLACE_WITH_PROJECT_ID.svg
    :target: https://www.codacy.com/app/whitesmith/auto-tune
    :alt: Codacy Code Quality Status

.. |version| image:: https://img.shields.io/pypi/v/auto-tune.svg
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/auto-tune

.. |commits-since| image:: https://img.shields.io/github/commits-since/whitesmith/auto-tune/v0.0.1.svg
    :alt: Commits since latest release
    :target: https://github.com/whitesmith/auto-tune/compare/v0.0.1...master

.. |wheel| image:: https://img.shields.io/pypi/wheel/auto-tune.svg
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/auto-tune

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/auto-tune.svg
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/auto-tune

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/auto-tune.svg
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/auto-tune


.. end-badges

Estimate hyper-parameter search using evolutionary algorithms

* Free software: MIT license

Installation
============

::

    pip install auto-tune

Documentation
=============

https://auto-tune.readthedocs.io/

Development
===========

To run the all tests run::

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
