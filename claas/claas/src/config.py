import os
from typing import Union
import yaml


class Configurable:
    """
    Read a YAML and configure "self" based on YAML and section
    """

    def __init__(self, filename: str, section: Union[str, list] = None):
        self.filename = os.path.expanduser(filename)
        self.yaml_dict = self._load_yaml()
        self._configure(section)

    def get_parameters(self, section: Union[str, list]) -> dict:
        """ Get "section" parameters dictionary """
        section_value = self.yaml_dict.get(section)
        if section_value is not None:
            return section_value
        return dict()

    def _load_yaml(self) -> dict:
        """
        Load yaml file into dictionary
        """
        try:
            with open(self.filename, "r") as config_file:
                config = yaml.load(config_file, Loader=yaml.FullLoader)
        except FileNotFoundError as e:
            raise ValueError(f"Exception while opening config file: {e}") from e
        return config

    def __getitem__(self, section: Union[str, list]) -> dict:
        return self.get_parameters(section)

    def _set_dict(self, dict_to_parse: dict):
        """"
        Parse dictionary into self.__dict__
        """
        for k, v in dict_to_parse.items():
            if k in self.__dict__:
                self.__dict__[k] = v
            else:
                raise KeyError(f"Class_name: {self.__class__.__name__}, filename: {self.filename}, No {k} in "
                               f"configure parameters.")

    def _configure(self, section: Union[str, list] = None):
        """
        Configure "self" using "section" from YAML file
        Section can be either "string" or "list"
        The test of presence of key in the default parameters is also performed
        """
        if not section:
            if self.yaml_dict:
                self._set_dict(self.yaml_dict)
        elif type(section) == str:
            dict_to_parse = self.get_parameters(section)
            self._set_dict(dict_to_parse)
        elif type(section) == list:
            temp_dict = {}
            for section_item in section:
                new_dict = self.get_parameters(section_item)
                intersection = temp_dict.keys() & new_dict.keys()
                if intersection:
                    raise ValueError(f"Key(s) {intersection} are not unique")
                temp_dict.update(new_dict)
                self._set_dict(new_dict)
        else:
            raise ValueError(f"Unexpected config section type {section}: {type(section)}")
