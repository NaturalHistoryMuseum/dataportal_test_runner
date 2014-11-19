Data Portal Test Runner
=======================

The Data Portal Test Runner is a utility for continuous running of tests on the live version of the Data Portal. Note that this is not about continuous integration or testing the code base (this is done separately as part of each component's code base, and typically run on test data rather than the full museum dataset). This is about testing the live version of the site, to ensure it is running as expected.

Usage
-----

The tests are run by invoking:

    dataportal_test_runner run

This should be set up using a CRON task to run as many times as required (at 
least once a day is recommended).

The reports are generated as JSON reports by invoking:

    dataportal_test_runner report

The full list of options:

    $ dataportal_test_runner --help
    Dataportal test runner
    
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
        -i              Specify test run ID to display in the report
        -v              Also include details of passed tests in the report.
        --tty           Output as if stdout was a terminal (output run steps and
                        prettify json report)
        --not-tty       Output as if stdout wasn't a terminal (run is silent, and
                        json report is compact)

Installing
----------
The Data Portal Test Runner requires [CasperJS](http://casperjs.org). In turn,
CasperJS requires [PhantomJS](http://phantomjs). The simplest way to install
both globally is to use [npm](http://npmjs.org):

    npm install -g casperjs
    
To install the Data Portal Test Runner you can run:

    pip install git+https://github.com/NaturalHistoryMuseum/dataportal_test_runner.git#egg=dataportal_test_runner

Note that will install the tests globally under `/var/lib/dataportal_test_runner/casper_tests`.  
    
Configuring
-----------

The configuration is a JSON file (with comments allowed), and by default stored
in `/etc/dataportal_test_runner/dataportal_test_runner.json`. It should contain
the following keys:

    ```json
    /*
     * Dataportal test runner configuration. This is a JSON file. Comments are
     * allowed.
     */
    {
      /* URL to test */
      "test_url": "http://data.nhm.ac.uk",
    
      /* Path to the casper tests to run */
      "casper_tests": "/var/lib/dataportal_test_runner/casper_tests",
    
      /* URL to the database to store results */
      "logs_db": "sqlite:////var/lib/dataportal_test_runner/logs.db",
    
      /* Path to CasperJS */
      "casper_js": "/usr/bin/casperjs",
    
      /* Path to PhantomJS. May be empty if PhamtomJS is in your path */
      "phantom_js": "/usr/bin/phantomjs"
    }
    ```