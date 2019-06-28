import os
import json

from django.conf import settings
from django.template.defaultfilters import slugify
from django.core.files import File
from django.core.files.storage import FileSystemStorage


class FileStorage(FileSystemStorage):
    def __init__(self, location=None, base_url=None):
        location = location if location else settings.FILES_ROOT
        base_url = base_url if base_url else settings.FILES_URL
        super(FileStorage, self).__init__(location, base_url)

    def list(self):
        file_list = []
        for f in os.listdir(self.location):
            f_path = os.path.join(self.base_location, f)
            if os.path.isfile(f_path):
                f_size = os.path.getsize(f_path)
                file_list.append({
                    'name': f,
                    'id': slugify(f),
                    'url': self.base_url + f,
                    'size': f_size,
                })
        return file_list

    def delete(self, name):
        assert name, "The name argument is not allowed to be empty."
        name = self.path(name)
        try:
            if os.path.isfile(name):
                os.remove(name)
                return True
        except FileNotFoundError:
            pass
        return False


def _create_file_object_from_json(json_data):
    """Принимает json с сериализованным файлом. Возвращает название файла и объект File"""
    print('JSON_DATA:', json_data)
    data = json.loads(json_data)
    name = ''
    file = File()

    return name, file


def _create_file_object_from_post(file_data):
    """Принимает обьект file. Возвращает название файла и объект File"""
    print('FILE_DATA:', file_data, dir(file_data))
    name = file_data.name
    file = File(file_data)

    return name, file




class FileNotFound(Exception): pass


class FileStorage1:
    """Хранит список файлов в заданной директории"""

    def __init__(self, directory=None):
        self.directory = directory if directory else settings['STORAGE_DIRECTORY']
        pass

    def list(self):
        """Выдаёт список файлов."""
        file_names = [f for f in os.listdir(self.directory) if os.path.isfile(f)]
        return [file_names]

    def get_file_content(self, file_name, as_string=True):
        """Возвращает содержимое заданного файла."""
        if not self.check_file_exists(file_name):
            raise FileNotFound

        # Т.к. неизвестно - бинарный файл, или текстовый, просто считываем в бинарном формате и отдаём
        content = b''
        with open(file_name, 'b') as fp:
            content = fp.read()

        return content

    def get_file_url(self, file_name):
        """Возвращает url файла на сервере."""
        return ''

    def check_file_exists(self, file_name):
        """Проверяет, что файл сущеествует."""

    def save(self, file_object):
        """Сохраняет полученный файл."""

    def del_file(self, file_name):
        """Удаляет файл по заданному имени"""
        return True

