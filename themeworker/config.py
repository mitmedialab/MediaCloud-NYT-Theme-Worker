import codecs
import os
import logging

COMMENT_CHAR = u'#'

logger = logging.getLogger(__name__)


def _variables_from_file(filepath):
    vars = {}
    logger.info(u"Loading configuration from {}".format(filepath))
    try:
        f = codecs.open(filepath, 'r', 'utf-8')
        for line in f:
            if len(line.strip()) is 0:
                continue
            if line.strip()[0] == COMMENT_CHAR:
                continue
            parts = line.split(u"=")
            key = parts[0].strip().upper()
            value = parts[1].strip()
            logger.debug(u"  {}={}".format(key, value))
            if key in vars:
                raise ConfigException(u"Config variable '{}' is declared twice in {}".format(key, filepath))
            vars[key] = value
    except IOError:
        logger.info(u"No local app.config file found; relying on environment variables for configuration")

    return vars


class ConfigException(Exception):
    def __init__(self, message, status_code=0):
        Exception.__init__(self, message)
        self.status_code = status_code


class EnvOrFileBasedConfig(object):
    # Simple wrapper around a text config file; lets us load from a text file (dev) or from env-vars (prod)

    def __init__(self, absolute_filepath):
        self.file_path = absolute_filepath
        self.variables = _variables_from_file(self.file_path)  # a dict from VARIABLE_NAME to value

    def get(self, key):
        variable_name = key.upper()
        try:
            return os.environ[variable_name]
        except KeyError:
            try:
                return self.variables[variable_name]
            except KeyError:
                error_details = u"Config variable '{}' not declared in env-var nor in {}".format(variable_name, self.file_path)
                logger.warn(error_details)
                raise ConfigException(error_details)


def get_default_config():
    base_dir = os.path.dirname(os.path.dirname((os.path.abspath(__file__))))
    path_to_config_file = os.path.join(base_dir, 'config', 'app.config')
    config = EnvOrFileBasedConfig(path_to_config_file)
    return config
