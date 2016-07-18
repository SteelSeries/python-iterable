from distutils.core import setup


setup(
    name='iterable',
    version='0.0.1',
    description='Iterable python bindings',
    keywords='iterable, api',
    author='Eric Burns <eric.burns@steelseries.com>',
    author_email='eric.burns@steelseries.com',
    url='https://github.com/SteelSeries/python-iterable',
    license='MIT',
    packages=['iterable', 'iterable.test', 'iterable.test.resources'],
    install_requires=['requests==2.9.1', ],
    test_suite='iterable.test',
    tests_require=['mock==1.3.0', ],
    zip_safe=False,
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Environment :: Web Environment',
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7'
    ],
)
