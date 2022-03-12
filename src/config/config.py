import yaml
from .SingletonMeta import SingletonMeta


class Config(metaclass=SingletonMeta):
    CONFIG_FILE = "data/config/config.yaml"
    FABRIC_CONF_FILE = "data/config/fabric_config.yaml"

    def __init__(self):
        with open(self.CONFIG_FILE, 'r') as conf_file:
            self.config_data = yaml.load(conf_file, Loader=yaml.FullLoader)

    def save_config(self):
        with open(self.CONFIG_FILE, 'w') as conf_file:
            yaml.dump(self.config_data, conf_file, Dumper=yaml.Dumper)
        return self

    def reset_config(self):
        with open(self.FABRIC_CONF_FILE, 'r') as fabric_conf:
            self.config_data = yaml.load(fabric_conf, Loader=yaml.FullLoader)
            self.save_config()

    def set_collector_config(self, newconfig: dict):
        self.config_data['collector'] = newconfig

    def set_annotator_config(self, newconfig: dict):
        self.config_data['annotator'] = newconfig

    def change_collector_option(self, option_name, new_option):
        self.config_data['collector'][option_name] = new_option
        self.save_config()

    def get_collector_options(self) -> dict:
        return self.config_data['collector']

    def get_annotator_options(self) -> dict:
        return self.config_data['annotator']

    def get_colelctor_option(self, option_name):
        return self.config_data['collector'][option_name]

    def change_annotator_option(self, option_name, new_option):
        self.config_data['annotator'][option_name] = new_option

    def get_annotator_option(self, option_name):
        return self.config_data['annotator'][option_name]

    def get_file_option(self, option_name):
        return self.config_data['files'][option_name]

    def set_file_config_options(self, options: dict):
        self.config_data['files'] = options
        self.save_config()

    def print_config(self):
        print(self.config_data)
