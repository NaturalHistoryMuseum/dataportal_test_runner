#!/usr/bin/env python
import os
import sys
import json

phantomjs = ''
if 'PHANTOMJS_EXECUTABLE' in os.environ:
    phantomjs = os.environ['PHANTOMJS_EXECUTABLE']

report = {
    'successes': [phantomjs, sys.argv],
    'failures': []
}

if phantomjs == '~failures~':
    report['failures'].append('a failure')


print 'PASS something'
print 'FAIL something'
print '# something'
print ''
print 'JSON carrot'

if phantomjs == '~bad json~':
    print '#JSON{broken;;;'
elif phantomjs == '~bad schema~':
    print '#JSON' + json.dumps({'a': 'b', 'c': 'd'})
elif phantomjs == '~all empty~':
    print '#JSON' + json.dumps({'successes': [], 'failures': []})
elif phantomjs != "~no output~":
    print '#JSON' + json.dumps(report)
print 'whatever'