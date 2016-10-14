# _*_ coding: utf-8 _*_

import pymysql
import logging
from urllib import request
from z_sql import *

# ----server----
SDB_HOST = "101.200.174.172"
SDB_DB = "data_apps"
SDB_USER = "dba_apps"
SDB_PWD = "mimadba_apps"
SDB_CHARSET = "utf8"


def condb():
    """
    connect to db
    :return:
    """
    conn = pymysql.connect(host=SDB_HOST, user=SDB_USER, password=SDB_PWD, db=SDB_DB, charset=SDB_CHARSET)
    cur = conn.cursor()
    conn.autocommit(1)
    return conn, cur


def install_softgame(soft_game):
    """
    show index page, top10 of soft, game, and speed
    :return:
    """
    conn, cur = condb()
    try:
        # yesterday soft TOP10
        sql = SQL_YS_INSTALL_TOP_SOFTGAME
        cur.execute(sql, soft_game)
        top_soft = cur.fetchall()
        if top_soft:
            dict_rank_soft = [(item[0], item[1], item[2], int(item[3])) for item in top_soft]
            dict_rank_soft = {"rankinfo_" + soft_game : dict_rank_soft}

            # save pic of topsoft
            # i = 0
            # for soft in top_soft:
            #     logging.debug("Soft is %s", soft)
            #     url = str(soft[2])
            #     path = "/static/pic/top" + soft_game + str(i) + ".jpg"
            #     logging.debug("path is %s", path)
            #     data = request.urlopen(url).read()
            #     f = open(path, "wb")
            #     f.write(data)
            #     i += 1
            #     f.close()
            return dict_rank_soft
        else:
            return "no data"
    except Exception as ex:
        logging.error("Install soft_game error %s", ex)
        return "error"


def speed_softgame(soft_game):
    conn, cur = condb()
    try:
        sql = SQL_YS_SPEED_TOP_SOGTGAME
        cur.execute(sql, soft_game)
        conn.commit()
        speed_soft = cur.fetchall()
        if speed_soft:
            dict_speed_soft = [(item[0], item[1], item[2], item[3], str(item[4]) + "%",
                                str(item[5]).replace("b", "").replace("'", "")) for item in speed_soft]
            dict_speed_soft = {"speed_" + soft_game: dict_speed_soft}

            # save pic of speedsoft
            # i = 0
            # for soft in speed_soft:
            #     logging.debug("Game is %s", soft)
            #     url = str(soft[1])
            #     path = "/static/pic/speed" + soft_game + str(i) + ".jpg"
            #     logging.debug("path is %s", path)
            #     data = request.urlopen(url).read()
            #     f = open(path, "wb")
            #     f.write(data)
            #     i += 1
            #     f.close()
            return dict_speed_soft
        else:
            return "no data"
    except Exception as ex:
        logging.error("Speed softgame error: %s", ex)
        return "error"


def speed_top5_current(soft_game):
    """
    for line chart and radar
    :return:
    """
    conn, cur = condb()
    # current 10 day's speed of yesterday soft speed top5
    sql = SQL_CRNT_SPEED_TOP_SOFTGAME
    try:
        cur.execute(sql, soft_game)
        app_top10 = cur.fetchall()
        if app_top10:
            app_dic = {}
            date_speed_list = []
            app_speed_disc = {}
            app_speed_list = []
            cur_app = app_top10[0]
            app_dic[cur_app[2].strftime('%Y-%m-%d')] = cur_app[3]
            date_speed_list.append(app_dic)

            for app in app_top10[1:]:
                app_dic = {}
                app_speed_disc = {}
                if cur_app[0] == app[0]:
                    app_dic[app[2].strftime('%Y-%m-%d')] = app[3]
                    date_speed_list.append(app_dic)
                else:
                    app_speed_disc[cur_app[1]] = date_speed_list
                    app_speed_list.append(app_speed_disc)
                    cur_app = app
                    date_speed_list = []
                    app_dic[cur_app[2].strftime('%Y-%m-%d')] = cur_app[3]
                    date_speed_list.append(app_dic)
            app_speed_disc[cur_app[1]] = date_speed_list
            app_speed_list.append(app_speed_disc)
            return app_speed_list
        else:
            return "no data"
    except Exception as ex:
        logging.error("Speed current error: %s", ex)
        return "error"


def install_softgame_current(soft_game):
    """
    for line chart and radar
    :return:
    """
    conn, cur = condb()
    # current 10 day's install of yesterday soft install top10
    sql = SQL_CRNT_INSTALL_TOP_SOFTGAME
    try:
        cur.execute(sql, soft_game)
        soft_top10 = cur.fetchall()
        if soft_top10:
            soft_dic = {}
            date_install_list = []
            soft_install_disc = {}
            soft_install_list = []
            cur_soft = soft_top10[0]
            soft_dic[cur_soft[2].strftime('%Y-%m-%d')] = cur_soft[3]
            date_install_list.append(soft_dic)

            for soft in soft_top10[1:]:
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
            return soft_install_list
        else:
            return "no data"
    except Exception as ex:
        logging.error("Install softgame error: %s", ex)
        return "error"


