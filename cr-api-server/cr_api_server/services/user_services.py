
import random
from threading import Thread
import redis
from cr_api_server.models.user import User
from cr_api_server.repositorys.props import error, success
from cr_api_server.services.email_services import EmailService
from .. import Config, app, db

redis_client = redis.StrictRedis.from_url(app.config.get("REDIS_URL"))


class UserService(object):

    def get_user_by_mail(self, mail):
        user = User.query.filter(User.mail == mail).first()
        return user

    def create_user(self, user: User) -> bool:
        """
        创建用户

        Args:
          User

        return:
          Response
        """
        try:
            if self.get_user_by_mail(user.mail):
                return error(reason="已存在用户")
            db.session.add(user)
            db.session.flush()
            db.session.commit()
            return success()
        except Exception as e:
            return error(reason="失败！create_user出错，原因：{}".format(str(e)))

    def send_login_code(self, mail):
        """
        发送验证码

        Args:
          mail:邮箱

        Retrun:
          Response
        """
        try:
            if not self.get_user_by_mail(mail):
                return error(reason="请先注册用户")

            ttl = redis_client.ttl(mail)
            remain_time = abs(ttl - Config.MAIL_CODE_TIME)
            if remain_time <= Config.MAIL_CODE_RESEND:
                return error(
                    reason='请稍等{}秒后再发'.format(
                        Config.MAIL_CODE_RESEND - remain_time))

            title = '邮箱验证码登录'
            recipients = [mail]
            code = ''.join(random.sample('0123456789', 4))
            body = '您的登录验证码是:{}'.format(code)

            redis_client.set(mail, code, ex=Config.MAIL_CODE_TIME)

            thr = Thread(target=EmailService.send_mail_async,
                         args=[app, title, body, recipients])
            thr.start()
            return success()

        except Exception as e:
            return error(reason="失败！send_login_code出错，原因：{}".format(str(e)))

    def verify_code(self, mail, code) -> bool:
        """
        登录code验证

        Args:
          mail
          code

        Retrun:
          bool
        """
        verify_code = redis_client.get(mail)
        if int(verify_code) == code:
            return True
        return False
