import uuid
import tempfile
from pathlib import Path
import uuid
import os


def create_temp_file(extension):
    tmpdirname = tempfile.mkdtemp()
    temp_dir = Path(tmpdirname)
    uid = str(uuid.uuid4())
    key = f'{uid}.{extension}'
    return temp_dir / key


def cleanup(path):
    os.remove(path)
