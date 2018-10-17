#!/usr/bin/env python

from distutils.core import setup
from setuptools import find_packages

README_FILE = open('README.rst')
try:
    long_description = README_FILE.read()
finally:
    README_FILE.close()

setup(name='django-multipageforms',
        version='0.6.0',
        packages=['multipageforms'],
        package_dir={'': 'src'},
        include_package_data=True,
        zip_safe=False,
        platforms=['any'],
        description='Form wizard is dead, long live multipageforms',
        author_email='kaleissin@gmail.com',
        author='kaleissin',
        url='https://github.com/kaleissin/django-multipageforms',
        long_description=long_description,
        classifiers=[
                'Development Status :: 4 - Beta',
                'Environment :: Web Environment',
                'Framework :: Django',
                'Intended Audience :: Developers',
                'License :: OSI Approved :: MIT License',
                'Operating System :: OS Independent',
                'Framework :: Django :: 1.8',
                'Framework :: Django :: 1.11',
                'Programming Language :: Python',
                'Programming Language :: Python :: 2',
                'Programming Language :: Python :: 2.7',
                'Programming Language :: Python :: 3',
                'Programming Language :: Python :: 3.5',
                'Programming Language :: Python :: 3.6',
                'Programming Language :: Python :: 3.7',
                'Topic :: Software Development :: Libraries :: Application Frameworks',
                'Topic :: Software Development :: Libraries :: Python Modules',
        ]
)
