from abstractModel import AbstractModel
from user import User
from patient import Patient
from error import PatientConnectionFailedException, UserConnectionFailedException

class AbstractPatientHelperModel(AbstractModel):
    """
    Basic functionality for all patient helper classes which interact with 
    patient-models
    """

    def __init__(self, db, patient_object, user_object):
        super().__init__(db)
        self.patient = None
        self.user = None
        
        self.check_and_attach(patient_object, should_be=Patient, self_attribute="patient", exception=PatientConnectionFailedException)
        self.check_and_attach(user_object, should_be=User, self_attribute="user", exception=UserConnectionFailedException)
        
    def check_and_attach(self, obj_to_check=None, should_be=None, self_attribute=None, exception=None):
        """checks object and connects it to helper"""
        if not isinstance(obj_to_check, should_be):
            raise exception
        if obj_to_check.id is None:
            raise exception
        setattr(self, self_attribute, obj_to_check)

