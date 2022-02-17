
from ..models import User, Data
from sqlalchemy import or_
from ..config import Config


class DataService(object):
    def __init__(self):
        pass

    def get_data(self, user_role,
                 user_province,
                 user_city,
                 page_size=0,
                 current_page=0,
                 province=[],
                 city=[],
                 district=[],
                 sex=[],
                 age=[],
                 keyword=None) -> dict:
        """
        获取数据

        Args:
          province: 筛选的省份
          city: 筛选的城市
          district: 筛选的区
          sex: 筛选的性别
          age: 筛选的年龄
          keyword: 搜索的名字、手机号
          user_province: 自己所在的省份
          user_city: 自己所在的市区
          user_role: 自己的角色
          page_size: 每页返回的条目数量，当设置为0时，则不分页
          current_page: 要查询的页（当page_size设置为0时，这个参数无意义）

        Return:
          {
            list:[]
            total:number
          }

        """
        def _format_data(item: Data):
            return {
                "id": item.id,
                "province": item.province,
                "city": item.city,
                "district": item.district,
                "name": item.name,
                "mobile": item.mobile,
                "age": item.age,
                "sex": item.sex,
            }
        query = Data.query

        # 筛选
        if len(province):
            query = query.filter(Data.province.in_(province))

        if len(city):
            query = query.filter(Data.city.in_(city))

        if len(district):
            query = query.filter(Data.district.in_(district))

        if len(age):
            query = query.filter(Data.age.in_(age))

        if len(sex):
            query = query.filter(Data.sex.in_(sex))

        if keyword:
            query = query.filter(
                or_(Data.mobile.like("%{}%".format(keyword)),
                    Data.name.like("%{}%".format(keyword))))

        # 根据用户角色过滤
        if user_role != Config.USER_ROLE_ROOT:
            # 暂不连带省and市过滤
            if user_role == Config.USER_ROLE_PROVINCE:
                query = query.filter(Data.province == user_province)
            if user_role == Config.USER_ROLE_CITY:
                query = query.filter(Data.city == user_city)

        total = query.count()

        # 是否分页
        if page_size > 0:
            query = query.limit(page_size).offset(
                (current_page - 1) * page_size)

        result = query.all()

        return {
            "list": [_format_data(o) for o in result] if result else [],
            "total": total
        }
