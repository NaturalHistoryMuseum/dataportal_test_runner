import os
import time
import tempfile
import shutil
from nose.tools import assert_true, assert_equals
from dataportal_test_runner.lib.logs_database import LogsDatabase

class TestLogsDatabase(object):
    """Test the LogsDatabase class"""
    def setUp(self):
        """Create a temporary folder for the database"""
        self._temp = tempfile.mkdtemp()
        self._db = LogsDatabase(
            'sqlite:////' + os.path.join(self._temp, 'db.db')
        )

    def tearDown(self):
        """Remove temporary folder"""
        shutil.rmtree(self._temp)

    def test_run_is_created(self):
        """Test that the run is created in the logs"""
        self._db.start_run()
        self._db.finish_run()
        assert_equals(len(self._db.query()), 1)

    def test_multiple_runs_are_created(self):
        """Test that multiple runs get added in the logs"""
        self._db.start_run()
        self._db.finish_run()
        self._db.start_run()
        self._db.finish_run()
        assert_equals(len(self._db.query()), 2)

    def test_multiple_logs_in_same_run(self):
        """Test that multiple logs in a single run do not add more runs"""
        self._db.start_run()
        self._db.log_test(['a'], ['b'])
        self._db.log_test(['c'], ['d'])
        self._db.log_test(['e'], ['f'])
        self._db.finish_run()
        assert_equals(len(self._db.query()), 1)

    def test_run_timestamp(self):
        """Test that a run entry contains the expected timestamp"""
        start_time = int(time.time())
        self._db.start_run()
        self._db.finish_run()
        end_time = int(time.time())
        data = self._db.query()[0]
        assert_true(data['timestamp'] >= start_time)
        assert_true(data['timestamp'] <= end_time)

    def test_run_finished(self):
        """Test that a finished run is marked as finished"""
        self._db.start_run()
        self._db.finish_run()
        data = self._db.query()[0]
        assert_equals(data['running'], 'finished')

    def test_run_running(self):
        """Test that a non-finished run is marked as running"""
        self._db.start_run()
        data = self._db.query()[0]
        assert_equals(data['running'], 'running')

    def test_run_test_count(self):
        """Test that a run entry contains the expected test count"""
        self._db.start_run()
        self._db.log_test(['a'], ['b'])
        self._db.log_test(['c'], ['d'])
        self._db.log_test(['e'], ['f'])
        self._db.finish_run()
        data = self._db.query()[0]
        # 3 successes + 3 failures means 6 tests were performed
        assert_equals(data['test_count'], 6)

    def test_run_status_passed(self):
        """Test that a run with no failures is marked as passed"""
        self._db.start_run()
        self._db.log_test(['a'], [])
        self._db.log_test(['c'], [])
        self._db.finish_run()
        data = self._db.query()[0]
        assert_equals(data['status'], 'passed')

    def test_run_status_failed(self):
        """Test that a run with failures is marked as failed"""
        self._db.start_run()
        self._db.log_test(['a'], [])
        self._db.log_test(['c'], ['d'])
        self._db.finish_run()
        data = self._db.query()[0]
        assert_equals(data['status'], 'failed')

    def test_run_successes(self):
        """Test that a run entry contains the expected successes"""
        self._db.start_run()
        self._db.log_test(['a'], ['b'])
        self._db.log_test(['c'], ['d'])
        self._db.log_test(['e'], ['f'])
        self._db.finish_run()
        data = self._db.query()[0]
        assert_equals(data['successes'], ['a', 'c', 'e'])

    def test_run_failures(self):
        """Test that a run entry contains the expected failures"""
        self._db.start_run()
        self._db.log_test(['a'], ['b'])
        self._db.log_test(['c'], ['d'])
        self._db.log_test(['e'], ['f'])
        self._db.finish_run()
        data = self._db.query()[0]
        assert_equals(data['failures'], ['b', 'd', 'f'])
