import shutil
import json
import subprocess
from pathlib import Path
from jinja2 import Template


class UserModel():

    def __init__(self):
        self.parent = Path(__file__).resolve().parent
        self.dst = self.parent / "config/user_model/"
        self.json = self.dst / "user_model.json"
        self.pyname_key = "user_model"

    def register_file(self, src: str):
        src_abs = Path(src).resolve()
        shutil.copy(src_abs, self.dst)
        self.update(src)

    def update(self, src: str):
        data = {self.pyname_key: src}
        with open(str(self.json), "w") as f:
            json.dump(data, f, indent=4)

    def get_value(self):
        f = self.get_filename()
        return self.execute(f)

    def get_filename(self) -> str:
        if self.json.exists():
            with open(str(self.json), "r") as f:
                j = json.load(f)
            self.py_name = j[self.pyname_key]
            self.py_file = self.parent / self.py_name
            return str(self.py_file)
        return None

    def execute(self, pyfile: str):
        cmd = f"python {pyfile}"
        ret = subprocess.check_output(cmd.split()).decode("utf-8").strip("\n")
        return ret


class JinjaTemplate():

    def __init__(self, data: dict):
        self.data = data
        self.parent = Path(__file__).resolve().parent
        self.model_prop = self.parent / "config/user_model/model_prop.json"
        self.body = self.parent / "templates/jinja/body.html"
        self.dst = self.parent / "templates/user_model.html"
        self.org = self.parent / "templates/user_model.html.org"

    def parse_dict(self):
        dct = {}
        colors = ["red", "blue", "yello", "green"]
        it = iter(colors)
        for key, value in self.data.items():
            key_words = key.split("_")
            if len(key_words) == 1 and not key_words[0] == "datasets":
                dct[key_words[0]] = self.parse_int(value)
            elif len(key_words) == 2:
                if not key_words[0] in dct.keys():
                    dct[key_words[0]] = {}
                dct[key_words[0]][key_words[1]] = self.parse_int(value)
                if key_words[0] == "datasets":
                    print("yes")
                    dct[key_words[0]]["color"] = next(it)
            else:
                pass
        if "add" in dct.keys():
            dct.pop("add")
        self.json_data = dct
        with open(str(self.model_prop), "w") as f:
            json.dump(self.json_data, f, indent=4)

    def parse_int(self, data):
        try:
            return int(data)
        except ValueError:
            return data

    def load_body(self):
        with open(str(self.body), "r") as f:
            s = f.read()
        print(s)
        temp = Template(s)
        body = {"body": temp.render(self.json_data)}
        return body

    def load_template(self, body: dict):
        tmp = """
        {%- raw %}
        {% extends "layout.html" %}
        {% block content %}
        {%- endraw %}
        {{ body }}
        {%- raw %}
        {% endblock %}
        {%- endraw %}
        """
        temp = Template(tmp)
        html = temp.render(body)
        return html

    def make_template(self):
        self.parse_dict()
        body = self.load_body()
        html = self.load_template(body)
        self.writer(html)

    def writer(self, data: str):
        with open(str(self.dst), "w") as f:
            f.write(data)

    def remove_model(self):
        shutil.copy(self.org, self.dst)

if __name__ == "__main__":
    pass
    #j = JinjaTemplate()
