from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

db = SQLAlchemy()
csrf = CSRFProtect()

def init_exetensions(server: object) -> None:
    db.init_app(server)
    csrf.init_app(server)
