"""This test actually tests the behaviour of the json reports javascript

It requires two environment variables:
- CASPERJS_EXECUTABLE: Path to casper JS
- PHANTOMJS_EXECUTABLE: Path to Phatom JS
"""
import os
from subprocess import Popen, PIPE
from nose.tools import assert_in


class TestJsonReports(object):
    def test_json_reports(self):
        """Test that json_reports.js works"""
        process = Popen(
            [
                os.environ['CASPERJS_EXECUTABLE'],
                'test', '--json', '--test-self',
                os.path.join(
                    os.path.dirname(__file__),
                    '../../casper_tests/json_report.js'
                )
            ],
            stdout=PIPE,
            stderr=PIPE
        )
        stdout_data, stderr_data = process.communicate()
        assert_in(
            '#JSON{"successes":["test json_report.js: a success"],"failures":["test json_report.js: a failure"]}',
            stdout_data.split("\n")
        )