from abstractPersonModel import AbstractPersonModel
from security import get_hashed_password
from error import PatientNotFoundException

"""
Model-classes for patients and its helpers
"""

class Patient(AbstractPersonModel):

    """Model for patients and their behaviours"""

    table_name = "patients"
    
    def __init__(self, db, surname=None, firstname=None, birthday=None, gender=None, phone=None):
        super().__init__(db)
        self.surname = surname
        self.firstname = firstname
        self.birthday = birthday
        self.gender = gender
        self.phone = phone
        
    def save(self):
        if self.gender is None:
            print("set gender to male")
            self.gender = self.GENDER_M
        if self.phone is None:
            print("set phone to zero")
            self.phone = "+49 0000"
        if not self.exist(self.id):
            return self._insert()
        return self._update()

    def delete(self):
        self.db.delete("WHERE " + self.table_name + ".id=?", [self.id])

    def exist(self, pid):
        return self.db.exist("WHERE " + self.table_name + ".id=?", [pid])

    def _insert(self):
        self.id = self.db.insert("surname, firstname, gender, phone, birthday, created", 
                                (self.surname, self.firstname, self.gender, self.phone, self.birthday, self.time_now()))

    def _update(self):
        return self.db.update("surname, firstname, gender, phone, birthday", "WHERE users.id=?",
                                (self.surname, self.firstname, self.gender, self.phone, self.birthday))

