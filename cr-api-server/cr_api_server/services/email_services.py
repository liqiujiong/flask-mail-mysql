from .. import mail
from ..config import Config
from flask_mail import Message


class EmailService(object):

    @classmethod
    def send_mail(self, title, content, recipients) -> bool:
        try:
            recipients = recipients if isinstance(
                recipients, list) else [recipients]
            sender = Config.MAIL_USERNAME
            msg = Message(title,
                          sender=sender,
                          recipients=recipients)
            msg.body = content
            mail.send(msg)
            return True
        except Exception as e:
            return None

    @classmethod
    def send_mail_async(self, app, title, body, recipients):
        with app.app_context():
            self.send_mail(title, body, recipients)
