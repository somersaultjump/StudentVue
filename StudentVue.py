import argparse
import json
from studentvue import StudentVue

parser = argparse.ArgumentParser(description='StudentVUE interface script.')
parser.add_argument("-g","--grades", help="Returns grades for each class.", action="store_true")
parser.add_argument("-a","--attendance", help="Returns attendance report.", action="store_true")
parser.add_argument("-s","--studentid", help="Provide student ID to avoid being prompted.")
parser.add_argument("-d","--district", help="Provide district URL to connect to.", required=True)
parser.add_argument("--debug",
    help="Show raw payload from StudentVUE. Requires record flag (-a, -g, etc.)",
    action="store_true")
args = parser.parse_args()

def get_student_id():
    """Get student ID from user."""
    if args.studentid:
        user = args.studentid
        passw = user
    else:
        user = input("Enter student ID: \n")
        passw = user
    domain = args.district
    connection = StudentVue(user, passw, domain)
    return connection

def get_grades(svconnect):
    """Retrieve student grades"""
    print('Retrieving grades from StudentVUE...')
    svgrade = svconnect.get_gradebook()
    try:
        courses = svgrade['Gradebook']['Courses']['Course']
    except Exception as exc:
        raise SystemExit('\nERROR: Unable to obtain grades.\n'
            '\t- is the student ID correct?\n'
            '\t- is the domain/url correct?') from exc
    all_grades = []

    for each_class in courses:
        classtitle = each_class['@Title']
        instructor = each_class['@Staff']
        markname = each_class['Marks']['Mark']['@MarkName']
        scoreraw = each_class['Marks']['Mark']['@CalculatedScoreRaw']
        result = print(f'=====[ {classtitle} ]=====\n'
            f'Instructor: {instructor}\n'
            f'Mark: {markname}\n'
            f'Grade: {scoreraw}\n')
        all_grades.append(result)
    return all_grades

def get_attendance(svconnect):
    """Retrieve student attendance records"""
    print('Retrieving attendance records from StudentVUE...')
    svattend = svconnect.get_attendance()
    try:
        missed_days = svattend['Attendance']['Absences']['Absence']
    except Exception as exc:
        raise SystemExit('\nERROR: Unable to retreive attendance records.\n'
            '\t- is the student ID correct?\n'
            '\t- is the domain/url correct?') from exc
    all_absenses = []

    for each_date in missed_days:
        this_day = each_date["@AbsenceDate"]
        print('########################')
        print(f'#####[ {this_day} ]#####')
        print('########################\n')

        for each_class in each_date["Periods"]["Period"]:
            if len(each_class["@Name"]) > 1:
                classtitle = each_class["@Course"]
                reason = each_class["@Name"]
                instructor = each_class["@Staff"]
                email = each_class["@StaffEMail"]

                if classtitle != "Lunch":
                    absense_result = print(f'=====[ {classtitle} ]=====\n'
                    f'Reason: {reason}\n'
                    f'Instructor: {instructor}\n'
                    f'Email: {email}\n')

                all_absenses.append(absense_result)
    return all_absenses

if (args.debug and args.grades):
    print('DEBUG: Get raw grade payload from StudentVUE...')
    gb = (get_student_id()).get_gradebook()
    print(json.dumps(gb, indent=4))
    raise SystemExit()

if (args.debug and args.attendance):
    print('DEBUG: Get raw attendance payload from StudentVUE...')
    attend = (get_student_id()).get_attendance()
    print(json.dumps(attend, indent=4))
    raise SystemExit()

if args.debug:
    raise SystemExit("You need to provice an argument to debug; -a or -g")

if args.grades:
    get_grades(get_student_id())
    raise SystemExit()

if args.attendance:
    get_attendance(get_student_id())
    raise SystemExit()
