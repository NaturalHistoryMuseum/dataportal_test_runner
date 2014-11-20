"""This test actually tests the behaviour of the json reports javascript

If casperjs or phantomjs are not in your path, then specify them using
CASPERJS_EXECUTABLE and PHANTOMJS_EXECUTABLE environment variables
respectively.
"""
import os
from subprocess import Popen, PIPE
from nose.tools import assert_in


class TestJsonReports(object):
    def test_json_reports(self):
        """Test that json_reports.js works"""
        if 'CASPERJS_EXECUTABLE' in os.environ:
            casperjs_executable = os.environ['CASPERJS_EXECUTABLE']
        else:
            casperjs_executable = 'casperjs'
        try:
            process = Popen(
                [
                    casperjs_executable,
                    'test', '--json', '--test-self',
                    os.path.join(
                        os.path.dirname(__file__),
                        '../../casper_tests/json_report.js'
                    )
                ],
                stdout=PIPE,
                stderr=PIPE
            )
        except OSError as e:
            return
        stdout_data, stderr_data = process.communicate()
        assert_in(
            '#JSON{"successes":["test json_report.js: a success"],"failures":["test json_report.js: a failure"]}',
            stdout_data.split("\n")
        )