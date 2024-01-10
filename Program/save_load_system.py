import pickle
import os


class SaveLoadSystem:
    def __init__(self, file_extension, save_folder):
        self.file_extension = file_extension
        self.save_folder = save_folder

    def save_data(self, data, name):
        data_file_path = os.path.join(self.save_folder, name + self.file_extension)
        try:
            with open(data_file_path, "wb") as data_file:
                pickle.dump(data, data_file)
        except Exception as e:
            print(f"Error saving data to {data_file_path}: {e}")

    def load_data(self, name, default=None):
        data_file_path = os.path.join(self.save_folder, name + self.file_extension)
        try:
            if os.path.exists(data_file_path):
                with open(data_file_path, "rb") as data_file:
                    return pickle.load(data_file)
            else:
                return default if default is not None else []
        except Exception as e:
            print(f"Error loading data from {data_file_path}: {e}")
            return default if default is not None else []

    def check_for_files(self, name):
        return os.path.exists(os.path.join(self.save_folder, name + self.file_extension))
