import os
from configparser import ConfigParser, NoOptionError


config_path = "~/.esgf2flows.ini"


class Config:
    def __init__(self):
        self.config = ConfigParser()
        self._config_path = os.path.expanduser(config_path)
        if os.path.isfile(self._config_path):
            self.config.read(self._config_path)
            for section in ["main", "tokens", "flows", "functions"]:
                if not section in self.config.sections():
                    self.config.add_section(section)
            with open(self._config_path, "w") as cf:
                self.config.write(cf)
        else:
            with open(self._config_path, "w+") as cf:
                self.config.add_section("main")
                self.config.add_section("tokens")
                self.config.add_section("flows")
                self.config.add_section("functions")
                self.config.write(cf)

    def set(self, section, key, value):
        if not section in self.config.sections():
            self.config.add_section(section)
        self.config.set(section, key, value)
        with open(self._config_path, "w") as cf:
            self.config.write(cf)

    def get(self, section, key):
        if section in self.config.sections():
            try:
                return self.config.get(section, key)
            except NoOptionError:
                return None
        return None
