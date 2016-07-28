# _*_ coding: utf-8 _*_


import logging
from datetime import datetime
import pymysql
from flask import Flask, render_template
from flask import request, jsonify
from tag_config.app_tags import *

# from flask_moment import Moment    # 时间

app = Flask(__name__)

# moment = Moment(app)    # 初始化Flask-Moment
# test


@app.route('/')
def index():
    return render_template('index.html',
                           current_time=datetime.utcnow())    # 加入时间变量


@app.route('/all')
def all():
    return render_template('all_data.html')


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
    except Exception:
        logging.error("=======")
    return


@app.route('/classify', methods=["POST", "GET"])
def get_classify():
    conn = pymysql.connect(host="localhost", user="root", password="123", db="app_db", charset="utf8")
    cur = conn.cursor()
    cur.execute("SELECT * FROM view_soft_install;")
    conn.commit()
    dict_rank_soft = [(item[0], item[1], item[2], int(item[3])) for item in cur.fetchall()]
    dict_rank_soft = {"rankinfo_soft": dict_rank_soft}

    cur.execute("SELECT * FROM view_game_install;")
    conn.commit()
    dict_rank_game = [(item[0], item[1], item[2], int(item[3])) for item in cur.fetchall()]
    dict_rank_game = {"rankinfo_game": dict_rank_game}

    return jsonify(soft_classify, game_classify, dict_rank_soft, dict_rank_game)


if __name__ == "__main__":
    app.run(debug=True)
