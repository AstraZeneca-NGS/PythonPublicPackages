import unittest
from mock import Mock, patch
from dataclasses import dataclass

from claas.claas.src.config import Configurable


def setUpModule():
    global file
    global file_content
    global filename

    file = Mock()
    file_content = {"cBio": {"Dcode": "Dxxxxx", "study": "Acronym_D-code"}}
    filename = "test_yaml_file"


class TestConfig(unittest.TestCase):

    @patch.object(Configurable, "_load_yaml", lambda x: file_content)
    def test_section_to_init(self):
        class ConfigInherited(Configurable):
            def __init__(self, file_name, section):
                self.Dcode = None
                self.study = None
                super().__init__(file_name, section)
        test_configurable = ConfigInherited(filename, "cBio")
        test_content = {"Dcode": "Dxxxxx", "study": "Acronym_D-code"}
        assert(test_content.items() <= test_configurable.__dict__.items())

    @patch.object(Configurable, "_load_yaml", lambda x: file_content)
    def test_with_dataclasses(self):
        @dataclass
        class ConfigureTest(Configurable):
            # required arguments for Configurable
            filename: str
            section: str
            Dcode: str = None
            study: str = None

            def __post_init__(self):
                super().__init__(self.filename, self.section)

        test_configurable = ConfigureTest(filename, "cBio")
        test_content = {"Dcode": "Dxxxxx", "study": "Acronym_D-code"}
        assert (test_content.items() <= test_configurable.__dict__.items())

    @patch.object(Configurable, "_load_yaml", lambda x: file_content)
    def test_configure_mock_load_yaml(self):
        class ConfigInherited(Configurable):
            def __init__(self, file_name, section):
                self.Dcode = None
                self.study = None
                super().__init__(file_name, section)
        test_configurable = ConfigInherited(filename, "cBio")
        test_content = {"Dcode": "Dxxxxx", "study": "Acronym_D-code"}
        assert(test_content.items() <= test_configurable.__dict__.items())
        self.assertEqual(test_configurable.study, "Acronym_D-code")

    @patch.object(Configurable, "__init__", lambda x, y, z: None)
    def test_configure_no_sections(self):
        test_configurable = Configurable(file, None)
        test_configurable.filename = filename
        test_configurable.Dcode = None
        test_configurable.study = None
        test_configurable.cBio = None
        test_configurable.yaml_dict = file_content
        test_configurable._configure(section=None)
        test_content = {"Dcode": "Dxxxxx", "study": "Acronym_D-code"}
        self.assertEqual(test_configurable.cBio, test_content)

    @patch.object(Configurable, "__init__", lambda x, y, z: None)
    def test_set_dict_no_key(self):
        test_configurable = Configurable(file, None)
        test_configurable.filename = filename
        test_configurable.Dcode = None
        test_configurable.study = None
        test_configurable.yaml_dict = {"cBio": {"Dcode": "Dxxxxx", "study": "Acronym_D-code", "contact": "email"}}
        self.assertRaises(KeyError, test_configurable._set_dict, test_configurable.yaml_dict["cBio"])

    @patch.object(Configurable, "__init__", lambda x, y, z: None)
    def test_config_ok(self):
        test_configurable = Configurable(file, None)
        test_configurable.filename = filename
        test_configurable.Dcode = None
        test_configurable.study = None
        test_configurable.yaml_dict = file_content
        test_configurable._configure(section="cBio")
        test_dict = {"Dcode": "Dxxxxx", "study": "Acronym_D-code"}
        assert(test_dict.items() <= test_configurable.__dict__.items())
        
    @patch.object(Configurable, "__init__", lambda x, y, z: None)
    def test_config_list(self):
        test_configurable = Configurable(file, None)
        test_configurable.filename = filename
        test_configurable.Dcode = None
        test_configurable.study = None
        test_configurable.data_owner = None
        test_configurable.yaml_dict = {"cBio": {"Dcode": "Dxxxxx", "study": "Acronym_D-code"},
                                       "Common": {"data_owner": "test_name"}}
        test_configurable._configure(section=["cBio", "Common"])
        test_dict = {"Dcode": "Dxxxxx", "study": "Acronym_D-code", "data_owner": "test_name"}
        assert(test_dict.items() <= test_configurable.__dict__.items())

    @patch.object(Configurable, "__init__", lambda x, y, z: None)
    def test_duplicated_keys(self):
        test_configurable = Configurable(file, None)
        test_configurable.filename = filename
        test_configurable.Dcode = None
        test_configurable.study = None
        test_configurable.data_owner = None
        test_configurable.yaml_dict = {"cBio": {"Dcode": "Dxxxxx", "study": "Acronym_D-code"},
                                       "Common": {"Dcode": "test_name"}}
        self.assertRaises(ValueError, test_configurable._configure, ["cBio", "Common"])

    @patch.object(Configurable, "__init__", lambda x, y, z: None)
    def test_missing_section(self):
        test_configurable = Configurable(file, None)
        test_configurable.filename = filename
        test_configurable.Dcode = None
        test_configurable.study = None
        test_configurable.cBio = None
        test_configurable.yaml_dict = file_content
        test_configurable._configure(section="Common")
        configurable_keys = [test_configurable.Dcode, test_configurable.study, test_configurable.cBio]
        self.assertEqual(all(key is None for key in configurable_keys), True)

    @patch.object(Configurable, "__init__", lambda x, y, z: None)
    def test_empty_section(self):
        test_configurable = Configurable(file, None)
        test_configurable.filename = filename
        test_configurable.Dcode = None
        test_configurable.study = None
        test_configurable.cBio = None
        test_configurable.yaml_dict = {"cBio": {"Dcode": "Dxxxxx", "study": "Acronym_D-code"},
                                       "Common": None}
        test_configurable._configure(section="Common")
        configurable_keys = [test_configurable.Dcode, test_configurable.study, test_configurable.cBio]
        self.assertEqual(all(key is None for key in configurable_keys), True)


if "__name__" == "__main__":
    testsuite = unittest.TestLoader().discover(pattern="test_*.py", start_dir="")
    unittest.TestRunner().run(testsuite)