def speed_softgame_current(soft_game):
    """
    for line chart and radar
    :return:
    """
    conn, cur = condb()
    # current 10 day's speed of yesterday soft speed top10
    sql = SQL_CRNT_SPEED_TOP_SOFTGAME
    try:
        cur.execute(sql, soft_game)
        game_top10 = cur.fetchall()
        if game_top10:
            game_dic = {}
            date_speed_list = []
            game_speed_disc = {}
            game_speed_list = []
            cur_game = game_top10[0]
            game_dic[cur_game[2].strftime('%Y-%m-%d')] = cur_game[3]
            date_speed_list.append(game_dic)

            for game in game_top10[1:]:
                game_dic = {}
                game_speed_disc = {}
                if cur_game[0] == game[0]:
                    game_dic[game[2].strftime('%Y-%m-%d')] = game[3]
                    date_speed_list.append(game_dic)
                else:
                    game_speed_disc[cur_game[1]] = date_speed_list
                    game_speed_list.append(game_speed_disc)
                    cur_game = game
                    date_speed_list = []
                    game_dic[cur_game[2].strftime('%Y-%m-%d')] = cur_game[3]
                    date_speed_list.append(game_dic)
            game_speed_disc[cur_game[1]] = date_speed_list
            game_speed_list.append(game_speed_disc)
            return game_speed_list
        else:
            return "no data"
    except Exception as ex:
        logging.error("Speed current error: %s", ex)
        return "error"


def install_classify(classify):
    """
    show index page, top10 of soft, game, and speed
    :return:
    """
    conn, cur = condb()
    try:
        # yesterday soft TOP10
        sql = SQL_YS_INSTALL_TOP_CLASSIFY
        cur.execute(sql, classify)
        top_soft = cur.fetchall()
        if top_soft:
            dict_rank_soft = [(item[0], item[1], item[2], int(item[3])) for item in top_soft]
            dict_rank_soft = {"rankinfo_classify": dict_rank_soft}

            # save pic of topsoft
            # i = 0
            # for soft in top_soft:
            #     logging.debug("Soft is %s", soft)
            #     url = str(soft[2])
            #     path = "static/pic/topclassify" + str(i) + ".jpg"
            #     logging.debug("path is %s", path)
            #     data = request.urlopen(url).read()
            #     f = open(path, "wb")
            #     f.write(data)
            #     i += 1
            #     f.close()
            return dict_rank_soft
        else:
            return "no data"
    except Exception as ex:
        logging.error("Install soft_game error %s", ex)
        return "error"


def speed_classify(classify):
    conn, cur = condb()
    try:
        sql = SQL_YS_SPEED_TOP_CLASSIFY
        cur.execute(sql, classify)
        conn.commit()
        speed_soft = cur.fetchall()
        if speed_soft:
            dict_speed_soft = [(item[0], item[1], item[2], item[3], str(item[4]) + "%",
                                str(item[5]).replace("b", "").replace("'", "")) for item in speed_soft]
            dict_speed_soft = {"speed_classify": dict_speed_soft}

            # save pic of speedsoft
            # i = 0
            # for soft in speed_soft:
            #     logging.debug("Game is %s", soft)
            #     url = str(soft[1])
            #     path = "static/pic/speedclassify" + str(i) + ".jpg"
            #     logging.debug("path is %s", path)
            #     data = request.urlopen(url).read()
            #     f = open(path, "wb")
            #     f.write(data)
            #     i += 1
            #     f.close()
            return dict_speed_soft
        else:
            return "no data"
    except Exception as ex:
        logging.error("Speed softgame error: %s", ex)
        return "error"


def search_app(app_name):
    conn, cur = condb()
    sql_basic = SQL_SEARCH_APP_NAME
    sql_install = SQL_SEARCH_APP_INSTALL_NAME
    sql_rate = SQL_SEARCH_APP_RATE_NAME
    try:
        cur.execute(sql_basic, (app_name, app_name))
        app_info = cur.fetchall()
        cur.execute(sql_install, app_name)
        app_install = cur.fetchall()
        cur.execute(sql_rate, app_name)
        app_rate = cur.fetchall()
        if app_info and app_install and app_rate:
            list_app_info = [(item[0], item[1], item[2], item[3], item[4].strftime("%Y-%m-%d"), item[5], item[6], item[7]) for item in app_info]
            list_app_install = [(item[0].strftime("%Y-%m-%d"), item[1]) for item in app_install]
            list_app_rate = [(item[0].strftime("%Y-%m-%d"), item[1]) for item in app_rate]
            dict_app_info = {"app_info": list_app_info}
            dict_app_install = {"app_install": list_app_install}
            dict_app_rate = {"app_rate": list_app_rate}
            print(dict_app_rate)
            return dict_app_info, dict_app_install, dict_app_rate
        else:
            return "no date"
    except Exception as ex:
        logging.error("Search app by name error: %s", ex)
        return "error"


def useradd(useremail, username, userpwd):
    """
    add user to db
    :param useremail:
    :param username:
    :param userpwd:
    :return:
    """
    try:
        conn = pymysql.connect(host="localhost", user="root", password="123", db="my_db", charset="utf8")
        cur = conn.cursor()
        cur.execute("INSERT INTO users (userEmail, userName, userPwd) VALUES (%s, %s, %s)",
                    (useremail, username, userpwd))
        conn.commit()
        return "suc"
    except Exception as e:
        logging.error(Exception, ":", e)
        return "wro"
