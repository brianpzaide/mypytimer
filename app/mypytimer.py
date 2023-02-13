from pathlib import Path
from typing import Any, Dict, List

from app import SUCCESS, CREATE_SESSION_ERROR, STOP_SESSION_ERROR
from app.database import DatabaseHandler, DailyWorkHours

class MyPyTimer:
    def __init__(self, db_path: Path) -> None:
        self._db_handler = DatabaseHandler(db_path)
    
    def start(self) -> int:
        """Start a new session."""
        current_session = self._db_handler.get_current_work_session()
        # for the first time use
        if current_session is None:
            self._db_handler.create_work_session()
            return SUCCESS

        if current_session.stop_time is None:
            return CREATE_SESSION_ERROR
        else:
            self._db_handler.create_work_session()
            return SUCCESS
    
    def stop(self) -> int:
        """End current session."""
        current_session = self._db_handler.get_current_work_session()
        # for the first time use
        if current_session is None:
            return STOP_SESSION_ERROR

        if current_session.stop_time:
            return STOP_SESSION_ERROR
        else:
            self._db_handler.end_work_session(current_session.id)
            return SUCCESS
    
    def hours_put_in_today(self) -> str:
        """Get number of hours put in today."""
        worksessions_for_today = self._db_handler.get_time_spent_on_work_for_today()
        hours_put_in_today = 0.0
        for ws in worksessions_for_today:
            hours_put_in_today += (ws.stop_time - ws.start_time)/3600
        return f"Today you worked for {hours_put_in_today} hrs"
        
    
    def hours_put_in_daily(self) -> List[DailyWorkHours]:
        """Get number of hours put in everyday."""
        return self._db_handler.get_daily_time_spent_on_work()