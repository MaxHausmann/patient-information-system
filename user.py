from abstractPersonModel import AbstractPersonModel
from security import get_hashed_password, check_password
from error import UserNotFoundException

"""
User model for all users of this software and its helpers
"""

class User(AbstractPersonModel):

    STATUS_MD = "medical_doctor"
    STATUS_N = "nurse"
    STATUS_A = "admin"

    table_name = "users"
    not_found_exception = UserNotFoundException
    #table_fields = ["id", "username", "password", "email", "surname", "firstname", "gender", "status"]

    def __init__(self, db, username=None, password=None, email=None, surname=None, firstname=None, gender=None, status=None):
        super().__init__(db)
        self.username = username
        self.password = password
        self.email = email
        self.surname = surname
        self.firstname = firstname
        self.gender = gender
        self.status = status
        self.pw_is_hashed = False
     
    def save(self):
        if self.gender != self.GENDER_M and self.gender != self.GENDER_F:
            print("Setting gender to male.")
            self.gender = self.GENDER_M
        if self.status != self.STATUS_MD and self.status != self.STATUS_N and self.status != self.STATUS_A:
            print("Setting status to nurse.")
            self.status = self.STATUS_N
        if not self.pw_is_hashed:
            self.password = self._encrypt_password(self.password)
        if not self.exist(self.username):
            return self._insert()
        return self._update()

    def get_by_username(self, username):
        self._get(self.table_name + ".username", username)
        self.pw_is_hashed = True # password from db is already hashed
        return self

    def get_by_id(self, uid):
        super().get_by_id(uid)
        self.pw_is_hashed = True # password from db is already hashed
        return self

    def exist(self, username):
        return super().exist("username", username)

    def _encrypt_password(self, password):
        return get_hashed_password(password)

    def check_password(self, password):
        return check_password(password, self.password)

    def _insert(self):
        self.id = self.db.insert(self.table_name, "username, password, email, surname, firstname, gender, status, created", 
                                (self.username, self.password, self.email, self.surname, self.firstname, self.gender, self.status, self.time_now()))

    def _update(self):
        return self.db.update(self.table_name, "username, password, email, surname, firstname, gender, status", "WHERE users.id=?",
                             (self.username, self.password, self.email, self.surname, self.firstname, self.gender, self.status, self.id))
