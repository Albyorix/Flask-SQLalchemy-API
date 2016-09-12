from requests import get, post, put, delete
import sys
from ast import literal_eval

############################################
###          Prerequisites               ###
############################################

base_url = "http://127.0.0.1:5000/api/v1/"
# Create a company
company_url = base_url + "company"
osl = {"name": "Old Street Labs"}
r = post(company_url, json=osl)
if not r.status_code == 200:
    print "Could not create a company"
    print r.text
    sys.exit(1)
dico = literal_eval(r.text)
osl_id = dico["id"]
print "OSL:", dico

# Create another company
eki = {"name": "eki"}
r = post(company_url, json=eki)
dico = literal_eval(r.text)
eki_id = dico["id"]
print "EKI:", dico


# Create a user
user_url = base_url + "user"
mike = {"name": "mike",
        "email": "mike@osl.com",
        "company_id": osl_id}
r = post(user_url, json=mike)
if not r.status_code == 200:
    print "Could not create a user"
    print r.text
    sys.exit(1)
dico = literal_eval(r.text)
mike_id = dico["id"]
print "MIKE:", dico

# Create 3 other users
john = {"name": "john",
        "email": "john@osl.com",
        "company_id": osl_id}
r = post(user_url, json=john)
dico = literal_eval(r.text)
john_id = dico["id"]
print "JOHN:", dico

fred = {"name": "fred",
        "email": "fred@eki.com",
        "company_id": eki_id}
r = post(user_url, json=fred)
dico = literal_eval(r.text)
fred_id = dico["id"]
print "FRED:", dico

hugo = {"name": "hugo",
        "email": "hugo@eki.com",
        "company_id": eki_id}
r = post(user_url, json=hugo)
dico = literal_eval(r.text)
hugo_id = dico["id"]
print "HUGO:", dico


############################################
###          Requirements                ###
############################################

# Create a new team
team_url = base_url + "team"
osl_eng = {"name": "engineering",
           "members": [{"id": mike_id},
                       {"id": john_id}],
           "company_id": osl_id}
r = post(team_url, json=osl_eng)
if not r.status_code == 200:
    print "Could not create a team"
    print r.text
    sys.exit(1)
dico = literal_eval(r.text)
osl_eng_id = dico["id"]
print "OSL ENG:", dico

# Create a second team
eki_cons = {"name": "consulting",
            "members": [{"id": fred_id},
                        {"id": hugo_id}],
            "company_id": eki_id}
r = post(team_url, json=eki_cons)
dico = literal_eval(r.text)
eki_cons_id = dico["id"]
print "EKI CONS:", dico

# View a list of all the teams
r = get(team_url)
if not r.status_code == 200:
    print "Could not list all teams"
    print r.text
    sys.exit(1)
print "ALL TEAMS", r.text

# View a list of all the teams for a specific company
osl_team_url = company_url + "/" + str(osl_id) + "/team"
r = get(osl_team_url)
if not r.status_code == 200:
    print "Could not list teams from one company"
    print r.text
    sys.exit(1)
print "OSL TEAMS", r.text

# View a specific team
osl_eng_url = team_url + "/" + str(osl_eng_id) + "/"
r = get(osl_eng_url)
print "OSL ENG:", dico
