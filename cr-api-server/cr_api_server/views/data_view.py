# -*- coding:utf-8 -*-
import math
from flask import Blueprint, request, g
from cr_api_server.services.data_services import DataService
from ..repositorys.props import auth, success, error, panic

data_view = Blueprint("data_view", __name__)
dataService = DataService()


@data_view.route("", methods=["GET"])
@auth
@panic()
def get_data_list():

    # 入参
    province = request.args.getlist("province", None)
    city = request.args.getlist("city", None)
    district = request.args.getlist("district", None)
    age = request.args.getlist("age", None)
    sex = request.args.getlist("sex", None)
    page_size = int(request.args.get("page_size", 20))
    current_page = int(request.args.get("current_page", 1))
    keyword = request.args.get("keyword", None)

    result = dataService.get_data(
        user_province=g.user_province,
        user_city=g.user_city,
        user_role=g.user_role,
        page_size=page_size,
        current_page=current_page,
        province=province,
        city=city,
        district=district,
        sex=sex,
        age=age,
        keyword=keyword)

    project_list_counts = result.get('total')

    return success({
        "current": current_page,
        "pageSize": page_size,
        "total": project_list_counts,
        "total_page": int(math.ceil(project_list_counts / page_size)),
        "list": result.get('list')
    })
