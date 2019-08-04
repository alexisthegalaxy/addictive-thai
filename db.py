import sqlite3
import os


def get_db_cursor():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    return sqlite3.connect(os.path.join(dir_path, 'thai.db')).cursor()


def get_db_conn():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    return sqlite3.connect(os.path.join(dir_path, 'thai.db'))

