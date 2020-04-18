"""app.io.py"""
import json
import pathlib
from typing import Dict, Union

HERE = pathlib.Path(__file__)
DATA = HERE.joinpath("..", "data").resolve()


def save(
    name: str, content: Union[str, Dict], write_mode: str = "w", indent: int = 2, **json_dumps_kwargs
) -> pathlib.Path:
    """Save content to a file. If content is a dictionary, use json.dumps()."""
    path = DATA / name
    if isinstance(content, dict):
        content = json.dumps(content, indent=indent, **json_dumps_kwargs)
    with open(DATA / name, mode=write_mode) as f_out:
        f_out.write(content)
    return path


def load(name: str, **json_kwargs) -> Union[str, Dict]:
    """Loads content from a file. If file ends with '.json', call json.load() and return a Dictionary."""
    path = DATA / name
    with open(path) as f_in:
        if path.suffix == ".json":
            return json.load(f_in, **json_kwargs)
        return f_in.read()
