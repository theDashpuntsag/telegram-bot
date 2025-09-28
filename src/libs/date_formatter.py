from datetime import datetime, timezone


class DateFormatter:
    _instance = None;

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DateFormatter, cls).__new__(cls);
        return cls._instance;

    @staticmethod
    def get_formatted_current_datetime() -> str:
        """
        Returns the current date and time formatted as YYYYMMDDHHMM.
        """
        now = datetime.now(timezone.utc)
        return now.strftime("%Y%m%d%H%M");