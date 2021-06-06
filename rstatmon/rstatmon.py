#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
import json
import argparse
import signal
import psutil
import shutil
from multiprocessing import Process
from flask_login import LoginManager
from pathlib import Path

from database import User, db, DBInit
from statdata import routine
from mylogger import MyLogger
from usermodel import UserModel
from application import app
import routes


login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def signal_handler(*args):
    for p in (child_id, parent_pid):
        proc = psutil.Process(p)
        proc.terminate()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-d',
        '--debug',
        help="debug",
        action='store_true'
    )
    parser.add_argument(
        '-c',
        '--create',
        help="create",
        action='store_true'
    )
    parser.add_argument(
        '-n',
        '--new',
        type=str,
        help='python'
    )
    parser.add_argument(
        '-p',
        '--password',
        type=str,
        help="password",
    )

    args = parser.parse_args()
    if args.new:
        model = UserModel()
        model.register_file(args.new)
        print("register :", args.new)
        parser.exit()

    if args.create:
        try:
            js = Path(__file__).resolve().parent / "config/database.json"
            d = DBInit()
            d.read_json(js)
            d.db_setup()
        except:
            print(
                "\033[31mFailed to create the database.\033[0m",
                file=sys.stderr)
        finally:
            parser.exit()

    signal.signal(signal.SIGINT, signal_handler)
    p = Process(target=routine, args=(args.debug,))
    p.start()
    parent_pid = os.getpid()
    child_id = p.pid

    if args.debug:
        app.config["TEST"] = True
        app.run(debug=True, threaded=True)
    else:
        app.run(debug=False, threaded=True, host="0.0.0.0")
