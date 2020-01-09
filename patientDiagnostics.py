from abstractPatientHelperModel import AbstractPatientHelperModel
from error import PatientDiagnosticsIncomplete

class PatientDiagnostics(AbstractPatientHelperModel):

    """helper model class for diagnostics."""

    table_name = "pat_diagnostics"

    def add(self, diagnostics):
        if not len(diagnostics) > 0:
            raise PatientDiagnosticsIncomplete
        self.db.insert(self.table_name, "pat_id, user_id, diagnostics, created", (self.patient.id, self.user.id, diagnostics, self.time_now()))

    def get_all(self):
        return self._get_many("pat_id", self.patient.id)