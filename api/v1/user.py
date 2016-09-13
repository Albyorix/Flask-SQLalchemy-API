from __init__ import app, api, session
from flask import request, redirect, url_for
from models import Company, User, Team


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

