import pytest
from adventure.dao.doc_yaml import get_yaml_doc
from adventure.exceptions import EmptyFileError, BadYamlError

class TestGetYamlDoc:
    """Test Class for yaml doc operations."""
    fname: str

    @pytest.fixture(autouse=True)
    def valid_yaml_doc(self, tmp_path):
        """Create a valid yaml doc for testing."""
        self.fname = tmp_path / "valid.yaml"
        with open(self.fname, "w", encoding="utf-8") as fh:
            fh.write("key: value\n")
        yield
        self.fname.unlink(missing_ok=True)

    def test_get_yaml_doc_ok(self):
        """Test that a valid yaml doc is read correctly."""
        doc = get_yaml_doc(str(self.fname))
        assert isinstance(doc, dict)
        assert doc.get("key") == "value"

    def test_get_yaml_doc_empty_file(self, tmp_path):
        """Test that an empty yaml doc raises EmptyFileError."""
        fname = tmp_path / "empty.yaml"
        with open(fname, "w", encoding="utf-8") as fh:
            fh.write("")
        with pytest.raises(EmptyFileError):
            get_yaml_doc(str(fname))
        fname.unlink(missing_ok=True)

    def test_get_yaml_doc_file_not_found(self):
        """Test that a non-existent file raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            get_yaml_doc("non_existent_file.yaml")

    def test_get_yaml_doc_not_yaml(self, tmp_path):
        """Test that a non-yaml file raises an error."""
        fname = tmp_path / "not_yaml.txt"
        with open(fname, "w", encoding="utf-8") as fh:
            fh.write("This is not yaml content")
        with pytest.raises(BadYamlError):
            get_yaml_doc(str(fname))
        fname.unlink(missing_ok=True)