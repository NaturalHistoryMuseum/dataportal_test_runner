import os
from setuptools import setup, find_packages

setup(
    name='dataportal_test_runner',
    version='0.1',
    description='Service to run and report on tests on the live data portal site',
    url='http://github.com/NaturalHistoryMuseum/dataportal_test_runner',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'dataportal_test_runner = dataportal_test_runner.cli:run'
        ]
    },
    data_files=[
        (
            os.path.join('/var/lib/dataportal_test_runner/', w[0]),
            w[2]
        ) for w in os.walk(os.path.join(os.path.dirname(__file__), 'casper_tests'))
    ]
)
