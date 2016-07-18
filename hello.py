from datetime import datetime
from flask import Flask, render_template
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment    # 时间
from flask import request, jsonify
import pymysql
import logging

app = Flask(__name__)

manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)    # 初始化Flask-Moment


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/')
def index():
    return render_template('index.html',
                           current_time=datetime.utcnow())    # 加入时间变量


@app.route('/register', methods=["POST", "GET"])
def register():
    useremail = request.form.get("userEmail", "")
    username = request.form.get("userName", "")
    userpwd = request.form.get("userPwd", "")
    useradd(useremail, username, userpwd)
    logging.debug(useremail, username, userpwd)
    return jsonify({"msg": "success"})


def useradd(useremail, username, userpwd):
    try:
        conn = pymysql.connect(host="localhost", user="root", password="123", db="my_db", charset="utf8")
        cur = conn.cursor()
        cur.execute("INSERT INTO users (userEmail, userName, userPwd) VALUES (%s, %s, %s)", (useremail, username, userpwd))
        conn.commit()
    except Exception :
        logging.error("=======")


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


if __name__ == '__main__':
    app.run()
