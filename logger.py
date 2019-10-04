import logging
import os
import json
import traceback
import os


_general_level = os.environ.get('godmode', 'info').upper()
_logger_config_path = './data/logger.json'
_module_logger_config = {
	'logfile': 'debug'
}


if os.path.exists(_logger_config_path):
	with open(_logger_config_path, 'r') as out:
		config = json.loads(out.read())
	_module_logger_config.update(config)


_level = {
	"CRITICAL": 50,
	"ERROR": 40,
	"WARNING": 30,
	"INFO": 20,
	"DEBUG": 10,
	"NOTSET": 0,
}

formatter = logging.Formatter('[ %(levelname)s ]%(name)s: %(message)s')
file_formatter = logging.Formatter('%(asctime)s[ %(levelname)s ]%(name)s: %(message)s')


_sthandler = logging.StreamHandler()
_sthandler.setLevel(logging.DEBUG)
_sthandler.setFormatter(formatter)

_fhandler = logging.FileHandler('log', mode="w+")
_fhandler.setFormatter(file_formatter)
_fhandler.setLevel(_level[_module_logger_config['logfile'].upper()])

def getLogLevel(name):
	log_level = _module_logger_config.get(name, _general_level).upper()
	return _level.get(log_level)

def Logger(name):
	log_level = _module_logger_config.get(name, _general_level).upper()

	logger = logging.getLogger(name)
	logger.setLevel(_level.get(log_level))
	logger.addHandler(_sthandler)
	logger.addHandler(_fhandler)

	return logger



if __name__ == '__main__':
	log1 = Logger(__name__)

	log1.info('asdasd')
	log1.debug('asdasdasdasdasdasd')
	log1.error('asdasdasdasdasdasd')

	log2 = Logger('test1')
	log1.debug('asdasdasdasdasdasd1')
	log1.error('asdasdasdasdasdasd1')
