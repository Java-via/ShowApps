# _*_ coding: utf-8 _*_

import pymysql
from tag_config.app_tags import *

db_host = "127.0.0.1"
db_user = "root"
db_pwd = "123"
db_database = "app_db"

sql = "UPDATE t_apps SET a_category = '%s' WHERE a_pkgname = '%s'"
sql_360 = "SELECT a_pkgname, a_classify FROM t_apps WHERE a_source='360';"
sql_baidu = "SELECT a_pkgname, a_classify FROM t_apps WHERE a_source='baidu';"
sql_wdj = "SELECT a_pkgname, a_classify FROM t_apps WHERE a_source='wdj';"
sql_yyb = "SELECT a_pkgname, a_classify FROM t_apps WHERE a_source='yyb';"


class Soft(object):
    def __init__(self, soft_socal, soft_map, soft_ecno, soft_video, soft_pho, soft_heal, soft_baby,
                 soft_news, soft_office, soft_life, soft_sys):
        self.soft_socal = soft_socal

        self.soft_map = soft_map
        self.sofe_ecno = soft_ecno

        self.soft_video = soft_video
        self.soft_pho = soft_pho

        self.soft_heal = soft_heal
        self.soft_baby = soft_baby

        self.soft_news = soft_news
        self.soft_office = soft_office

        self.soft_life = soft_life
        self.soft_sys = soft_sys


class Game(object):
    def __init__(self, game_child, game_relas, game_jewels, game_run, game_chess, game_pe, game_fire, game_guard,
                 game_playing, game_bussiness, game_net, game_simulation):
        self.game_child = game_child
        self.game_relas = game_relas
        self.game_jewels = game_jewels
        self.game_run = game_run

        self.game_chess = game_chess
        self.game_pe = game_pe

        self.game_fire = game_fire
        self.game_guard = game_guard
        self.game_playing = game_playing
        self.game_bussiness = game_bussiness

        self.game_net = game_net
        self.game_simulation = game_simulation


soft_basic = Soft("社交通讯", "地图旅游", "理财购物", "影音播放", "拍摄美化", "运动健康", "丽人母婴", "资讯阅读",
                  "办公学习", "生活实用", "系统工具")


def category_360():
    dict = {}
    conn = pymysql.connect(host=db_host, user=db_user, passwd=db_pwd, db=db_database)
    cur = conn.cursor()
    cur.execute(sql_360)
    sql_360_update = ""
    for r in cur:
        print(r["a_pkgname"], r["a_classify"])
        dict[r["a_pkgname"]] = r["a_classify"]
        for key in soft_classify:
            for tag in soft_classify[key]:
                if r["a_classify"] in tag:
                    dict[r["a_pkgname"]] = key
        sql_360_update += "UPDATE t_apps SET a_category = %s WHERE a_pkgname = %s;" \
                          % (dict[r["a_pkgname"]], r["a_pkgname"])
    cur.execute(sql_360_update)


def category_baidu():
    dict = {}
    conn = pymysql.connect(host=db_host, user=db_user, passwd=db_pwd, db=db_database, charset="utf8")
    cur = conn.cursor()
    cur.execute(sql_baidu)
    sql_baidu_update = ""

    for r in cur.fetchall():
        # print(r[0], str(r[1]))
        dict[r[0]] = r[1]

        for key in soft_classify:

            for tag in soft_classify[key]:

                if tag in r[1]:
                    dict[r[0]] = key
                    print("key=", key)
                    # print("dict=", dict[r[0]])
                    break
                break
            break
        print("dict=", dict[r[0]])
        sql_baidu_update = "UPDATE t_apps SET a_category = '%s' WHERE a_pkgname = '%s' AND a_source = 'baidu';" % (dict[r[0]], r[0])
        print(sql_baidu_update)
        cur.execute(sql_baidu_update)


def category_wdj():
    dict = {}
    conn = pymysql.connect(host=db_host, user=db_user, passwd=db_pwd, db=db_database)
    cur = conn.cursor()
    cur.execute(sql_wdj)
    sql_wdj_update = ""
    for r in cur:
        print(r["a_pkgname"], r["a_classify"])
        dict[r["a_pkgname"]] = r["a_classify"]
        for key in soft_classify:
            for tag in soft_classify[key]:
                if r["a_classify"] in tag:
                    dict[r["a_pkgname"]] = key
        sql_wdj_update += "UPDATE t_apps SET a_category = %s WHERE a_pkgname = %s;" \
                          % (dict[r["a_pkgname"]], r["a_pkgname"])
    cur.execute(sql_wdj_update)


def category_yyb():
    dict = {}
    conn = pymysql.connect(host=db_host, user=db_user, passwd=db_pwd, db=db_database)
    cur = conn.cursor()
    cur.execute(sql_yyb)
    sql_yyb_update = ""
    for r in cur:
        print(r["a_pkgname"], r["a_classify"])
        dict[r["a_pkgname"]] = r["a_classify"]
        for key in soft_classify:
            for tag in soft_classify[key]:
                if r["a_classify"] in tag:
                    dict[r["a_pkgname"]] = key
        sql_yyb_update += "UPDATE t_apps SET a_category = %s WHERE a_pkgname = %s;" \
                          % (dict[r["a_pkgname"]], r["a_pkgname"])
    cur.execute(sql_yyb_update)


if __name__ == "__main__":
    category_baidu()
