import yaml


class ConfigReader:
    def __init__(self, config_path):
        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)

    def get_config(self):
        return self.config

    def get_attribute(self, attribute):
        if attribute not in self.config:
            raise ValueError(f"Invalid attribute: {attribute}")
        return self.config[attribute]


if __name__ == "__main__":
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))

    config_reader = ConfigReader(os.path.join(script_dir, "test.yaml"))
    print(config_reader.get_config())
