import os
import logging

logger = logging.getLogger(__name__)

from .config_reader import ConfigReader
from .translate_data_handler import sanitize_model_name


class InferenceDataHandler:
    def __init__(self, config):
        self.config_reader = ConfigReader(config)
        self.__setup_result_configurations()

    def __setup_result_configurations(self):
        # Get the model name and storage folder path from the config reader
        model_name = self.config_reader.get_attribute("model")
        storage_folder_path = self.config_reader.get_attribute("storage_folder_path")
        task = self.config_reader.get_attribute("task")
        language = self.config_reader.get_attribute("language")
        category = self.config_reader.get_attribute("category")

        # Sanitize the model name
        sanitized_model_name = sanitize_model_name(model_name)
        result_folder_name = (
            f"{sanitized_model_name}_{task}_{language}_{category}"
        )

        # Create the storage folder if it doesn't exist
        if not os.path.exists(storage_folder_path):
            os.makedirs(storage_folder_path)

        # Create the model folder if it doesn't exist
        self.model_folder_path = os.path.join(storage_folder_path, result_folder_name)
        if not os.path.exists(self.model_folder_path):
            os.makedirs(self.model_folder_path)

    def get_attribute(self, attribute):
        return self.config_reader.get_attribute(attribute)

    def __is_datapoint_eligible(self, index):
        index_folder_path = os.path.join(self.model_folder_path, str(index))
        return not os.path.exists(index_folder_path)

    def __create_valid_data_points(self) -> dict:
        import pandas as pd

        refined_data_path = self.config_reader.get_attribute("data_path")
        refined_data = pd.read_csv(refined_data_path)

        mask = [self.__is_datapoint_eligible(index) for index in refined_data.index]
        valid_data_points = refined_data[mask].to_dict("records")

        return valid_data_points

    def return_data_point(self, total=-1):
        valid_data_points = self.__create_valid_data_points()

        for i, data_point in enumerate(valid_data_points):
            yield data_point
            if i == total - 1:
                break

    def save_data_point(self, index: int, content: dict):

        # Create the index folder
        index_folder_path = os.path.join(self.model_folder_path, str(index))
        if not os.path.exists(index_folder_path):
            os.makedirs(index_folder_path)

        # Write the content to the files
        for key, value in content.items():
            filepath = os.path.join(index_folder_path, f"{key}.txt")
            try:
                with open(filepath, "w", encoding="utf-8") as file:
                    file.write(str(value))
                    logger.info(f"Content saved to file: {filepath}")
            except Exception as e:
                logger.error(f"Error occurred while writing to file: {e}\n")
                pass  # Skip the operation if an error occurs
