# _*_ coding: utf-8 _*_

import pymysql
import logging

# ----server----
SDB_HOST = "101.200.174.172"
SDB_DB = "data_apps"
SDB_USER = "dba_apps"
SDB_PWD = "mimadba_apps"
SDB_CHARSET = "utf8"

logging.basicConfig(level=logging.WARN)


SQL_YS_INSTALL_SOFTGAME = """INSERT INTO t_apps_speed (a_getdate, a_pkgname, a_name, a_tdinstall,
                                                    a_url, a_picurl, a_version, a_like, a_comment,
                                                    a_score, a_softgame, a_source, a_isspeed)
                                      SELECT
                                          a_getdate, a_pkgname, a_name,
                                          a_install, a_url, a_picurl,
                                          a_version, a_like, a_comment,
                                          a_score, a_softgame, a_source, 0
                                      FROM t_apps_additional_new
                                      WHERE
                                          a_softgame = %s AND
                                          DATE(a_getdate) = DATE(DATE_SUB(LOCALTIME,INTERVAL 1 DAY)) AND
                                          a_source = "yyb" ORDER BY a_install DESC LIMIT 10;"""

SQL_YS_RATE_SOFTGAME = """INSERT INTO t_apps_speed (a_pkgname, a_name, a_url, a_picurl, a_updatedate, a_version,
                                        a_ysinstall, a_tdinstall, a_rateinstall,
                                        a_like, a_comment, a_score, a_softgame, a_source, a_getdate, a_isspeed)
                        SELECT t0.a_pkgname, t0.a_name, t0.a_url, t0.a_picurl, t0.a_updatedate, t0.a_version,
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


def insert_speed(soft_game):
    conn = pymysql.connect(host=SDB_HOST, db=SDB_DB, user=SDB_USER, passwd=SDB_PWD, chartset=SDB_CHARSET)
    cur = conn.cursor()
    conn.autocommit(1)
    sql_install = SQL_YS_INSTALL_SOFTGAME
    sql_rate = SQL_YS_RATE_SOFTGAME
    try:
        cur.execute(sql_rate, soft_game)
        cur.execute(sql_install, soft_game)
    except Exception as ex:
        logging.error("Insert speed error: %s", ex)

if __name__ == "__main__":
    insert_speed("soft")
    insert_speed("game")
