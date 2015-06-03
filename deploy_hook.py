# coding=utf-8
from flask import Flask, request

app = Flask(__name__)


@app.route('/', methods=['post'])
def hello_world():
    # 表单
    print request.form
    print request.args
    print request.data
    return 'Hello World!'


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
