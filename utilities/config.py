import yaml


class ConfigFileReader:
    def __init__(self, config_file):
        self.config_file = config_file
        self.config = None
        self.read_config()

    def read_config(self):
        with open(self.config_file, 'r') as stream:
            try:
                parsed_yaml = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                raise exc
        self.config = parsed_yaml

    def get_config(self):
        return self.config
