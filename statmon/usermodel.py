import shutil
import json
from pathlib import Path


class UserModel():

    def __init__(self):
        self.parent = Path(__file__).resolve().parent / "config/user_model/"
        self.json = self.parent / "user_model.json"
        self.py_name_key = "user_model"

    def copy_pyfile(self, src: str):
        dst = self.parent / "config/user_model/"
        shutil.copy2(src, dst)

    def set_config(self):
        pass

    def read_pyfile(self) -> str:
        if self.json.exists():
            with open(str(self.json), "r") as f:
                j = json.load(f)
            self.py_name = j[self.py_name_key]
            self.py_file = self.parent / self.py_name
            return str(self.py_file)
        return None

