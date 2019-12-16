from setuptools import setup, find_packages


setup(
    name = 'thoughtprocess',
    version = '0.1.0',
    author = 'Assaf Manor',
    description = 'A mind reading and recording software.',
    packages = find_packages(),
    install_requires = ['click', 'flask', 'Pillow'],
    tests_require = ['pytest', 'pytest-cov'],
)
