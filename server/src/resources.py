"""Provides definition of configuration register."""


class ConfigRegister(dict):
    """Singleton containing server configurations."""

    __instance = None

    def __init__(self):
        super().__init__()
        file = open('../resources/config.txt', 'r', encoding='utf-8')

        for line in file:
            key, value = line.split('=')
            self[key.strip()] = value.strip()

        file.close()

    def save(self):
        """Saves configuration from memory to disc."""

        file = open('../resources/config.txt', 'w', encoding='utf-8')

        for key, value in self.items():
            file.write(key + '=' + value + '\n')
        file.close()

    @classmethod
    def get_instance(cls):
        """Returns singleton of this class."""

        if ConfigRegister.__instance is None:
            ConfigRegister.__instance = ConfigRegister()

        return ConfigRegister.__instance
