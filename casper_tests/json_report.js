/**
 * Module to include a JSON report in the CasperJS output if --json
 * was specified as an option.
 *
 * The JSON is output as a single line starting with '#JSON' followed by a
 * JSON object.
 *
 * Usage:
 * Add `require('json_report')` at the begining of a casperjs test script.
 *
 */

if (casper.cli.options['json']) {
  var _casper_json_report = {
    successes: [],
    failures: [],

    /**
     * Internal method to format casperjs messages such that:
     * - all newlines are removed;
     * - empty messages are replace by a '-'
     */
    _nl: function (str) {
      if (typeof(str) == 'string') {
        return str.replace(/\r?\n|\r/g, ' ');
      } else {
        return '-';
      }
    },

    /**
     * Add a new failure
     */
    failure: function (f) {
      this.failures.push(this._nl(f['suite']) + ': ' + this._nl(f['message']));
    },

    /**
     * Add a new success
     */
    success: function (f) {
      this.successes.push(this._nl(f['suite']) + ': ' + this._nl(f['message']));
    },

    /**
     * Return JSON report
     */
    report: function () {
      return JSON.stringify({
        successes: this.successes,
        failures: this.failures
      });
    }
  };

  casper.test.on('fail', function (f) {
    _casper_json_report.failure(f);
  });
  casper.test.on('success', function (f) {
    _casper_json_report.success(f);
  });
  casper.test.on('exit', function () {
    casper.echo('#JSON' + _casper_json_report.report());
  });
}

/**
 * Tests to test the script's own functionality! Invoke as
 * casperjs test --json --test-self json_report.js and ensure
 * that the output includes:
 * #JSON{"successes":["test json_report.js: a success"],"failures":["test json_report.js: a failure"]}
 */
if (casper.cli.options['test-self']) {
  casper.test.begin("test json_report.js", 1, function(test) {
    test.assertTrue(true, 'a success');
    test.assertTrue(false, 'a failure');
    test.done();
  });
}