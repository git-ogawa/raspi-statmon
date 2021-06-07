#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import json
import sys
from pathlib import Path

from usermodel import UserModel


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-p',
        '--password',
        type=str,
        help='password'
    )
    parser.add_argument(
        '--port',
        type=str,
        default="3306",
        help='port'
    )
    parser.add_argument(
        "-s",
        '--server',
        type=str,
        default="localhost",
        help='server name'
    )
    parser.add_argument(
        '-u',
        '--user',
        type=str,
        default="root",
        help='user name'
    )
    parser.add_argument(
        '-r',
        '--register',
        help="Register user account to json",
        action='store_true'
    )
    args = parser.parse_args()

    if args.register:
        if args.user and args.password:
            data = {
                "username": args.user,
                "password": args.password,
                "server": args.server,
                "port": args.port,
                "db_name": "raspi"
            }
            j = Path(__file__).resolve().parent / "config/database.json"
            with open(str(j), mode='wt', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
            print("register success")
            print("create :", j)
        else:
            print(
                "\033[31mUsername or password is empty.\033[0m",
                file=sys.stderr)
        parser.exit()
