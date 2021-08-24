import json
import os

class FileManager:
    def __init__(self, file_path):
        self.file_path = file_path
        
    #Private
    def __get_file_path(self):
        return self.file_path

    def __file_exists(self):
        return os.path.isfile(self.__get_file_path()) and os.path.exists(self.__get_file_path())

    #Public
    def read_file(self):
        if not self.__file_exists():
            print("File not accessible")
            exit(0)

        with open(self.__get_file_path(), 'r') as file:
            text = file.read()
            file.close()
            return text

    def write_to_file(self, text):
        if not self.__file_exists():
            open(self.__get_file_path(), 'w')

        with open(self.__get_file_path(), 'w') as file:
            file.write(text)
            file.close()

class JSONManager:
    def __init__(self, file_manager):
        self.file_manager = file_manager

    #Private
    def __get_file_manager(self):
        return self.file_manager

    #Public
    def get_data(self):
        text = self.__get_file_manager().read_file()
        return json.loads(text)

    def write_data(self, data_dict):
        text = json.dumps(data_dict)
        self.__get_file_manager().write_to_file(text)