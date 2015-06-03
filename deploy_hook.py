# coding=utf-8
import os
from flask import Flask, request
from flask.ext.mail import Message, Mail

app = Flask(__name__)


class Config(object):
    MAIL_SERVER = 'smtp.exmail.qq.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_TO = [os.environ.get('MAIL_TO')]

    GIT_TOKEN = os.environ.get('GIT_TOKEN')


app.config.from_object(Config)

mail = Mail(app=app)


@app.route('/', methods=['post'])
def hello_world():
    # 表单
    app.logger.debug('data: {data}'.format(data=request.data))
    j = request.json
    if j and app.config.get('GIT_TOKEN') == j.get('token') and 'push' == j.get('event') and 'master' == j.get('ref'):
        content = u''
        for commit in j.get('commits'):
            content += u'{name}：{desc}\r\n'.format(name=commit.get('committer').get('name'), desc=commit.get('short_message'))

        # TODO deploy project

        # send mail
        send_mail(u'项目部署', content)
        return 'success'
    return 'error'


def send_mail(subject, content):
    app.logger.debug(u'send mail. subject: {subject}, content: {content}'.format(subject=subject, content=content))
    msg = Message(subject=subject, sender=app.config.get('MAIL_USERNAME'), recipients=app.config.get('MAIL_TO'))
    msg.body = content
    mail.send(msg)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
