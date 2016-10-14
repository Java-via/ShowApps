# _*_ coding: utf-8 _*_

import pymysql
import logging
from tag_config.app_tags import *

# ----server----
SDB_HOST = "101.200.174.172"
SDB_DB = "data_apps"
SDB_USER = "dba_apps"
SDB_PWD = "mimadba_apps"
SDB_CHARSET = "utf8"

logging.basicConfig(level=logging.WARN)


SQL_YS_INSTALL_SOFTGAME = """INSERT INTO t_apps_speed (a_getdate, a_pkgname, a_name, a_classify, a_tdinstall,
                                                    a_url, a_picurl, a_version, a_like, a_comment,
                                                    a_score, a_softgame, a_source, a_isspeed)
                                      SELECT
                                          a_getdate, a_pkgname, a_name, "综合",
                                          a_install, a_url, a_picurl,
                                          a_version, a_like, a_comment,
                                          a_score, a_softgame, a_source, 0
                                      FROM t_apps_additional_new
                                      WHERE
                                          a_softgame = %s AND
                                          DATE(a_getdate) = DATE(DATE_SUB(LOCALTIME,INTERVAL 1 DAY)) AND
                                          a_source = "yyb" ORDER BY a_install DESC LIMIT 10;"""

SQL_YS_RATE_SOFTGAME = """INSERT INTO t_apps_speed (a_pkgname, a_name, a_classify, a_url, a_picurl, a_updatedate, a_version,
                                        a_ysinstall, a_tdinstall, a_rateinstall,
                                        a_like, a_comment, a_score, a_softgame, a_source, a_getdate, a_isspeed)
                        SELECT t0.a_pkgname, t0.a_name, "综合", t0.a_url, t0.a_picurl, t0.a_updatedate, t0.a_version,
                              t1.a_install AS ysinstall, t0.a_install AS tdinstall,
                              1.0*(t0.a_install-t1.a_install)/t1.a_install AS rate,
                              t0.a_like, t0.a_comment, t0.a_score, t0.a_softgame, t0.a_source, t0.a_getdate AS td, 1
                        FROM
                              t_apps_additional_new t1,
                              (
                                  SELECT
                                      a_pkgname, a_name, a_url, a_picurl, a_updatedate, a_version,
                                      a_like, a_comment, a_score, a_softgame, a_source, a_getdate, a_install
                                  FROM
                                      t_apps_additional_new
                                  WHERE
                                      a_source = "yyb" AND a_softgame = %s AND
                                      DATE(a_getdate) BETWEEN DATE(DATE_SUB(LOCALTIME,INTERVAL 10 DAY))
                                                      AND DATE(DATE_SUB(LOCALTIME,INTERVAL 1 DAY))
                              ) t0
                        WHERE
                              t1.a_source = "yyb" AND t1.a_pkgname = t0.a_pkgname AND
                              DATE(t1.a_getdate) = DATE_SUB(t0.a_getdate,INTERVAL 1 DAY) ORDER BY rate DESC LIMIT 10;"""

SQL_YS_INSTALL_CLASSIFY = """INSERT INTO t_apps_speed (a_pkgname, a_name, a_classify, a_url,
                                                      a_picurl, a_updatedate, a_version,
                                                      a_tdinstall, a_like, a_comment, a_score, a_softgame,
                                                      a_source, a_getdate, a_isspeed )
                            (SELECT
                                            t2.a_pkgname, t2.a_name, t1.a_classify, t2.a_url,
                                            t2.a_picurl, t2.a_updatedate, t2.a_version,
                                            t2.a_install, t2.a_like, t2.a_comment, t2.a_score, t2.a_softgame,
                                            t2.a_source, t2.a_getdate, 0
                            FROM t_apps_additional_new t2, (SELECT a_pkgname, a_classify FROM t_apps_basic_new
                                                              WHERE a_source = "yyb" AND a_classify = %s) t1
                            WHERE t2.a_source = "yyb" AND t2.a_pkgname = t1.a_pkgname AND
                                  DATE(t2.a_getdate) = DATE(DATE_SUB(LOCALTIME,INTERVAL 1 DAY))
                            ORDER BY t2.a_install DESC LIMIT 10); """


SQL_YS_RATE_CLASSIFY = """INSERT INTO t_apps_speed (a_pkgname, a_name, a_classify, a_url,
                                                    a_picurl, a_updatedate, a_version,
                                                    a_ysinstall, a_tdinstall, a_rateinstall,
                                                    a_like, a_comment, a_score, a_softgame,
                                                    a_source, a_getdate, a_isspeed )
                                      (SELECT
                                            t2.a_pkgname, t2.a_name, t1.a_classify, t2.a_url,
                                            t2.a_picurl, t2.a_updatedate, t2.a_version,
                                            t3.a_install AS ysinstall, t2.a_install AS tdinstall,
                                            1.0*(t2.a_install-t3.a_install)/t3.a_install AS rateinstall,
                                            t2.a_like, t2.a_comment, t2.a_score, t2.a_softgame,
                                            t2.a_source, t2.a_getdate, 1
                                      FROM t_apps_additional_new t3, t_apps_additional_new t2,
                                          (SELECT a_pkgname, a_classify FROM t_apps_basic_new
                                            WHERE a_source = "yyb" AND a_classify = %s ) t1
                                      WHERE t2.a_source = "yyb" AND t2.a_pkgname = t1.a_pkgname AND
                                            DATE(t2.a_getdate) = DATE(DATE_SUB(LOCALTIME,INTERVAL 1 DAY)) AND
                                            t3.a_source = "yyb" AND t3.a_pkgname = t2.a_pkgname AND
                                            t3.a_getdate = DATE_SUB(t2.a_getdate,INTERVAL 1 DAY)
                                      ORDER BY rateinstall DESC LIMIT 10);"""


def insert_install_and_speed(soft_game):
    conn = pymysql.connect(host=SDB_HOST, db=SDB_DB, user=SDB_USER, passwd=SDB_PWD, charset=SDB_CHARSET)
    cur = conn.cursor()
    conn.autocommit(1)
    sql_install = SQL_YS_INSTALL_SOFTGAME
    sql_rate = SQL_YS_RATE_SOFTGAME
    try:
        print("INSERT RATE BEGIN")
        cur.execute(sql_rate, soft_game)
        print("INSERT RATE END")
        print("INSERT INSTALL BEGIN")
        cur.execute(sql_install, soft_game)
        print("INSERT INSTALL END")
        return
    except Exception as ex:
        logging.error("Insert speed error: %s", ex)


def insert_classify():
    conn = pymysql.connect(host=SDB_HOST, db=SDB_DB, user=SDB_USER, passwd=SDB_PWD, charset=SDB_CHARSET)
    cur = conn.cursor()
    conn.autocommit(1)
    sql_install_classify = SQL_YS_INSTALL_CLASSIFY
    sql_rate_classify = SQL_YS_RATE_CLASSIFY
    for key in config_yyb:
        try:
            print("INSERT INSTALL BEGIN: %s" % key)
            cur.execute(sql_install_classify, key)
            print("INSERT INSTALL END: %s" % key)
            print("INSERT RATE BEGIN: %s" % key)
            cur.execute(sql_rate_classify, key)
            print("INSERT RATE END: %s" % key)
        except Exception as ex:
            print("ERROR :", key, ex)

if __name__ == "__main__":
    print("install_and_speed_soft start")
    insert_install_and_speed("soft")
    print("install_and_speed_game start")
    insert_install_and_speed("game")
    print("rate_classify start")
    insert_classify()
    print("end")
