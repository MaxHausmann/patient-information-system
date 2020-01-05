from abc import ABC
import time

class AbstractModel(ABC):
    
    GENDER_M = "m"
    GENDER_D = "d"

    def __init__(self, db_connection):
        self.db = db_connection

    @staticmethod
    def time_now():
        return time.strftime('%Y-%m-%d %H:%M:%S')

    def _attach_to_attributes(self, cursor, exception):
        dataset = cursor.fetchone()
        if dataset is None:
            raise exception
        for idx, column in enumerate(cursor.description):
            setattr(self, column[0], dataset[idx])
