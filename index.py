# _*_ coding: utf-8 _*_


import os
import time
import logging
import pymysql
import shutil
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

YESTERDAY = time.strftime('%Y-%m-%d', time.localtime(time.time() - 24*60*60))

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
        cur.execute("INSERT INTO users (userEmail, userName, userPwd) VALUES (%s, %s, %s)",
                    (useremail, username, userpwd))
        conn.commit()
    except Exception as e:
        logging.error(Exception, ":", e)
    return


@app.route('/classify', methods=["POST", "GET"])
def get_classify():
    try:
        conn = pymysql.connect(host=SDB_HOST, user=SDB_USER, password=SDB_PWD, db=SDB_DB, charset=SDB_CHARSET)
        cur = conn.cursor()

        # yesterday soft TOP10
        cur.execute("SELECT a_pkgname, a_name, a_picurl, a_install_sum FROM t_apps_addi_united "
                    "WHERE a_softgame = 'soft' AND DATE(a_getdate) = %s ORDER BY a_install_sum "
                    "DESC LIMIT 10;", YESTERDAY)
        conn.commit()
        top_soft = cur.fetchall()
        dict_rank_soft = [(item[0], item[1], item[2], int(item[3])) for item in top_soft]
        dict_rank_soft = {"rankinfo_soft": dict_rank_soft}

        # delete dir and create new with the same name
        # if os.path.exists("F:/pythonworkspace/flasktest/static/pic"):
        #     shutil.rmtree(r"F:/pythonworkspace/flasktest/static/pic")
        #     os.makedirs("F:/pythonworkspace/flasktest/static/pic")

        # save pic of topsoft
        i = 0
        for soft in top_soft:
            logging.debug("Game is %s", soft)
            url = str(soft[2])
            path = "F:/pythonworkspace/flasktest/static/pic/topsoft" + str(i) + ".jpg"
            logging.debug("path is %s", path)
            data = urllib.request.urlopen(url).read()
            f = open(path, "wb")
            f.write(data)
            i += 1
            f.close()

        # yesterday game TOP10
        cur.execute("SELECT a_pkgname, a_name, a_picurl, a_install_sum FROM t_apps_addi_united "
                    "WHERE a_softgame = 'game' AND DATE(a_getdate) = %s ORDER BY a_install_sum "
                    "DESC LIMIT 10;", YESTERDAY)
        conn.commit()
        top_game = cur.fetchall()
        dict_rank_game = [(item[0], item[1], item[2], int(item[3])) for item in top_game]
        dict_rank_game = {"rankinfo_game": dict_rank_game}

        # save pic of topgame
        i = 0
        for game in top_game:
            logging.debug("Game is %s", game)
            url = str(game[2])
            path = "F:/pythonworkspace/flasktest/static/pic/topgame" + str(i) + ".jpg"
            logging.debug("path is %s", path)
            data = urllib.request.urlopen(url).read()
            f = open(path, "wb")
            f.write(data)
            i += 1
            f.close()

        # select yesterday speed of soft top 10
        cur.execute("SELECT DATE_SUB(LOCALTIME, INTERVAL 2 DAY), bf.a_picurl, af.a_pkgname, af.a_name, "
                    "af.a_install_sum - bf.a_install_sum AS speed FROM ( SELECT DISTINCT (a_pkgname), a_name, "
                    "a_install_sum, a_getdate, a_picurl, a_url FROM t_apps_addi_united WHERE a_install_sum > 100000000 "
                    "AND a_softgame = 'soft') bf, (SELECT a_pkgname, a_name, a_install_sum, a_getdate "
                    "FROM t_apps_addi_united WHERE a_install_sum > 100000000 AND "
                    "DATE(a_getdate) = DATE(DATE_SUB(LOCALTIME, INTERVAL 1 DAY)) "
                    "AND a_softgame = 'soft') af WHERE bf.a_pkgname = af.a_pkgname AND "
                    "DATE(bf.a_getdate) = DATE(DATE_SUB(LOCALTIME, INTERVAL 2 DAY)) ORDER BY speed DESC LIMIT 10;")
        conn.commit()
        speed_soft = cur.fetchall()
        dict_speed_soft = [(item[0], item[1], item[2], item[3], int(item[4])) for item in speed_soft]
        dict_speed_soft = {"speed_soft": dict_speed_soft}

        # save pic of speedsoft
        i = 0
        for soft in speed_soft:
            logging.debug("Game is %s", soft)
            url = str(soft[1])
            path = "F:/pythonworkspace/flasktest/static/pic/speedsoft" + str(i) + ".jpg"
            logging.debug("path is %s", path)
            data = urllib.request.urlopen(url).read()
            f = open(path, "wb")
            f.write(data)
            i += 1
            f.close()

        # select yesterday speed of game top 10
        cur.execute("SELECT DATE_SUB(LOCALTIME, INTERVAL 2 DAY), bf.a_picurl, af.a_pkgname, af.a_name, "
                    "af.a_install_sum - bf.a_install_sum AS speed FROM ( SELECT DISTINCT (a_pkgname), a_name, "
                    "a_install_sum, a_getdate, a_picurl, a_url FROM t_apps_addi_united WHERE a_install_sum > 100000000 "
                    "AND a_softgame = 'game') bf, (SELECT a_pkgname, a_name, a_install_sum, a_getdate "
                    "FROM t_apps_addi_united WHERE a_install_sum > 100000000 AND "
                    "DATE(a_getdate) = DATE(DATE_SUB(LOCALTIME, INTERVAL 1 DAY)) "
                    "AND a_softgame = 'game') af WHERE bf.a_pkgname = af.a_pkgname AND "
                    "DATE(bf.a_getdate) = DATE(DATE_SUB(LOCALTIME, INTERVAL 2 DAY)) ORDER BY speed DESC LIMIT 10;")
        conn.commit()
        speed_game = cur.fetchall()
        dict_speed_game = [(item[0], item[1], item[2], item[3], int(item[4])) for item in speed_game]
        dict_speed_game = {"speed_game": dict_speed_game}

        # save pic of speedgame
        i = 0
        for game in speed_game:
            logging.debug("Game is %s", game)
            url = str(game[1])
            path = "F:/pythonworkspace/flasktest/static/pic/speedgame" + str(i) + ".jpg"
            logging.debug("path is %s", path)
            data = urllib.request.urlopen(url).read()
            f = open(path, "wb")
            f.write(data)
            i += 1
            f.close()

        return jsonify(soft_classify, game_classify, dict_rank_soft, dict_rank_game, dict_speed_soft, dict_speed_game)

    except Exception as e:
        logging.error(Exception, ":", e)


