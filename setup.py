import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

if not os.path.exists('pimanager/VERSION'):
    version = '0'
else:
    with open('pimanager/VERSION', 'r') as fp:
        version = fp.read().strip()
        version = version[1:]  # Remove v before version number

setup(
    name='pimanager',
    version=version,
    packages=find_packages(),
    include_package_data=True,
    license='GPL',
    description='A django app to monitor status and manage Raspberry Pi devices',
    long_description=README,
    url='https://github.com/datagutten/pimanager',
    author='Anders Birkenes',
    author_email='datagutten@datagutten.net',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.1',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ], install_requires=['django', 'switchinfo']
)
