#!/usr/bin/env python3
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
from app import app
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
        '-p',
        '--password',
        type=str,
        help='port'
    )
    parser.add_argument(
        '-u',
        '--user',
        type=str,
        default="root",
        help='user'
    )
    parser.add_argument(
        '-r',
        '--register',
        help="Register",
        action='store_true'
    )
    parser.add_argument(
        '--py',
        type=str,
        help='python'
    )


    args = parser.parse_args()

    if args.py:
        pass

    if args.register:
        if args.user and args.password:
            data = {
                "username": args.user,
                "password": args.password,
                "server": "localhost",
                "db_name": "raspi"
            }
            j = Path(__file__).resolve().parent / "config/database.json"
            with open(str(j), mode='wt', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        else:
            print(
                "\033[31mUsername or password is empty.\033[0m",
                file=sys.stderr)
        parser.exit()

    if args.create:
        try:
            if not args.password:
                print("Input the password :", end="")
                args.password = input().strip()
            DBInit(args.user, args.password).db_setup()
        except:
            print(
                "\033[31mFailed to create the database. Check the password.\033[0m",
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
