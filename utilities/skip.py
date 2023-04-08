import utilities.env_config
from utilities.config import ConfigFileReader


def skip_send(file_path):
    if utilities.env_config.get_config_with_default("SKIP_CONFIG_FILE", False):
        skip_config = ConfigFileReader().get_config()
        return should_skip(file_path, skip_config)
    else:
        return False


def should_skip(file_path, skip_config):
    for pattern in skip_config['patterns_to_skip']:
        if pattern['match_string'] in file_path:
            return True
    return False
