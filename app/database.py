import configparser
from pathlib import Path
from collections import namedtuple
from typing import List, NamedTuple
from datetime import date, datetime

import sqlite3

DEFAULT_DATE_FORMAT = '%d-%m-%Y'
DEFAULT_DB_FILE_PATH = Path.joinpath(Path.cwd(), "_mypytimer", "worksessions.db")
DEFAULT_SCHEMA_FILE_PATH = Path.joinpath(Path.cwd(), "_mypytimer", "schema.sql")

class WorkSession(NamedTuple):
    start_time: float
    stop_time: float

class WorkSessionInfo(NamedTuple):
    id: int
    date: str
    start_time: float
    stop_time: float

class DailyWorkHours(NamedTuple):
    date: str
    hours: float

def get_schema_path(config_file: Path) -> Path:
    """Return the current path to the mypytimer schema."""
    config_parser = configparser.ConfigParser()
    config_parser.read(config_file)
    return Path(config_parser["General"]["schema"])

def get_database_path(config_file: Path) -> Path:
    """Return the current path to the mypytimer database."""
    config_parser = configparser.ConfigParser()
    config_parser.read(config_file)
    return Path(config_parser["General"]["database"])

def init_database(schema_path: Path, db_path: Path):
    """Create the mypytimer database."""
    connection = sqlite3.connect(db_path)
    with open(schema_path, 'r') as f:
        connection.executescript(f.read())
    connection.commit()
    connection.close()

class DatabaseHandler:
    def __init__(self, db_path: Path) -> None:
        self._db_path = db_path

    def get_time_spent_on_work_for_today(self) -> List[WorkSession]:
        connection = sqlite3.connect(self._db_path)
        cursor = connection.cursor()
        work_sessions = cursor.execute('SELECT start_time, stop_time FROM worksessions where date=?;', (date.today().strftime(DEFAULT_DATE_FORMAT),)).fetchall()
        work_sessions = [WorkSession(start_time=start, stop_time=stop) for start, stop in work_sessions]
        connection.close()
        return work_sessions
    
    def get_current_work_session(self) -> WorkSessionInfo:
        connection = sqlite3.connect(self._db_path)
        cursor = connection.cursor()
        latest_work_session = cursor.execute('SELECT * FROM worksessions where date=? order by start_time desc limit 1;', (date.today().strftime(DEFAULT_DATE_FORMAT),)).fetchone()
        if latest_work_session:
            latest_work_session = WorkSessionInfo(*latest_work_session)
        # if latest_work_session.stop_time:
        #     None
        # else:
        # connection.close()
        return latest_work_session

    def create_work_session(self):
        connection = sqlite3.connect(self._db_path)
        cursor = connection.cursor()
        cursor.execute('INSERT INTO worksessions(date, start_time) values(?, ?);', (date.today().strftime(DEFAULT_DATE_FORMAT), datetime.now().timestamp()))
        connection.commit()
        connection.close()

    def end_work_session(self, id):
        connection = sqlite3.connect(self._db_path)
        cursor = connection.cursor()
        # result = cursor.execute('SELECT id, stop_time FROM worksessions where date=? order by start_time desc limit 1;', (date.today().strftime(DEFAULT_DATE_FORMAT),)).fetchOne()
        # if result[1]:
            # return DBResponse(work_sessions=None, error="No session was in progress")
        # else:
        cursor.execute('UPDATE worksessions SET stop_time=? where id=?;', (datetime.now().timestamp(), id))
        connection.commit()
        connection.close()

    def get_daily_time_spent_on_work(self) -> List[DailyWorkHours]:
        connection = sqlite3.connect(self._db_path)
        cursor = connection.cursor()
        results = cursor.execute('SELECT date, ROUND(SUM(stop_time-start_time)*1.0/3600, 2) FROM worksessions where stop_time is not null GROUP BY date;').fetchall()
        daily_workhours_list = [DailyWorkHours(*daily_workhours) for daily_workhours in results]
        connection.close()
        return daily_workhours_list