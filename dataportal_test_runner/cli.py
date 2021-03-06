#!/usr/bin/env python
""" Dataportal test runner

This is used to run the tests, and log the results in the configured database.

Usage: dataportal_test_runner [options] run
       dataportal_test_runner [options] report

Options:
    -h --help       Show this screen.
    --version       Show version.
    -c CONFIG-FILE  Configuration file [default: /etc/dataportal_test_runner/dataportal_test_runner.json]
    -j TEST-NAME    Only run scripts with name 'test_TEST-NAME.js'
    -n COUNT        Number of runs to display in the report [default: 1]
    -r              Include non-finished runs in the report
    -x              Only show failed runs in the report
    -t TIME         Exit with a non-zero status if the last report has failures,
                    or if no reports were run in the last TIME seconds
    -i              Specify test run ID to display in the report
    -v              Also include details of passed tests in the report.
    --tty           Output as if stdout was a terminal (output run steps and
                    prettify json report)
    --not-tty       Output as if stdout wasn't a terminal (run is silent, and
                    json report is compact)
"""
import os
import sys
import json
import time
import datetime
import docopt
import StringIO
from dataportal_test_runner.lib.casper_test_runner import CasperTestRunner
from dataportal_test_runner.lib.logs_database import LogsDatabase
from dataportal_test_runner.config import read_config

from version import __version__


def run_tests(test_name, config, stdout):
    """Run the test suite

    @param test_name: Name of a test (where the corresponding script will be
                      test_NAME.js) or False to run all tests
    @param quiet: True to suppress output
    @param config: dict configuration object
    """
    logs = LogsDatabase(config['logs_db'])
    try:
        for entry in os.walk(config['casper_tests']):
            for script in entry[2]:
                run_it = script.startswith('test') and script.endswith('.js')
                if test_name:
                    run_it = run_it and "test_{}.js".format(test_name) == script
                if run_it:
                    stdout.write("#Running tests for {}".format(script) + "\n")
                    runner = CasperTestRunner(
                        os.path.join(entry[0], script),
                        config['test_url'],
                        config['casper_js'],
                        config['phantom_js']
                    )
                    runner.run()
                    logs.log_test(runner.successes(), runner.failures())
                    if runner.status():
                        stdout.write('PASS {}'.format(script) + "\n")
                    else:
                        stdout.write('FAIL {}'.format(script) + "\n")
    except Exception as e:
        logs.log_test(
            [],
            ['Runner raised un-caught exception : {}'.format(str(e))]
        )
        stdout.write(
            "FAIL Runner raised un-caught exception : {}".format(str(e)) +
            "\n"
        )
    finally:
        logs.finish_run()


def report(count, running, failed, indicate_failure, run_id, verbose,
           pretty, config, stdout):
    """Display the last test runs

    @param count: Number of test runs to display
    @param running: If True, also display running tasks
    @param failed: If True, only display failed runs
    @param indicate_failure: If not None, then exit with non zero status code
        if the last run failed or there was no run in the given number of
        seconds
    @param run_id: If defined and not False, only display that run id
    @param verbose: If True, output individual success/failure
    @param pretty: If True, indent the output json for readability
    @param config: dict configuration
    """
    logs = LogsDatabase(config['logs_db'])
    conditions = {}
    if not running:
        conditions['running'] = 'finished'
    if failed:
        conditions['status'] = 'failed'
    if run_id is not False:
        conditions['id'] = run_id
    log_report = []
    for row in logs.query(count, **conditions):
        r = row.copy()
        if not verbose:
            del r['successes']
        if pretty:
            r['date'] = datetime.datetime.fromtimestamp(
                r['timestamp']
            ).strftime('%Y-%m-%d %H:%M:%S')
        log_report.append(r)
    if pretty:
        stdout.write(json.dumps(log_report, indent=2, sort_keys=True) + "\n")
    else:
        stdout.write(json.dumps(log_report))
    if indicate_failure is not None:
        if len(log_report) == 0:
            return 1
        elif len(log_report[0]['failures']) > 0:
            return 1
        elif time.time() - log_report[0]['timestamp'] > int(indicate_failure):
            return 1

    return 0


def run():
    """Setup tools entry point"""
    arguments = docopt.docopt(__doc__, help=True, version=__version__)
    config = read_config(arguments['-c'])
    is_tty = os.isatty(sys.stdout.fileno())
    if arguments['run']:
        test_name = arguments['-j']
        if arguments['--tty'] or (is_tty and not arguments['--not-tty']):
            stdout = sys.stdout
        else:
            stdout = StringIO.StringIO()
        run_tests(test_name, config, stdout)
    elif arguments['report']:
        count = int(arguments['-n'])
        verbose = arguments['-v']
        running = arguments['-r']
        run_id = arguments['-i']
        failed = arguments['-x']
        pretty = arguments['--tty'] or (is_tty and not arguments['--not-tty'])
        indicate_failure = arguments['-t']
        rc = report(count, running, failed, indicate_failure, run_id,
               verbose, pretty, config, sys.stdout)
        exit(rc)

if __name__ == '__main__':
    run()