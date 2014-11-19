import os
import json
from subprocess import Popen, PIPE


class CasperTestRunner(object):
    """ Class used to run and return the result of a casper test

    @param test_file: The name of the file containing the casper test
    @param url: The URL to test
    @param casper: Path to casper executable
    @param phantom: Path to PhantomJS executable
    """
    def __init__(self, test_file, url, casper, phantom=''):
        self._test_file = test_file
        self._url = url
        self._casper = casper
        self._phantom = phantom
        self._successes = []
        self._failures = ['Test {} was not run'.format(self._test_file)]

    def run(self):
        """Run the test. This is a wrapper around the actual code to ensure
        all exceptions are reported as errors"""
        try:
            self._run()
        except Exception as e:
            self._failures.append("Test runner failed with {}".format(str(e)))

    def _run(self):
        """Run the test"""
        # Invoke casperjs
        env = os.environ.copy()
        if self._phantom:
            env['PHANTOMJS_EXECUTABLE'] = self._phantom
        try:
            #TODO: Implement timeout.
            process = Popen(
                [
                    self._casper,
                    'test', '--json', '--url={}'.format(self._url),
                    self._test_file
                ],
                stdout=PIPE,
                stderr=PIPE,
                env=env
            )
        except OSError:
            self._successes = []
            self._failures = [
                'Os error (not found?) with {}'.format(self._casper)
            ]
            return

        # Look for the JSON report
        stdout_data, stderr_data = process.communicate()
        self._successes = []
        self._failures = []
        for line in stdout_data.split("\n"):
            if line.startswith('#JSON{'):
                try:
                    report = json.loads(line[5:])
                    self._successes = report['successes']
                    self._failures = report['failures']
                except (KeyError, ValueError) as e:
                    self._successes = []
                    self._failures = [
                        'Failed to parse JSON report from test {}'.format(self._test_file)
                    ]
        if len(self._successes) == 0 and len(self._failures) == 0:
            self._failures = [
                'Test {} did not run or did not produce a report.'.format(self._test_file)
            ]

    def status(self):
        """Return True if the test passed, False otherwise"""
        return len(self._failures) == 0

    def successes(self):
        """Return the successes from the last run"""
        return self._successes

    def failures(self):
        """Return the failures from the last run"""
        return self._failures

