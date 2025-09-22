"""adventure/dao/doc_yaml -- functions to read in YAML documents."""

import yaml
from yaml.parser import ParserError
from adventure.exceptions import EmptyFileError, BadYamlError


def get_yaml_doc(fname: str) -> dict:
    """Read in a yaml doc and return a dictionary of the contents.

    Arguments:
        fname(str):     Name of the YAML document to read in.

    Returns:
        (Dict):         The dictionary found in the doc

    Raises:
        (FileNotFoundError): if the named file cannot be found.
        (EmptyFileError):    if the named file does not contain any content.
    """
    doc: dict = {}
    try:
        with open(fname, "r", encoding="utf-8") as fh:
            doc = yaml.safe_load(fh)
        if not doc:
            raise EmptyFileError("Data file {fname} contained no data!")
        if not isinstance(doc, dict) and not isinstance(doc, list):
            raise BadYamlError(f"Data file {fname} did not contain valid YAML data!")
        return doc
    except ParserError as pe:
        raise BadYamlError(f"Data file {fname} could not be parsed: {pe}") from pe
    except FileNotFoundError as fnfe:
        raise fnfe
