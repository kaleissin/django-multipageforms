===================================
django-multipageforms Documentation
===================================

Installation
============

Install the library, for instance with pip::

    pip install django-multipageforms


Demo
====

Copy the entire django-multipageforms directory somewhere, set up and
enter a virtualenv, then provided you are on some Un*x::

    make demo

This'll automatically make a user "admin" with the password "demo".

The demo should now be running on http://127.0.0.1/

Running `make demo` again will erase the database from the previous
run.

Tests
=====

To run the tests, first install the testing-requirements::

    pip install -r requirements/test.txt

Provided you have a python on your path you can then run the tests with::

    python runtests.py

You can also test with tox::

    tox


:Version: 0.6.0
