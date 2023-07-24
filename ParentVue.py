import argparse
import json
from studentvue import StudentVue

parser = argparse.ArgumentParser(description='ParentVUE interface script.')
parser.add_argument("-u","--username", help="Provide username.")
parser.add_argument("-p","--password", help="Provide password.")
parser.add_argument("-d","--district", help="Provide district URL to connect to.", required=True)
parser.add_argument("--debug",
    help="Show raw payload from ParentVUE.",
    action="store_true")
args = parser.parse_args()

user = args.username
passw = args.password
domain = args.district
connection = StudentVue(user, passw, domain)

record = connection.get_student_info()

if (args.debug):
    print('DEBUG: Get raw payload from ParentVue...')
    record = connection.get_student_info()
    print(json.dumps(record, indent=4))
    raise SystemExit()
