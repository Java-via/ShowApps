# _*_ coding: utf-8 _*_


import time
import logging
import pymysql
import urllib.request
from flask import Flask, render_template
from flask import request, jsonify
from tag_config.app_tags import *

logging.basicConfig(level=logging.DEBUG)
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


# @app.route('/')
# def index():
#     return render_template('index.html',
#                            current_time=datetime.utcnow())    # 加入时间变量


@app.route('/')
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
        yesterday = time.strftime('%Y-%m-%d', time.localtime(time.time() - 24*60*60))
        conn = pymysql.connect(host=SDB_HOST, user=SDB_USER, password=SDB_PWD, db=SDB_DB, charset=SDB_CHARSET)
        cur = conn.cursor()
        cur.execute("SELECT a_pkgname, a_name, a_picurl, a_install_sum FROM t_apps_addi_united "
                    "WHERE a_softgame = 'soft' AND DATE(a_getdate) = %s ORDER BY a_install_sum DESC LIMIT 10;", yesterday)
        conn.commit()
        """0:pkgnamge 1:name 2:picurl 3:install"""
        dict_rank_soft = [(item[0], item[1], item[2], int(item[3])) for item in cur.fetchall()]
        dict_rank_soft = {"rankinfo_soft": dict_rank_soft}

        cur.execute("SELECT a_pkgname, a_name, a_picurl, a_install_sum FROM t_apps_addi_united "
                    "WHERE a_softgame = 'game' AND DATE(a_getdate) = %s ORDER BY a_install_sum DESC LIMIT 10;", yesterday)
        conn.commit()
        """0:pkgnamge 1:name 2:picurl 3:install"""
        dict_rank_game = [(item[0], item[1], item[2], int(item[3])) for item in cur.fetchall()]
        dict_rank_game = {"rankinfo_game": dict_rank_game}

        cur.execute("SELECT DATE_SUB(LOCALTIME, INTERVAL 2 DAY), bf.a_picurl, af.a_pkgname, af.a_name, "
                    "af.a_install_sum - bf.a_install_sum AS speed FROM ( SELECT DISTINCT (a_pkgname), a_name, "
                    "a_install_sum, a_getdate, a_picurl, a_url FROM t_apps_addi_united WHERE a_install_sum > 100000000 "
                    "AND a_softgame = 'soft') bf, (SELECT a_pkgname, a_name, a_install_sum, a_getdate "
                    "FROM t_apps_addi_united WHERE a_install_sum > 100000000 AND "
                    "DATE(a_getdate) = DATE(DATE_SUB(LOCALTIME, INTERVAL 1 DAY)) "
                    "AND a_softgame = 'soft') af WHERE bf.a_pkgname = af.a_pkgname AND "
                    "DATE(bf.a_getdate) = DATE(DATE_SUB(LOCALTIME, INTERVAL 2 DAY)) ORDER BY speed DESC LIMIT 10;")
        conn.commit()
        """0:pkgnamge 1:name 2:picurl 3:install"""
        dict_speed_soft = [(item[0], item[1], item[2], item[3], int(item[4])) for item in cur.fetchall()]
        dict_speed_soft = {"speed_soft": dict_speed_soft}

        cur.execute("SELECT DATE_SUB(LOCALTIME, INTERVAL 2 DAY), bf.a_picurl, af.a_pkgname, af.a_name, "
                    "af.a_install_sum - bf.a_install_sum AS speed FROM ( SELECT DISTINCT (a_pkgname), a_name, "
                    "a_install_sum, a_getdate, a_picurl, a_url FROM t_apps_addi_united WHERE a_install_sum > 100000000 "
                    "AND a_softgame = 'game') bf, (SELECT a_pkgname, a_name, a_install_sum, a_getdate "
                    "FROM t_apps_addi_united WHERE a_install_sum > 100000000 AND "
                    "DATE(a_getdate) = DATE(DATE_SUB(LOCALTIME, INTERVAL 1 DAY)) "
                    "AND a_softgame = 'game') af WHERE bf.a_pkgname = af.a_pkgname AND "
                    "DATE(bf.a_getdate) = DATE(DATE_SUB(LOCALTIME, INTERVAL 2 DAY)) ORDER BY speed DESC LIMIT 10;")
        conn.commit()
        """0:data 1:picurl 2:pkgname 3:name 4:install"""
        speed_game = cur.fetchall()
        dict_speed_game = [(item[0], item[1], item[2], item[3], int(item[4])) for item in speed_game]
        dict_speed_game = {"speed_game": dict_speed_game}
        # for game in speed_game:
        #     logging.debug("Game is %s", game)
        #     url = str(game[1])
        #     path = "f:/static/" + url.replace(".")
        #     resp = urllib.request.urlopen(url=url)
        #     data = resp.read()
        #     f = open(path, "wb")
        #     f.write(data)
        #     f.close()

        return jsonify(soft_classify, game_classify, dict_rank_soft, dict_rank_game, dict_speed_soft, dict_speed_game)
    except Exception as e:
        logging.error(Exception, ":", e)


if __name__ == "__main__":
    app.run(debug=True)
