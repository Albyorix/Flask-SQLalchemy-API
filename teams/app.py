from flask import Flask, request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from initdb import User, Base, Company, Team, init_db
from os import remove

api_version = "v1"
api = "/api/" + api_version

########################################
####       !!!  WARNING  !!!        ####
####   For dev environment only     ####
####   This reinit the whole DB     ####
########################################

db_path = "osldev.db"
remove(db_path)
sqlite_path = "sqlite:///" + db_path
init_db(sqlite_path)

app = Flask(__name__)

engine = create_engine(sqlite_path)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
DBSession.bind = engine
session = DBSession()


@app.route(api + "/company", methods=['GET'])
def list_company():
    """List all companies"""
    companies = session.query(Company).all()
    return str(companies)


@app.route(api + "/company", methods=['POST'])
def post_company():
    """Create a new company"""
    name = request.json["name"]
    try:
        company = session.query(Company).filter_by(name=name).one()
        # if it exists already, return it
        return str(company)
    except:
        # if it does not exists create a new company
        new_company = Company(name=name)
        session.add(new_company)
        session.commit()
        return str(new_company)


@app.route(api + "/company/<int:id>/", methods=['GET'])
def get_company(id):
    """Show one company"""
    company = session.query(Company).filter(Company.id == id).first()
    return str(company)


@app.route(api + "/company/<int:id>/team", methods=['GET'])
def get_company_team(id):
    """Show the teams of the company"""
    company = session.query(Company).filter(Company.id == id).first()
    teams = company.teams
    return str(teams)


@app.route(api + "/company/<int:id>/", methods=['PUT'])
def put_company(id):
    """Edit one company"""
    name = request.json["name"]
    company = session.query(Company).filter(Company.id == id).first()
    company.name = name
    session.commit()
    return str(company)


@app.route(api + "/company/<int:id>/", methods=['DELETE'])
def delete_company(id):
    """Delete one company"""
    session.query(Company).filter(Company.id == id).delete()
    return redirect(url_for("list_company"))


@app.route(api + "/user", methods=['GET'])
def list_user():
    """List all users"""
    users = session.query(User).all()
    return str(users)


@app.route(api + "/user", methods=['POST'])
def post_user():
    """Create a new user"""
    email = request.json["email"]
    try:
        user = session.query(User).filter_by(email=email).one()
        # if it exists already, return it
        return str(user)
    except:
        # if it does not exists create a new user
        new_user = User(email=email,
                        name=request.json["name"])
        if "company" in request.json.keys():
            company_id = request.json["company"]
            company = session.query(Company).filter_by(id=company_id).first()
            new_user.company = company
        if "team" in request.json.keys():
            team_id = request.json["team"]
            team = session.query(Team).filter_by(id=team_id).first()
            new_user.company = team
        session.add(new_user)
        session.commit()
        return str(new_user)


@app.route(api + "/user/<int:id>/", methods=['GET'])
def get_user(id):
    """Show one user"""
    user = session.query(User).filter(User.id == id).first()
    return str(user)


@app.route(api + "/user/<int:id>/", methods=['PUT'])
def put_user(id):
    """Edit one user"""
    user = session.query(User).filter(User.id == id).first()
    if "name" in request.json.keys():
        user.name = request.json["name"]
    if "email" in request.json.keys():
        user.email = request.json["email"]
    if "company" in request.json.keys():
        company_id = request.json["company"]
        company = session.query(Company).filter_by(id=company_id).first()
        user.company = company
    if "team" in request.json.keys():
        team_id = request.json["team"]
        team = session.query(Team).filter_by(id=team_id).first()
        user.company = team
    session.commit()
    return str(user)


@app.route(api + "/user/<int:id>/", methods=['DELETE'])
def delete_user(id):
    """Delete one user"""
    session.query(User).filter(User.id == id).delete()
    return redirect(url_for("list_user"))


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


if __name__ == "__main__":
    app.run(debug=True)
