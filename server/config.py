import os

database_path = os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), "instance"), "datab.db")

SECRET_KEY = '598ea6577e2b4197ce6b5f59b859c590371c144b14cce9c82162f4448b7ee557'
DEBUG = True
SQLALCHEMY_DATABASE_URI = f"sqlite:///{database_path}"
