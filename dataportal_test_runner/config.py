import json
import jsmin

_defaults = {
    'test_url': 'http://127.0.0.1',
    'logs_db': 'sqlite:////var/lib/dataportal_test_runner/log.db',
    'casper_js': '/usr/bin/casperjs',
    'phantom_js': '',
}


def read_config(file_name):
    """Read the given JSON configuration file and apply missing defaults

    @param file_name: File name to JSON configuration file
    @rtype: dict
    """
    with open(file_name) as f:
        config = json.loads(jsmin.jsmin(f.read()))
    for key in _defaults:
        if key not in config:
            config[key] = _defaults[key]
    return config