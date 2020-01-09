from abc import ABC
import time
from error import NotFoundException, PatientConnectionFailedException, UserConnectionFailedException, TableNotImplementedException

"""
Abstract classes for implementation in database-model classes
"""

class AbstractModel(ABC):
    """
    Basic functionality for database models
    """

    not_found_exception = NotFoundException
    table_name = None

    def __init__(self, db_connection):
        self.db = db_connection
        self.id = None
        if self.table_name is None:
            raise TableNotImplementedException

    def _attach_to_attributes(self, cursor):
        dataset = cursor.fetchone()
        if dataset is None:
            raise self.not_found_exception
        for idx, column in enumerate(cursor.description):
            setattr(self, column[0], dataset[idx])

    def _get(self, field, value, return_cursor=False):
        cursor = self.db.select_all(self.table_name, "WHERE " + str(field) +"=?", [value])
        if not cursor:
            raise self.not_found_exception
        if return_cursor:
            return cursor
        self._attach_to_attributes(cursor)

    def _get_last(self, field, value):
        field = str(field)
        cursor = self.db.select_all(self.table_name, "WHERE " + field +"=? ORDER BY id DESC LIMIT 1", [value])
        if not cursor:
            raise self.not_found_exception
        self._attach_to_attributes(cursor)

    def _get_many(self, field, value):
        cursor = self._get(field, value, True)
        dataset = cursor.fetchall()
        return (cursor.description, dataset)

    def get_by_id(self, xid):
        self._get(self.table_name + ".id", xid)
        return self

    def delete(self):
        self.db.delete(self.table_name, "WHERE " + self.table_name + ".id=?", [self.id])

    def exist(self, field, value):
        return self.db.exist(self.table_name, "WHERE " + self.table_name + "." + str(field) + "=?", [value])
        
    @staticmethod
    def time_now():
        return time.strftime('%Y-%m-%d %H:%M:%S')