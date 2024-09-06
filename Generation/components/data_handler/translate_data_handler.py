import os
import logging

logger = logging.getLogger(__name__)

from .config_reader import ConfigReader


def sanitize_model_name(model_name: str):
    model_name = model_name.split("/")[0]
    model_name = model_name.replace(".", "_").replace("-", "_")
    return model_name


class TranslationDataHandler:
    def __init__(self, config):
        self.config_reader = ConfigReader(config)

    def get_attribute(self, attribute):
        return self.config[attribute]

    def __create_valid_data_points(self):
        pass

    def return_data_point(self, total=-1):
        valid_data_points = self.__create_valid_data_points()

        for i, data_point in enumerate(valid_data_points):
            yield data_point
            if i == total - 1:
                break

    def save_data_point(self, index: int, content: dict):

        # Get the model name and storage folder path from the config reader
        model_name = self.config_reader.get_attribute("model")
        storage_folder_path = self.config_reader.get_attribute("storage_folder_path")

        # Sanitize the model name
        sanitized_model_name = sanitize_model_name(model_name)

        # Create the storage folder if it doesn't exist
        if not os.path.exists(storage_folder_path):
            os.makedirs(storage_folder_path)

        # Create the model folder if it doesn't exist
        model_folder_path = os.path.join(storage_folder_path, sanitized_model_name)
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)

        # Create the index folder
        index_folder_path = os.path.join(model_folder_path, str(index))
        if not os.path.exists(index_folder_path):
            os.makedirs(index_folder_path)

        # Write the content to the files
        for key, value in content.items():
            filepath = os.path.join(index_folder_path, f"{key}.txt")
            try:
                with open(filepath, "w", encoding="utf-8") as file:
                    file.write(str(value))
                    logger.info(f"Content saved to file: {filepath}\n")
            except Exception as e:
                logger.error(f"Error occurred while writing to file: {e}\n")
                pass  # Skip the operation if an error occurs
