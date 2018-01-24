class ConfigRegister(dict):
    __instance = None

    def __init__(self):
        super().__init__()
        file = open('../resources/config.txt')

        for line in file:
            key, value = line.split('=')
            self[key.strip()] = value.strip()

        file.close()

    def save(self):
        file = open('../resources/config.txt', 'w')

        for key, value in self.items():
            file.write(key + '=' + value + '\n')
        file.close()

    @classmethod
    def get_instance(cls):
        if ConfigRegister.__instance is None:
            ConfigRegister.__instance = ConfigRegister()

        return ConfigRegister.__instance
