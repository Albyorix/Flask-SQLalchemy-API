from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Company(Base):
    __tablename__ = "company"

    def __repr__(self):
        dico = {}
        dico["name"] = self.name
        dico["id"] = self.id
        dico["teams"] = [{"id": team.id} for team in self.teams]
        dico["employee"] = [{"id": user.id} for user in self.employees]
        return str(dico)

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False, unique=True)
    # One company has many teams
    teams = relationship("Team", back_populates="company")
    # One company has many members
    employees = relationship("User", back_populates="company")


class User(Base):
    __tablename__ = "user"

    def __repr__(self):
        dico = {}
        dico["name"] = self.name
        dico["id"] = self.id
        dico["email"] = self.email
        dico["company_id"] = self.company_id
        dico["team_id"] = self.team_id
        return str(dico)

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False, unique=True)
    # One user belongs to a company
    company_id = Column(Integer, ForeignKey("company.id"))
    company = relationship("Company", back_populates="employees")
    # One user belongs to a team
    team_id = Column(Integer, ForeignKey("team.id"))
    team = relationship("Team", back_populates="members")


class Team(Base):
    __tablename__ = "team"

    def __repr__(self):
        dico = {}
        dico["name"] = self.name
        dico["id"] = self.id
        dico["members"] = [{"id": user.id} for user in self.members]
        dico["company_id"] = self.company_id
        return str(dico)

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    # One team has many members
    members = relationship("User", back_populates="team")
    # One team belongs to a company
    company_id = Column(Integer, ForeignKey("company.id"), nullable=False)
    company = relationship("Company", back_populates="teams")


def init_db(sqlite_path):
    # Create an engine that stores data in the local directory's
    engine = create_engine(sqlite_path)

    # Create all tables in the engine
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    init_db("sqlite:///osldev.db")
