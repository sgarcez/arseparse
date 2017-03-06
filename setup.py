from setuptools import setup


setup(
    name='arseparse',
    version='0.1',
    description='Command-line app helper library',
    author='Sergio Garcez',
    author_email='garcez.sergio@gmail.com',
    url='https://github.com/sgarcez/arseparse',
    py_modules=['arseparse'],
    setup_requires=['pytest-runner'],
    tests_require=['mock', 'pytest'],
    keywords=['cli', 'argparse', 'command-line'],
)
