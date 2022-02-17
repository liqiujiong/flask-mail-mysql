
from .. import db


class Data(db.Model):
    __tablename__ = "data"

    id        = db.Column("id", db.Integer, autoincrement=True, primary_key=True)
    province  = db.Column("province", db.String(128))
    city      = db.Column("city", db.String(128))
    district  = db.Column("district", db.String(128))
    name      = db.Column("name", db.String(128))
    mobile    = db.Column("mobile", db.String(128))
    age       = db.Column("age", db.Integer)
    sex       = db.Column("sex", db.String(128))
