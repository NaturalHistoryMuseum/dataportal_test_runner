import os
from setuptools import setup, find_packages


with open('dataportal_test_runner/version.py') as f:
    exec(f.read())


def _find_data_files(root, dest):
    """ Helper function to gather data files recursively """
    here = os.path.dirname(__file__)
    result = []
    list = os.walk(os.path.join(here, root))
    for directory, folders, files in list:
        result.append((
            os.path.join(dest, os.path.relpath(directory, here)),
            [os.path.join(directory, f) for f in files]
        ))
    return result


setup(
    name='dataportal_test_runner',
    version=__version__,
    description='Service to run and report on tests on the live data portal site',
    url='http://github.com/NaturalHistoryMuseum/dataportal_test_runner',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'dataportal_test_runner = dataportal_test_runner.cli:run'
        ]
    },
    data_files=_find_data_files(
        'casper_tests',
        'share/dataportal_test_runner'
    ),
    install_requires=[
        'dataset==0.5.5',
        'docopt==0.6.2',
        'jsmin==2.0.11'
    ]
)