@app.route("/softtop5")
def getsoft_top5():
    conn = pymysql.connect(host=SDB_HOST, user=SDB_USER, password=SDB_PWD, db=SDB_DB, charset=SDB_CHARSET)
    cur = conn.cursor()
    # soft top 5
    cur.execute("SELECT t0.a_pkgname, t0.a_name, date(t0.a_getdate) a_getdate, t0.a_install_sum FROM t_apps_addi_united t0 "
                "JOIN (SELECT t.a_pkgname FROM t_apps_addi_united t WHERE t.a_softgame = 'soft' AND "
                "DATE(t.a_getdate) = DATE_SUB(CURDATE(), INTERVAL 1 DAY) ORDER BY t.a_install_sum DESC LIMIT 5) t1 ON "
                "t0.a_pkgname = t1.a_pkgname WHERE DATE(t0.a_getdate) BETWEEN '2016-08-18' AND '2016-08-22';", YESTERDAY)
    soft_top5 =

    # game top 5
    cur.execute("SELECT t0.a_pkgname, t0.a_name, date(t0.a_getdate) a_getdate, t0.a_install_sum FROM t_apps_addi_united t0 "
                "JOIN (SELECT t.a_pkgname FROM t_apps_addi_united t WHERE t.a_softgame = 'game' AND "
                "DATE(t.a_getdate) = DATE_SUB(CURDATE(), INTERVAL 1 DAY) ORDER BY t.a_install_sum DESC LIMIT 5) t1 ON "
                "t0.a_pkgname = t1.a_pkgname WHERE DATE(t0.a_getdate) BETWEEN '2016-08-18' AND '2016-08-22';", YESTERDAY)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
