
import time
from .. import db

class User(db.Model):
    __tablename__ = "user"

    id        = db.Column("id", db.Integer, autoincrement=True, primary_key=True)
    role      = db.Column("role", db.Integer)# 0超管 1省管 2市管
    mail      = db.Column("mail", db.String(128))
    province  = db.Column("province", db.String(128))
    city      = db.Column("city", db.String(128))
    district  = db.Column("district", db.String(128))
    create_at = db.Column("create_at", db.Integer, default=time.time,)
