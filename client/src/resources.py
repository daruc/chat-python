import os
import re

class StringsRegister(dict):

    def __init__(self, language):
        self.language = language

        path = '../resources/strings-' + language + '.txt'
        file = open(path)

        for line in file:
            key, value = line.split('=')
            self[key.strip()] = value.strip()


class ConfigRegister(dict):
    __instance = None

    def __init__(self):
        file = open('../resources/config.txt')

        for line in file:
            key, value = line.split('=')
            self[key.strip()] = value.strip()

        file.close()

    def __getitem__(self, item):
        if item == 'languages_list':
            return self._get_available_languages()
        return dict(self)[item]

    @staticmethod
    def _get_available_languages():
        files = os.listdir('../resources/')
        result = []
        for file in files:
            if re.search(r'^strings-.*\.txt$', file):
                match_obj = re.match(r'^strings-(.*)\.txt$', file)
                language = match_obj.group(1)
                result.append(language)
        return result

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
