from requests import get, post, put, delete
import sys
from ast import literal_eval


def test_OSL():
    ############################################
    ###          Prerequisites               ###
    ############################################
    base_url = "http://127.0.0.1:5000/api/v1/"
    # Create a company
    company_url = base_url + "company"
    osl = {"name": "Old Street Labs"}
    r = post(company_url, json=osl)
    assert(r.status_code == 200)
    dico = literal_eval(r.text)
    osl_id = dico["id"]
    assert(osl_id == 1)

    # Create another company
    eki = {"name": "eki"}
    r = post(company_url, json=eki)
    dico = literal_eval(r.text)
    eki_id = dico["id"]
    assert(eki_id == 2)

    # Create a user
    user_url = base_url + "user"
    mike = {"name": "mike",
            "email": "mike@osl.com",
            "company_id": osl_id}
    r = post(user_url, json=mike)
    assert(r.status_code == 200)
    dico = literal_eval(r.text)
    mike_id = dico["id"]
    assert(mike_id == 1)

    # Create 3 other users
    john = {"name": "john",
            "email": "john@osl.com",
            "company_id": osl_id}
    r = post(user_url, json=john)
    dico = literal_eval(r.text)
    john_id = dico["id"]
    assert(john_id == 2)

    fred = {"name": "fred",
            "email": "fred@eki.com",
            "company_id": eki_id}
    r = post(user_url, json=fred)
    dico = literal_eval(r.text)
    fred_id = dico["id"]
    assert(fred_id == 3)

    hugo = {"name": "hugo",
            "email": "hugo@eki.com",
            "company_id": eki_id}
    r = post(user_url, json=hugo)
    dico = literal_eval(r.text)
    hugo_id = dico["id"]
    assert(hugo_id == 4)

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
    assert(r.status_code == 200)
    dico = literal_eval(r.text)
    osl_eng_id = dico["id"]
    assert(osl_eng_id == 1)

    # Create a second team
    eki_cons = {"name": "consulting",
                "members": [{"id": fred_id},
                            {"id": hugo_id}],
                "company_id": eki_id}
    r = post(team_url, json=eki_cons)
    dico = literal_eval(r.text)
    eki_cons_id = dico["id"]
    assert(eki_cons_id == 2)

    # View a list of all the teams
    r = get(team_url)
    assert(r.status_code == 200)
    assert(r.text == "[{'company_id': 1,"
                     " 'name': u'engineering',"
                     " 'members': [{'id': 1}, {'id': 2}],"
                     " 'id': 1},"
                     " {'company_id': 2,"
                     " 'name': u'consulting',"
                     " 'members': [{'id': 3}, {'id': 4}],"
                     " 'id': 2}]")

    # View a list of all the teams for a specific company
    osl_team_url = company_url + "/" + str(osl_id) + "/team"
    r = get(osl_team_url)
    assert(r.status_code == 200)
    assert(r.text == "[{'company_id': 1,"
                     " 'name': u'engineering',"
                     " 'members': [{'id': 1}, {'id': 2}],"
                     " 'id': 1}]")

    # View a specific team
    osl_eng_url = team_url + "/" + str(osl_eng_id) + "/"
    r = get(osl_eng_url)
    assert(r.text == "{'company_id': 1,"
                     " 'name': u'engineering',"
                     " 'members': [{'id': 1}, {'id': 2}],"
                     " 'id': 1}")

if __name__ == "__main__":
    test_OSL()
