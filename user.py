from abstractModel import AbstractModel
from security import get_hashed_password
from error import *

class User(AbstractModel):

    STATUS_MD = "medical_doctor"
    STATUS_N = "nurse"
    STATUS_A = "admin"

    def __init__(self, db, username=None, password=None, email=None, surname=None, firstname=None, gender=None, status=None):
        super().__init__(db)
        self.id = None
        self.username = username
        self.password = password
        self.email = email
        self.surname = surname
        self.firstname = firstname
        self.gender = gender
        self.status = status
        self.pw_is_hashed = False
     
    def save(self):
        if self.gender != self.GENDER_M and self.gender != self.GENDER_D:
            print("Setting gender to male.")
            self.gender = self.GENDER_M
        if self.status != self.STATUS_MD and self.status != self.STATUS_N and self.status != self.STATUS_A:
            print("Setting status to nurse.")
            self.status = self.STATUS_N
        if not self.pw_is_hashed:
            self.update_password(self.password)
        if not self.exist(self.username):
            return self._insert()
        return self._update()

    def _insert(self):
        self.id = self.db.insert("users", "username, password, email, surname, firstname, gender, status, created", 
                                (self.username, self.password, self.email, self.surname, self.firstname, self.gender, self.status, self.time_now()))

    def _update(self):
        return self.db.update(  "users", "username, password, email, surname, firstname, gender, status", "WHERE users.id=?",
                                (self.username, self.password, self.email, self.surname, self.firstname, self.gender, self.status, self.id))

    def exist(self, username):
        return self.db.exist("users", "WHERE users.username = ?", [username])

    def _get(self, field, value):
        cursor = self.db.select_all("users", "WHERE " + str(field) +" = ?", [value])
        if not cursor:
            raise UserNotFoundException
        self._attach_to_attributes(cursor, UserNotFoundException)
        self.pw_is_hashed = True # password from db is already hashed

    def get_by_name(self, username):
        self._get("users.username", username)
        return self

    def get_by_id(self, uid):
        self._get("users.id", uid)
        return self

    def update_password(self, password):
        self.password = get_hashed_password(password)
        


