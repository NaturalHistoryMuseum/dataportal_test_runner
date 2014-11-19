"""Test TestCasperTestRunner

This relies on a fake script to replace casperjs (see fake_casperjs.py)
"""
import os
from nose.tools import assert_equals, assert_in, assert_true, assert_false
from dataportal_test_runner.lib.casper_test_runner import CasperTestRunner


class TestCasperTestRunner(object):
    def setUp(self):
        """Locate fake casperjs and test data"""
        self._casperjs = os.path.join(
                os.path.dirname(__file__),
                'fake_casperjs.py'
        )

    def test_casperjs_invoked_and_parsed(self):
        """Ensure that casper js is invoked and results are parsed"""
        runner = CasperTestRunner('a', 'b', self._casperjs)
        runner.run()
        s = runner.successes()
        assert_equals(2, len(s))

    def test_casperjs_test_invoked(self):
        """Ensure that casper js is invoked with the test command"""
        runner = CasperTestRunner('a', 'b', self._casperjs)
        runner.run()
        s = runner.successes()
        assert_in('test', s[1][1])

    def test_casperjs_script_name(self):
        """Ensure that casperjs is invoked with the correct script"""
        runner = CasperTestRunner('thescript.js', 'b', self._casperjs)
        runner.run()
        s = runner.successes()
        assert_in('thescript.js', s[1])

    def test_casperjs_url(self):
        """Ensure that casperjs is invoked with the correct url"""
        runner = CasperTestRunner('a', 'http://example.com', self._casperjs)
        runner.run()
        s = runner.successes()
        assert_in('--url=http://example.com', s[1])

    def test_casperjs_json_mode(self):
        """Ensure that casperjs is invoked with json mode"""
        runner = CasperTestRunner('a', 'b', self._casperjs)
        runner.run()
        s = runner.successes()
        assert_in('--json', s[1])

    def test_casperjs_phatomjs(self):
        """Ensure that PhantomJS path is passed to casperJS"""
        runner = CasperTestRunner('a', 'b', self._casperjs, '/path/to/phantom')
        runner.run()
        s = runner.successes()
        assert_equals('/path/to/phantom', s[0])

    def test_status_success(self):
        """Ensure that status is true if there are no errors"""
        runner = CasperTestRunner('a', 'b', self._casperjs, '/path/to/phantom')
        runner.run()
        assert_true(runner.status())

    def test_status_error(self):
        """Ensure that status is false if there are errors"""
        runner = CasperTestRunner('a', 'b', self._casperjs, '~failures~')
        runner.run()
        assert_false(runner.status())

    def test_failures_parsed(self):
        """Ensure that failures are parsed"""
        runner = CasperTestRunner('a', 'b', self._casperjs, '~failures~')
        runner.run()
        f = runner.failures()
        assert_equals(1, len(f))
        assert_equals(['a failure'], f)

    def test_no_output_becomes_failure(self):
        """Ensure that if no json output is found, a failure is added"""
        runner = CasperTestRunner('a', 'b', self._casperjs, '~no output~')
        runner.run()
        f = runner.failures()
        assert_equals(1, len(f))
        assert_false(runner.status())

    def test_broken_json_becomes_failure(self):
        """Ensure that if json is badly formatted, a failure is added"""
        runner = CasperTestRunner('a', 'b', self._casperjs, '~bad json~')
        runner.run()
        f = runner.failures()
        assert_equals(1, len(f))
        assert_false(runner.status())

    def test_wrong_json_schema_becomes_failure(self):
        """Ensure that if the returned json doesn't include the expected fields
        a failure is added"""
        runner = CasperTestRunner('a', 'b', self._casperjs, '~bad schema~')
        runner.run()
        f = runner.failures()
        assert_equals(1, len(f))
        assert_false(runner.status())

    def test_no_results_becomes_failure(self):
        """Ensure that if there are no successes and no failues, then a failure
        is added"""
        runner = CasperTestRunner('a', 'b', self._casperjs, '~all empty~')
        runner.run()
        f = runner.failures()
        assert_equals(1, len(f))
        assert_false(runner.status())

    def test_absent_script_becomes_failure(self):
        """Ensure that if casperjs is not found, then a failure is added"""
        runner = CasperTestRunner('a', 'b', self._casperjs + 'x')
        runner.run()
        f = runner.failures()
        assert_equals(1, len(f))
        assert_false(runner.status())
