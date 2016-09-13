from __init__ import app, api, session
from flask import request, redirect, url_for
from models import Company, User, Team


@app.route(api + "/team", methods=['GET'])
def list_team():
    """List all teams"""
    teams = session.query(Team).all()
    return str(teams)


@app.route(api + "/team", methods=['POST'])
def post_team():
    """Create a new team from:
    {
    "name": string,
    "company_id": valic company id,
    "members": list of user id {"id": valid user id}
    }
    """
    # A team is defined by its name and company, but not by its members
    name = request.json["name"]
    company_id = request.json["company_id"]
    try:
        team = session.query(Team).filter(Team.name==name and Team.company.id==company_id).one()
        # if it exists already, return it
        return str(team)
    except:
        # if it does not exists create a new team
        new_team = Team(name=name)
        company = session.query(Company).filter_by(id=company_id).first()
        new_team.company = company
        members = request.json["members"]
        if len(members) < 2:
            return "Team too small", 409
        for user in members:
            user = session.query(User).filter_by(id=user["id"]).first()
            new_team.members.append(user)
            # Update the user company in case it it not the same
            user.company = company
            session.commit()
        session.add(new_team)
        session.commit()
        return str(new_team)


@app.route(api + "/team/<int:id>/", methods=['GET'])
def get_team(id):
    """Show one team"""
    team = session.query(Team).filter(Team.id == id).first()
    return str(team)


@app.route(api + "/team/<int:id>/", methods=['PUT'])
def put_team(id):
    """Edit one team"""
    team = session.query(Team).filter(Team.id == id).first()
    if "name" in request.json.keys():
        team.name = request.json["name"]
    if "company_id" in request.json.keys():
        company_id = request.json["company"]
        company = session.query(Company).filter_by(id=company_id).first()
        team.company = company
    if "members" in request.json.keys():
        for user in request.json["members"]:
            user = session.query(User).filter_by(id=user["id"]).first()
            team.members.append(user)
            # Update the user company in case it it not the same
            user.company = team.company
            session.commit()
    session.commit()
    return str(team)


@app.route(api + "/team/<int:id>/", methods=['DELETE'])
def delete_team(id):
    """Delete one team"""
    session.query(Team).filter(Team.id == id).delete()
    return redirect(url_for("list_team"))
