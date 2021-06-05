import json
from pathlib import Path
from flask import Flask
from database import init_db
from passhash import init_bcrypt


def create_app():
    j = Path(__file__).resolve().parent / "config/database.json"
    with open(j, "r") as f:
        json_data = json.load(f)
    username = json_data["username"]
    password = json_data["password"]
    server = json_data["server"]
    db_name = json_data["db_name"]
    db_url = f"mysql+pymysql://{username}:{password}@{server}/{db_name}?charset=utf8"

    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'cfb33786023cc152019e747a051f73c6'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
    app.config["TEST"] = False
    init_db(app)
    init_bcrypt(app)
    return app


app = create_app()
