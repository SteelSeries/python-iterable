from distutils.core import setup


setup(
    name='iterable',
    version='0.1.0',
    description='Iterable python bindings',
    author='SteelSeries',
    author_email='eric.burns@steelseries.com',
    url='https://github.com/SteelSeries/python-iterable',
    packages=['iterable', 'iterable.test', 'iterable.test.resources'],
    install_requires=['requests==2.9.1', ],
    test_suite='iterable.test',
    tests_require=['mock==1.3.0', ],
)
