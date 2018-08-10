import os
from trinity import Logger
import yaml
import json
from copy import deepcopy

logger = Logger.get_logger("Config")


class _Config:
    """
        TODO: Pramod - Refactor and simplify the process of making config a <em>singleton</em>
    """
    DEFAULT_CONFIG_FILE = os.path.join(os.path.dirname(__file__), "../config/sample.yml")
    _ = {}

    def load(self, config_file):
        default_config = open(self.DEFAULT_CONFIG_FILE, "r")
        self._ = yaml.load(default_config)
        if config_file is not None and os.path.isfile(config_file):
            override_config = open(config_file, "r")
            overriden_configs = yaml.load(override_config)
            if not overriden_configs:
                logger.info("Empty overrides")
                return
            logger.info("Overriding Config Values")
            logger.info(json.dumps(overriden_configs, indent=4))
            self._ = merge_dictionaries(self._, overriden_configs)
        logger.info("Full config")
        logger.info(json.dumps(self._, indent=4))

    def get(self, config):
        keys = config.split(".")
        result = self._
        for key in keys:
            result = result[key]

        return result

    def fullConfigAsString(self):
        return json.dumps(self._, indent=2)


_config = _Config()


def merge_dictionaries(a, b):
    if not isinstance(b, dict):
        return b
    result = deepcopy(a)
    for k, v in b.iteritems():
        if k in result and isinstance(result[k], dict):
                result[k] = merge_dictionaries(result[k], v)
        else:
            result[k] = deepcopy(v)
    return result


def config(key,default=None):
    global _config
    value = None
    try:
        value = _config.get(key)
    except KeyError:
        value = default
    return value


def load(config_file):
    global _config
    _config.load(config_file)

def fullConfigAsString():
    global _config
    return _config.fullConfigAsString()
