# _*_ coding: utf-8 _*_


import datetime
import logging
import pymysql
import urllib.request
from flask import Flask, render_template
from flask import request, jsonify
from tag_config.app_tags import *
import util

logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)

# ----server----
SDB_HOST = "101.200.174.172"
SDB_DB = "data_apps"
SDB_USER = "dba_apps"
SDB_PWD = "mimadba_apps"
SDB_CHARSET = "utf8"

YESTERDAY = (datetime.date.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')

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
    """
    turn to index page
    :return:
    """
    return render_template('all_data.html')


@app.route("/softgametop")
def softgametop():
    """
    turn to top 5 radar chart
    :return:
    """
    return render_template("top5detail.html")


@app.route("/softgame")
def softgame():
    """
    turn to app top5 7days line chart
    :return:
    """
    return render_template("lineshow.html")


@app.route("/everydaytop5")
def everyday():
    """
    to turn to everyday_top10 scatter
    :return:
    """
    return render_template("everyday_top10.html")


@app.route("/test")
def test():
    """
    to test charts
    :return:
    """
    return render_template("test.html")


@app.route('/register', methods=["POST", "GET"])
def register():
    """
    user register
    :return:
    """
    useremail = request.form.get("userEmail", "")
    username = request.form.get("userName", "")
    userpwd = request.form.get("userPwd", "")
    logging.debug(useremail, username, userpwd)
    if util.useradd(useremail, username, userpwd) == "suc":
        return jsonify({"msg": "success"})
    else:
        return jsonify({"msg": "fail"})


@app.route('/classify', methods=["POST", "GET"])
def get_classify():
    """
    show index page, top10 of soft, game, and speed
    :return:
    """
    try:
        conn, cur = util.condb()

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
            logging.debug("Soft is %s", soft)
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


@app.route("/searchapp", methods=["GET", "POST"])
def search_app():
    if request.method == "GET":
        app_name = request.args.get("app_name")
        logging.debug("App_name is : %s", app_name)
        conn, cur = util.condb()
        cur.execute("SELECT a_picurl, a_name, a_pkgname "
                    "FROM t_apps_basic_united WHERE a_name = %s ORDER BY a_getdate DESC LIMIT 1;", app_name)
        aim_app = cur.fetchall()
        logging.debug("Exact Match! Search result is %s", aim_app)
        if len(aim_app) > 0:
            return jsonify({"msg": "exact match", "apps": aim_app})
        else:
            cur.execute("SELECT a_picurl, a_name, a_pkgname "
                        "FROM t_apps_basic_united WHERE a_name like %s ORDER BY a_getdate DESC;", ("%" + app_name + "%"))
            aim_apps = cur.fetchall()
            logging.debug("Fuzzy Match! Search result is %s", aim_apps)
            return jsonify({"msg": "fuzzy match", "apps": aim_apps})
    else:
        return jsonify({"msg": "wrong request method"})


@app.route("/appdetail", methods=["GET", "POST"])
def show_app_detail():
    pkgname = request.args.get("pkgname")
    conn, cur = util.condb()
    sql = "SELECT a_picurl, a_name, a_pkgname, a_url, a_classify, a_desc FROM t_apps_basic_unite " \
          "WHERE a_pkgname = %s ORDER BY a_getdate DESC LIMIT 1"
    cur.execute(sql, pkgname)
    this_app = (item[0], item[1], item[2], item[3], item[4], item[5] for item in cur.fetchall())

    return render_template("appdetail.html", this_app)


@app.route("/top5")
def get_soft_top5():
    """
    for line chart and radar
    :return:
    """
    conn, cur = util.condb()
    # soft top 5
    cur.execute("SELECT t0.a_pkgname, t0.a_name, date(t0.a_getdate) a_getdate, t0.a_install_sum "
                "FROM t_apps_addi_united t0 "
                "JOIN (SELECT t.a_pkgname FROM t_apps_addi_united t WHERE t.a_softgame = 'soft' AND "
                "DATE(t.a_getdate) = DATE_SUB(CURDATE(), INTERVAL 1 DAY) ORDER BY t.a_install_sum DESC LIMIT 5) t1 ON "
                "t0.a_pkgname = t1.a_pkgname WHERE DATE(t0.a_getdate) "
                "BETWEEN DATE_SUB(LOCALTIME,INTERVAL 7 DAY) AND DATE_SUB(LOCALTIME,INTERVAL 1 DAY);")
    soft_top5 = cur.fetchall()
    soft_dic = {}
    date_install_list = []
    soft_install_disc = {}
    soft_install_list = []
    cur_soft = soft_top5[0]
    soft_dic[cur_soft[2].strftime('%Y-%m-%d')] = cur_soft[3]
    date_install_list.append(soft_dic)

    for soft in soft_top5[1:]:
        soft_dic = {}
        soft_install_disc = {}
        if cur_soft[0] == soft[0]:
            soft_dic[soft[2].strftime('%Y-%m-%d')] = soft[3]
            date_install_list.append(soft_dic)
        else:
            soft_install_disc[cur_soft[1]] = date_install_list
            soft_install_list.append(soft_install_disc)
            cur_soft = soft
            date_install_list = []
            soft_dic[cur_soft[2].strftime('%Y-%m-%d')] = cur_soft[3]
            date_install_list.append(soft_dic)
    soft_install_disc[cur_soft[1]] = date_install_list
    soft_install_list.append(soft_install_disc)
    print(soft_install_list)

    # game top 5
    cur.execute("SELECT t0.a_pkgname, t0.a_name, date(t0.a_getdate) a_getdate, t0.a_install_sum "
                "FROM t_apps_addi_united t0 "
                "JOIN (SELECT t.a_pkgname FROM t_apps_addi_united t WHERE t.a_softgame = 'game' AND "
                "DATE(t.a_getdate) = DATE_SUB(CURDATE(), INTERVAL 1 DAY) ORDER BY t.a_install_sum DESC LIMIT 5) t1 ON "
                "t0.a_pkgname = t1.a_pkgname WHERE DATE(t0.a_getdate) "
                "BETWEEN DATE_SUB(LOCALTIME,INTERVAL 7 DAY) AND DATE_SUB(LOCALTIME,INTERVAL 1 DAY);")
    game_top5 = cur.fetchall()
    game_dic = {}
    date_install_list = []
    game_install_disc = {}
    game_install_list = []
    cur_game = game_top5[0]
    game_dic[cur_game[2].strftime('%Y-%m-%d')] = cur_game[3]
    date_install_list.append(game_dic)

    for game in game_top5[1:]:
        game_dic = {}
        game_install_disc = {}
        if cur_game[0] == game[0]:
            game_dic[game[2].strftime('%Y-%m-%d')] = game[3]
            date_install_list.append(game_dic)
        else:
            game_install_disc[cur_game[1]] = date_install_list
            game_install_list.append(game_install_disc)
            cur_game = game
            date_install_list = []
            game_dic[cur_game[2].strftime('%Y-%m-%d')] = cur_game[3]
            date_install_list.append(game_dic)
    game_install_disc[cur_game[1]] = date_install_list
    game_install_list.append(game_install_disc)
    print(game_install_list)

    return jsonify({"softtop": soft_install_list,
                    "gametop": game_install_list})


@app.route("/appspeed", methods=["GET", "POST"])
def speed_of_days():
    """
    search app install_sum speed for three days top10 for scatter
    :return:
    """
    if request.method == "GET":
        yesterday = (datetime.date.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        day_before_yes = (datetime.date.today() - datetime.timedelta(days=2)).strftime('%Y-%m-%d')
        twodays_before = (datetime.date.today() - datetime.timedelta(days=3)).strftime('%Y-%m-%d')
        conn, cur = util.condb()
        speed_sql = "SELECT a_getdate, a_pkgname, a_name, a_softgame, speed, a_install_sum FROM " \
                    "(SELECT a_getdate, a_pkgname, a_name, a_softgame, speed, a_install_sum FROM " \
                    "(SELECT DATE(t0.a_getdate) a_getdate, t0.a_pkgname a_pkgname, " \
                    "t0.a_name a_name, t0.a_softgame a_softgame, t0.a_install_sum - t1.a_install_sum speed, " \
                    "t0.a_install_sum a_install_sum " \
                    "FROM t_apps_addi_united t0 JOIN t_apps_addi_united t1 ON t0.a_pkgname = t1.a_pkgname WHERE " \
                    "DATE(t1.a_getdate) = DATE_SUB(DATE(t0.a_getdate), INTERVAL 1 DAY) AND " \
                    "DATE(t0.a_getdate) = %s AND t0.a_softgame = %s " \
                    "GROUP BY DATE(t0.a_getdate), t0.a_install_sum - t1.a_install_sum ORDER BY speed DESC) t LIMIT 10) t2 " \
                    "UNION ALL " \
                    "SELECT a_getdate, a_pkgname, a_name, a_softgame, speed, a_install_sum FROM " \
                    "(SELECT a_getdate, a_pkgname, a_name, a_softgame, speed, a_install_sum FROM " \
                    "(SELECT DATE(t0.a_getdate) a_getdate, t0.a_pkgname a_pkgname, t0.a_name a_name, " \
                    "t0.a_softgame a_softgame, t0.a_install_sum - t1.a_install_sum speed, t0.a_install_sum a_install_sum " \
                    "FROM t_apps_addi_united t0 " \
                    "JOIN t_apps_addi_united t1 ON t0.a_pkgname = t1.a_pkgname " \
                    "WHERE DATE(t1.a_getdate) = DATE_SUB(DATE(t0.a_getdate),INTERVAL 1 DAY) AND " \
                    "DATE(t0.a_getdate) = %s AND t0.a_softgame = %s " \
                    "GROUP BY DATE(t0.a_getdate), t0.a_install_sum - t1.a_install_sum ORDER BY speed DESC) t LIMIT 10) t3 " \
                    "UNION ALL " \
                    "SELECT a_getdate, a_pkgname, a_name, a_softgame, speed, a_install_sum FROM " \
                    "(SELECT a_getdate, a_pkgname, a_name, a_softgame, speed, a_install_sum FROM " \
                    "(SELECT DATE(t0.a_getdate) a_getdate, t0.a_pkgname a_pkgname, t0.a_name a_name, " \
                    "t0.a_softgame a_softgame, t0.a_install_sum - t1.a_install_sum speed, t0.a_install_sum a_install_sum " \
                    "FROM t_apps_addi_united t0 " \
                    "JOIN t_apps_addi_united t1 ON t0.a_pkgname = t1.a_pkgname WHERE " \
                    "DATE(t1.a_getdate) = DATE_SUB( DATE(t0.a_getdate), INTERVAL 1 DAY) AND " \
                    "DATE(t0.a_getdate) = %s AND t0.a_softgame = %s GROUP BY DATE(t0.a_getdate), " \
                    "t0.a_install_sum - t1.a_install_sum ORDER BY speed DESC) t LIMIT 10 ) t4"

        cur.execute(speed_sql, (str(yesterday), "soft", str(day_before_yes), "soft", str(twodays_before), "soft"))
        soft_speed = cur.fetchall()
        samedate_soft_list = []
        soft_list = []
        cur_soft = soft_speed[0]
        i_cur_soft = [cur_soft[4], cur_soft[4]/cur_soft[5], cur_soft[5], cur_soft[2], str(cur_soft[0])]
        logging.debug("to string :%s", i_cur_soft)
        samedate_soft_list.append(i_cur_soft)
        for soft in soft_speed[1:]:
            i_soft = [soft[4], soft[4]/soft[5], soft[5], soft[2], str(soft[0])]
            if i_cur_soft[4] == i_soft[4]:
                samedate_soft_list.append(i_soft)
                i_cur_soft = i_soft
            else:
                soft_list.append(samedate_soft_list)
                samedate_soft_list = []
                i_cur_soft = i_soft
                samedate_soft_list.append(i_cur_soft)
        soft_list.append(samedate_soft_list)

        cur.execute(speed_sql, (str(yesterday), "game", str(day_before_yes), "game", str(twodays_before), "game"))
        game_speed = cur.fetchall()
        samedate_game_list = []
        game_list = []
        cur_game = game_speed[0]
        i_cur_game = [cur_game[4], cur_game[4]/cur_game[5], cur_game[5], cur_game[2], str(cur_game[0])]
        samedate_game_list.append(i_cur_game)
        for game in game_speed[1:]:
            i_game = [game[4], game[4]/game[5], game[5], game[2], str(game[0])]
            if i_cur_game[4] == i_game[4]:
                samedate_game_list.append(i_game)
                i_cur_game = i_game
            else:
                game_list.append(samedate_game_list)
                samedate_game_list = []
                i_cur_game = i_game
                samedate_game_list.append(i_cur_game)
        game_list.append(samedate_game_list)

        logging.debug("soft_list: %s", soft_list)
        logging.debug("game_list: %s", game_list)
        return jsonify({"softdata": soft_list, "gamedata": game_list})
    else:
        logging.error("Request method is wrong")
        return jsonify({"status": "failed"})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
