from setuptools import setup


setup(
    name='arseparse',
    version='0.1.2',
    description='Command-line app helper library',
    author='Sergio Garcez',
    author_email='garcez.sergio@gmail.com',
    url='https://github.com/sgarcez/arseparse',
    py_modules=['arseparse'],
    setup_requires=['pytest-runner'],
    tests_require=['mock', 'pytest-cov', 'pytest'],
    license='MIT',
    keywords=['cli', 'argparse', 'command-line'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
