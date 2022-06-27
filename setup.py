from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='bugsplat',
    version='1.0.1',
    description='A Python package for sending Unhandled Exceptions to BugSplat',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/BugSplat-Git/bugsplat-py',
    author='BugSplat',
    author_email='support@bugsplat.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords='crash, reporting, bugsplat, unhandled, exception, diagnostics, debug, debugging, stack, trace',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.6, <4',
    install_requires=[
        'requests'
    ],
    project_urls={
        'Bug Reports': 'https://github.com/BugSplat-Git/bugsplat-py/issues',
        'BugSplat': 'https://www.bugsplat.com',
    },
)