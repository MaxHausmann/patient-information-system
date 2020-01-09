from abstractPatientHelperModel import AbstractPatientHelperModel
from error import PatientStatusInvalid

class PatientStatus(AbstractPatientHelperModel):

    """helper model class for patients' status."""

    table_name = "pat_status"

    STATUS_DEAD = "dead"
    STATUS_DISMISSED = "dismissed"
    STATUS_ACTIVE = "active"
    DEPARTMENTS = {"Intensive Care Unit": "icu", "Emergency": "em", "Neonatology": "neo"}

    def __init__(self, *args):
        self.department = None
        self.status = None
        super().__init__(*args)

    def add(self, status, department):
        if not (status == self.STATUS_ACTIVE or status == self.STATUS_DEAD or status == self.STATUS_DISMISSED):
            raise PatientStatusInvalid
        if len(self.department_decode(department)) == 0:
            raise PatientStatusInvalid
        self.db.insert(self.table_name, "pat_id, user_id, department, status, created", (self.patient.id, self.user.id, department, status, self.time_now()))

    def get_current(self):
        self._get_last(self.table_name, "pat_id", self.patient.id)

    @staticmethod
    def department_decode(department):
        """decodes department abbreviation to full name"""
        return [key for (key, value) in PatientStatus.DEPARTMENTS.items() if value == department]