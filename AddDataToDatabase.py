import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://faceattendancesystem-243a6-default-rtdb.firebaseio.com/"
})


ref = db.reference('Students')

# for graphically interface we have to use pyGame or twinter
data = {
    "321654":
        {
            "name": "Murtaza Hassan",
            "major": "Robotics",
            "starting_year": 2017,
            "total_attendance": 7,
            "standing": "G",
            "year": 4,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "852741":
        {
            "name": "Emly Blunt",
            "major": "Economics",
            "starting_year": 2021,
            "total_attendance": 12,
            "standing": "B",
            "year": 1,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "963852":
        {
            "name": "Elon Musk",
            "major": "Physics",
            "starting_year": 2020,
            "total_attendance": 7,
            "standing": "G",
            "year": 2,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "1":
        {
            "name": "Rashmi",
            "major": "IT",
            "starting_year": 2021,
            "total_attendance": 7,
            "standing": "G",
            "year": 3,
            "last_attendance_time": "2024-04-30 00:54:34"
        },
    "2":
        {
            "name": "Garvit",
            "major": "CSE",
            "starting_year": 2021,
            "total_attendance": 2,
            "standing": "G",
            "year": 3,
            "last_attendance_time": "2024-04-30 00:54:34"
        },
    "3":
        {
            "name": "Rashmi",
            "major": "IT",
            "starting_year": 2021,
            "total_attendance": 7,
            "standing": "G",
            "year": 3,
            "last_attendance_time": "2024-04-30 00:54:34"
        },
    "4":
        {
            "name": "Rashmi",
            "major": "IT",
            "starting_year": 2021,
            "total_attendance": 7,
            "standing": "G",
            "year": 3,
            "last_attendance_time": "2024-04-30 00:54:34"
        },
    "5":
        {
            "name": "Rashmi",
            "major": "IT",
            "starting_year": 2021,
            "total_attendance": 7,
            "standing": "G",
            "year": 3,
            "last_attendance_time": "2024-04-30 00:54:34"
        },
    "6":
        {
            "name": "Rashmi",
            "major": "IT",
            "starting_year": 2021,
            "total_attendance": 7,
            "standing": "G",
            "year": 3,
            "last_attendance_time": "2024-04-30 00:54:34"
        },
    "7":
        {
            "name": "Rashmi",
            "major": "IT",
            "starting_year": 2021,
            "total_attendance": 7,
            "standing": "G",
            "year": 3,
            "last_attendance_time": "2024-04-30 00:54:34"
        },
    "8":
        {
            "name": "Rashmi",
            "major": "IT",
            "starting_year": 2021,
            "total_attendance": 7,
            "standing": "G",
            "year": 3,
            "last_attendance_time": "2024-04-30 00:54:34"
        },
    "9":
        {
            "name": "Rashmi",
            "major": "IT",
            "starting_year": 2021,
            "total_attendance": 7,
            "standing": "G",
            "year": 3,
            "last_attendance_time": "2024-04-30 00:54:34"
        },
    "10":
        {
            "name": "Rashmi",
            "major": "IT",
            "starting_year": 2021,
            "total_attendance": 7,
            "standing": "G",
            "year": 3,
            "last_attendance_time": "2024-04-30 00:54:34"
        },
    "11":
        {
            "name": "Rashmi",
            "major": "IT",
            "starting_year": 2021,
            "total_attendance": 7,
            "standing": "G",
            "year": 3,
            "last_attendance_time": "2024-04-30 00:54:34"
        },
    "12":
        {
            "name": "Rashmi",
            "major": "IT",
            "starting_year": 2021,
            "total_attendance": 7,
            "standing": "G",
            "year": 3,
            "last_attendance_time": "2024-04-30 00:54:34"
        }
}

# for automatically updation in realtime database
for key, value in data.items():
    ref.child(key).set(value)
