from setuptools import setup
import os

setup(
    name='teams',
    version='1.1.0',
    author='Mikey Waites, Jack Saunders, Alfred Bourely',
)

DEBUG = True
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'db/osldev.db')
DATABASE_CONNECT_OPTIONS = {}

