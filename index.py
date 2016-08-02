# _*_ coding: utf-8 _*_


import logging
from datetime import datetime
import pymysql
from flask import Flask, render_template
from flask import request, jsonify
from tag_config.app_tags import *

app = Flask(__name__)

# ----server----
SDB_HOST = "101.200.174.172"
SDB_DB = "data_apps"
SDB_USER = "dba_apps"
SDB_PWD = "mimadba_apps"
SDB_CHARSET = "utf8"

# ----local----
# DB_HOST = "127.0.0.1"
# DB_DB = "app_db"
# DB_USER = "root"
# DB_PWD = "123"
# DB_CHARSET = "utf8"


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
    except Exception as e:
        logging.error(Exception, ":", e)
    return


@app.route('/classify', methods=["POST", "GET"])
def get_classify():
    try:
        conn = pymysql.connect(host=SDB_HOST, user=SDB_USER, password=SDB_PWD, db=SDB_DB, charset=SDB_CHARSET)
        cur = conn.cursor()
        cur.execute("SELECT a_pkgname, a_name, a_picurl, a_install FROM t_apps_additional_united "
                    "WHERE a_softgame = 'soft' AND DATE(a_getdate) = '2016-08-01' ORDER BY a_install DESC LIMIT 10;")
        conn.commit()
        """0:pkgnamge 1:name 2:picurl 3:install"""
        dict_rank_soft = [(item[0], item[1], item[2], int(item[3])) for item in cur.fetchall()]
        dict_rank_soft = {"rankinfo_soft": dict_rank_soft}

        cur.execute("SELECT a_pkgname, a_name, a_picurl, a_install FROM t_apps_additional_united "
                    "WHERE a_softgame = 'game' AND DATE(a_getdate) = '2016-08-01' ORDER BY a_install DESC LIMIT 10;")
        conn.commit()
        """0:pkgnamge 1:name 2:picurl 3:install"""
        dict_rank_game = [(item[0], item[1], item[2], int(item[3])) for item in cur.fetchall()]
        dict_rank_game = {"rankinfo_game": dict_rank_game}

        return jsonify(soft_classify, game_classify, dict_rank_soft, dict_rank_game)
    except Exception as e:
        logging.error(Exception, ":", e)


if __name__ == "__main__":
    app.run(debug=True)
