from database import Database
from user import User
from patient import Patient
from patientStatus import PatientStatus
from patientDiagnostics import PatientDiagnostics

"""
Scratch file for all drytests, because Unit-Tests are to expensive ;)
"""

db = Database("database/database.sqlite3")
#usr = 
#usr = User(db, username="MaxHausmann3", password="123", email="sma.x@web.de", surname="Hausmann", firstname="Maximilian", gender=User.GENDER_M, status=User.STATUS_MD)
#usr.save()
#print(usr)
#user = User(db).get_by_username("MaxHausmann3")
#print(user)
#user.surname = "Balbalba234"
#user.save()
#user.delete()
#print(user)

#pat = Patient(db, surname="Hausmann", firstname="Maximilian", birthday="08.03.1995")
#pat.save()
#pat = Patient(db).get_by_id(1)
#print(pat.surname)

#pat_status = PatientStatus(db, pat, user)
#pat_status.add(PatientStatus.STATUS_DEAD, "em")
#pat_status.get_current()
#print(PatientStatus.department_decode(pat_status.department))

#pat_diag = PatientDiagnostics(db, pat, user)
#test = pat_diag.get_all()
#for val in test[1]:
#    print(val[3])
db.execute("DELETE FROM patients WHERE id=15")