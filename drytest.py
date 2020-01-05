from database import Database
from user import User

db = Database("database/database.sqlite3")
#usr = 
#usr = User(db, "MaxHausmann3", "123", "sma.x@web.de", "Hausmann", "Maximilian", User.GENDER_M, User.STATUS_MD)
#usr.save()

user = User(db).get_by_name("MaxHausmann34")
print(user)
user.surname = "Balbalba234"
user.save()
#print(user)