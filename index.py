# _*_ coding: utf-8 _*_

from flask import Flask, render_template
from flask import request as flask_request, jsonify
from tag_config.app_tags import *
from z_util import *

logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)


@app.route('/')
def index_rank():
    """
    turn to index page
    :return:
    """
    return render_template('b_index_speed.html')


@app.route("/all/speed")
def softgame():
    """
    turn to app top5 7days line chart
    :return:
    """
    return render_template("ba_rank_line_show.html")


@app.route("/all/speed/req")
def get_speed_top5_current():
    """
    for line chart and radar
    :return:
    """
    # current 10 day's speed of yesterday soft speed top5
    soft_speed_list = speed_top5_current("soft")

    # current 10 day's speed of yesterday game speed top5
    game_speed_list = speed_top5_current("game")

    return jsonify({"softtop5": soft_speed_list[0: 5],
                    "gametop5": game_speed_list[0: 5]})


@app.route('/index/classify')
def index_classify():
    """
    turn to index page
    :return:
    """
    return render_template('c_index_classify.html')


@app.route('/all/classify')
def all_classify():
    """
    turn to index page
    :return:
    """
    return render_template('ca_classify_tbl_show.html')


@app.route('/all/classify/req', methods=["POST", "GET"])
def get_classify():
    """
    show index page, top10 of soft, game, and speed
    :return:
    """
    # yesterday install soft TOP10]
    dict_rank_soft = install_softgame("soft")

    # yesterday install game TOP10
    dict_rank_game = install_softgame("game")

    # yesterday speed soft TOP10
    dict_speed_soft = speed_softgame("soft")

    # yesterday speed game TOP10
    dict_speed_game = speed_softgame("game")

    return jsonify(soft_classify, game_classify, dict_rank_soft, dict_rank_game, dict_speed_soft, dict_speed_game)


@app.route("/install/soft/current")
def install_softcurrent():
    """
    turn to current 10 day's line chart of yesterday soft install top 10
    :return:
    """
    return render_template("cb_soft_install_crnt_line_show.html")


@app.route("/install/soft/current/req")
def get_install_soft_current():
    """
    for line chart and radar
    :return:
    """
    soft_install_list = install_softgame_current("soft")

    return jsonify({"softtop5": soft_install_list[0: 5],
                    "softtop10": soft_install_list[5: 10]})


@app.route("/speed/soft/current")
def speed_softcurrent():
    """
    turn to current 10 day's line chart of yesterday soft speed top 10
    :return:
    """
    return render_template("cc_soft_speed_crnt_line_show.html")


@app.route("/speed/soft/current/req")
def get_speed_soft_current():
    """
    for line chart and radar
    :return:
    """
    soft_speed_list = speed_softgame_current("soft")

    return jsonify({"softtop5": soft_speed_list[0: 5],
                    "softtop10": soft_speed_list[5: 10]})


@app.route("/install/game/current")
def install_gamecurrent():
    """
    turn to current 10 day's line chart of yesterday soft install top 10
    :return:
    """
    return render_template("cd_game_install_crnt_line_show.html")


@app.route("/install/game/current/req")
def get_install_game_current():
    """
    for line chart and radar
    :return:
    """
    game_install_list = install_softgame_current("game")

    return jsonify({"gametop5": game_install_list[0: 5],
                    "gametop10": game_install_list[5: 10]})


@app.route("/speed/game/current")
def speed_gamecurrent():
    """
    turn to current 10 day's line chart of yesterday game speed top 10
    :return:
    """
    return render_template("ce_game_speed_crnt_line_show.html")


@app.route("/speed/game/current/req")
def get_speed_game_current():
    """
    for line chart and radar
    :return:
    """
    game_speed_list = speed_softgame_current("game")

    return jsonify({"gametop5": game_speed_list[0: 5],
                    "gametop10": game_speed_list[5: 10]})


@app.route('/index/search')
def index_search():
    """
    turn to index page
    :return:
    """
    return render_template('d_index_search.html')


@app.route("/everydaytop5")
def everyday():
    """
    to turn to everyday_top10 scatter
    :return:
    """
    return render_template("z_everyday_top10.html")


@app.route("/test")
def test():
    """
    to test charts
    :return:
    """
    return render_template("z_test.html")


@app.route('/register', methods=["POST", "GET"])
def register():
    """
    user register
    :return:
    """
    useremail = flask_request.form.get("userEmail", "")
    username = flask_request.form.get("userName", "")
    userpwd = flask_request.form.get("userPwd", "")
    logging.debug(useremail, username, userpwd)
    if useradd(useremail, username, userpwd) == "suc":
        return jsonify({"msg": "success"})
    else:
        return jsonify({"msg": "fail"})


@app.route("/searchapp", methods=["GET", "POST"])
def search_app():
    if flask_request.method == "GET":
        app_name = flask_request.args.get("app_name")
        logging.debug("App_name is : %s", app_name)
        conn, cur = condb()
        cur.execute("SELECT a_picurl, a_name, a_pkgname "
                    "FROM t_apps_basic_united WHERE a_name = %s ORDER BY a_getdate DESC LIMIT 1;", app_name)
        aim_app = cur.fetchall()
        if len(aim_app) > 0:
            logging.debug("Exact Match! Search result is %s", aim_app)
            return jsonify({"msg": "exact match", "apps": aim_app})
        else:
            cur.execute("SELECT a_picurl, a_name, a_pkgname "
                        "FROM t_apps_basic_united WHERE a_name like %s ORDER BY a_getdate DESC;",
                        ("%" + app_name + "%"))
            aim_apps = cur.fetchall()
            logging.debug("Fuzzy Match! Search result is %s", aim_apps)
            return jsonify({"msg": "fuzzy match", "apps": aim_apps})
    else:
        return jsonify({"msg": "wrong request method"})


@app.route("/appdetail", methods=["GET", "POST"])
def show_app_detail():
    pkgname = flask_request.args.get("pkgname")
    conn, cur = condb()
    sql = "SELECT a_picurl, a_name, a_pkgname, a_url, a_classify, a_description FROM t_apps_basic_united " \
          "WHERE a_pkgname = %s ORDER BY a_getdate DESC LIMIT 1"
    cur.execute(sql, pkgname)
    this_app = [(item[0], item[1], item[2], item[3], item[4], item[5]) for item in cur.fetchall()]
    return jsonify(this_app)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", threaded=True)
