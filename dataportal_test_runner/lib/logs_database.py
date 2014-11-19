import time
import json
import dataset


class LogsDatabase(object):
    """Class used to store and retrieve information from the logs database.

    As tests are expected to take some time to run, this class specifically
    re-creates the database connection at each operation.

    @param url: Database URL
    """
    def __init__(self, url):
        self._url = url
        self._successes = []
        self._failures = []
        self._test_count = 0
        self._run_id = None

    def start_run(self, db=None):
        """Start a new test run

        @param db: Dataset connection or None
        """
        if db is None:
            db = dataset.connect(self._url)
        self._successes = []
        self._failures = []
        self._test_count = 0
        self._run_id = db['test_runs'].insert({
            'timestamp': int(time.time()),
            'running': 'running',
            'status': 'unknown',
            'successes': json.dumps(self._successes),
            'failures': json.dumps(self._failures),
            'test_count': 0
        })

    def log_test(self, successes, failures, db=None):
        """Store the results of a test

        @param successes: List of strings representing the successes
        @param failures: List of strings representing the successes
        @param db: Dataset connection or None
        """
        if db is None:
            db = dataset.connect(self._url)
        if self._run_id is None:
            self.start_run(db)
        self._successes += successes
        self._failures += failures
        self._test_count += len(successes) + len(failures)
        db['test_runs'].update({
            'id': self._run_id,
            'successes': json.dumps(self._successes),
            'failures': json.dumps(self._failures),
            'test_count': self._test_count
        }, ['id'])

    def finish_run(self, db=None):
        """Finish the current test run

        @param db: Dataset connection or None
        """
        if db is None:
            db = dataset.connect(self._url)
        if len(self._failures) > 0:
            db['test_runs'].update({
                'id': self._run_id,
                'running': 'finished',
                'status': 'failed'
            }, ['id'])
        else:
            db['test_runs'].update({
                'id': self._run_id,
                'running': 'finished',
                'status': 'passed'
            }, ['id'])
        self._successes = []
        self._failures = []
        self._run_id = None

    def query(self, count=10, db=None, **kargs):
        """Return test run information

        @param count: Number of test runs to return
        @param db: Dataset connection or None
        @param **kargs: Addition conditions
        @returns: List of dict representing the runs
        """
        if db is None:
            db = dataset.connect(self._url)
        results = []
        options = kargs
        options['_limit'] = count
        options['order_by'] = '-timestamp'
        for row in db['test_runs'].find(**options):
            r = dict(row)
            r['failures'] = json.loads(r['failures'])
            r['successes'] = json.loads(r['successes'])
            results.append(r)
        return results
