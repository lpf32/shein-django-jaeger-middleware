#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages

MIDDLEWARE_BASE_DIR = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(MIDDLEWARE_BASE_DIR, 'README.md')) as f:
    long_description = f.read()

setup(
    name='shein-django-jaeger-middleware',
    license='MIT',
    version='0.1.4',
    description='python(django) tracing middleware tool: django-jaeger-middleware',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='zhangpanpan',
    author_email='zhpan188@gmail.com',
    url='https://github.com/lpf32/shein-django-jaeger-middleware',
    packages=find_packages(),
    install_requires=[
        "jaeger_client",
        "opentracing",
        "requests"
    ],
    keywords=['django', 'jaeger', 'jaegertracing', 'requests'],
    classifiers=[
        "Framework :: Django",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    zip_safe=False
)