# coding:utf-8

from marshmallow import Schema, fields

class LoginUserSchema(Schema):
    mail = fields.Email(required=True)
    code = fields.Int(required=True)

    class Meta:
        strict = True

class CreateUserSchema(Schema):
    mail = fields.Email(required=True)
    province = fields.Str(required=True)
    city = fields.Str(required=True)
    district = fields.Str(required=True)
    role = fields.Int(required=True)

    class Meta:
        strict = True


class SendCodeSchema(Schema):
    mail = fields.Email(required=True)

    class Meta:
        strict = True