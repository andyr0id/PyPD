#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-


__author__ = 'Andrew J. Elmsley, andy@andyroid.co.uk'


from setuptools import setup, find_packages


setup(
    name="PyPD",
    version="0.0.1",
    description="PyPD is a python library for libpd.",
    license="BSD",
    keywords="Pure Data, libpd",
    url="http://andyroid.co.uk",
    packages=find_packages(exclude=['examples', 'docs']),
    include_package_data=True,
    test_suite='pypd.tests.runtests.make_test_suite',
    package_data={'pypd': ['rl/environments/ode/models/*.xode']},
    # install_requires = ["pylibpd"],
)