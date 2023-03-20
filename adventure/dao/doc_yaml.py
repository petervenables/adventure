from typing import Dict
import yaml


def get_yaml_doc(fname: str) -> Dict:
    """Read in a yaml doc and return a dictionary of the contents.
    
    Arguments:
        fname(str):     Name of the YAML document to read in.

    Returns:
        (Dict):         The dictionary found in the doc

    Raises:
        (FileNotFoundError): if the named file cannot be found.
        (EmptyFileError):    if the named file does not contain any content.
    """
    doc: Dict = {}
    try:
        stream = open(fname, 'r', encoding='UTF-8')
        doc = yaml.safe_load(stream)
        stream.close()
        return doc
    except FileNotFoundError as fnfe:
        raise fnfe
