# -*- coding:utf-8 -*-
from flask import Blueprint, request
from cr_api_server.models.user import User
from cr_api_server.repositorys.token import IDToken
from cr_api_server.services.user_services import UserService
from ..repositorys.props import auth, success, error, panic
from ..types.user_schema import CreateUserSchema, LoginUserSchema, SendCodeSchema
from ..config import Config

user_view = Blueprint("user_view", __name__)
id_token_client = IDToken(Config.JWT_SECRET)
user_service = UserService()


@user_view.route("/login", methods=["POST"])
@panic(LoginUserSchema)
def do_login(payload):

    mail = payload.get('mail')
    code = payload.get('code')

    if not user_service.verify_code(mail, code):
        return error(reason='登录失败：登录验证码错误')

    user: User = user_service.get_user_by_mail(mail)

    user_info = {
        "id": user.id,
        "role": user.role,
        "province": user.province,
        "city": user.city
    }

    # build token
    id_token = id_token_client.jwt_encode(user_info)
    id_token_dict = id_token_client.jwt_decode(id_token)

    return success({
        "result": {
            "jwt": id_token,
            "jwt_exp": id_token_dict.get("exp"),
            "role": user_info["role"],
            "province": user_info["province"],
            "city": user_info["city"]
        }
    })


@user_view.route("/create", methods=["POST"])
@panic(CreateUserSchema)
def create_user(payload):

    user = User(
        role=payload.get('role'),
        mail=payload.get('mail'),
        province=payload.get('province'),
        city=payload.get('city'),
        district=payload.get('district'))

    return user_service.create_user(user)


@user_view.route("/code", methods=["POST"])
@panic(SendCodeSchema)
def send_mail_code(payload):

    mail = payload.get('mail')

    return user_service.send_login_code(mail)
