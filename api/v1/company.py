from __init__ import app, api, session
from flask import request, redirect, url_for
from models import Company


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

