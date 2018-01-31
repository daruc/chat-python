"""Provides definitions of resources and configuration registers."""

import os
import re


class StringsRegister(dict):
    """Contains labels for each language which are showing in UI."""

    def __init__(self, language):
        super().__init__()
        self.language = language

        path = '../resources/strings-' + language + '.txt'
        file = open(path, 'r', encoding='utf-8')

        for line in file:
            key, value = line.split('=')
            self[key.strip()] = value.strip()


class ConfigRegister(dict):
    """Singleton containing application configurations."""

    __instance = None

    def __init__(self):
        super().__init__()
        file = open('../resources/config.txt', 'r', encoding='utf-8')

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
        """Looking for strings-*.txt files and returns language suffixes."""

        files = os.listdir('../resources/')
        result = []
        for file in files:
            if re.search(r'^strings-.*\.txt$', file):
                match_obj = re.match(r'^strings-(.*)\.txt$', file)
                language = match_obj.group(1)
                result.append(language)
        return result

    def save(self):
        """Saves configuration from memory to disc."""

        file = open('../resources/config.txt', 'w', encoding='utf-8')

        for key, value in self.items():
            file.write(key + '=' + value + '\n')
        file.close()

    @classmethod
    def get_instance(cls):
        """Returns instance of ConfigRegister."""

        if ConfigRegister.__instance is None:
            ConfigRegister.__instance = ConfigRegister()

        return ConfigRegister.__instance
