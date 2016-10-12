# _*_ coding: utf-8 _*_


# yesterday install top10
SQL_YS_INSTALL_TOP_SOFTGAME = """SELECT
                                    a_pkgname, a_name, a_picurl, a_install
                                  FROM
                                    t_apps_speed
                                  WHERE
                                    DATE(a_getdate) = DATE(DATE_SUB(LOCALTIME,INTERVAL 1 DAY)) AND a_isspeed = 0 AND
                                    a_softgame = %s ORDER BY a_id;"""

# yesterday speed top10
SQL_YS_SPEED_TOP_SOGTGAME = """SELECT a_getdate, a_picurl, a_pkgname, a_name, a_install FROM t_apps_speed
                                WHERE DATE(a_getdate) = DATE(DATE_SUB(LOCALTIME,INTERVAL 1 DAY)) AND a_isspeed = 1 AND
                                a_softgame = %s ORDER BY a_id;"""

# current 10 day's speed of yesterday speed top10
SQL_CRNT_SPEED_TOP_SOFTGAME = """SELECT t1.a_pkgname, t1.a_name, t2.a_getdate, t1.a_install-t2.a_install AS a_subinstall
                                  FROM
                                  t_apps_additional_new t2,
                                  t_apps_additional_new t1,
                                  (
                                    SELECT a_pkgname
                                    FROM t_apps_speed
                                    WHERE a_softgame = %s AND
                                        DATE(a_getdate) = DATE(DATE_SUB(LOCALTIME,INTERVAL 1 DAY)) ORDER BY a_id
                                  ) t0
                                  WHERE
                                  t1.a_pkgname = t0.a_pkgname AND t2.a_pkgname = t0.a_pkgname AND
                                  t1.a_source = "yyb" AND t2.a_source = "yyb" AND
                                  t1.a_getdate BETWEEN DATE(DATE_SUB(LOCALTIME,INTERVAL 11 DAY)) AND
                                  DATE(DATE_SUB(LOCALTIME,INTERVAL 1 DAY)) AND
                                  t2.a_getdate = DATE_SUB(t1.a_getdate,INTERVAL 1 DAY);"""

# current 10 day's install of yesterday install top10
SQL_CRNT_INSTALL_TOP_SOFTGAME = """SELECT t1.a_pkgname, t1.a_name, t1.a_getdate, t1.a_install
                                    FROM
                                        t_apps_additional_new t1,
                                        (
                                          SELECT a_pkgname
                                          FROM
                                              t_apps_speed
                                          WHERE
                                              a_isspeed = 0 AND a_softgame = %s AND
                                              DATE(a_getdate) = DATE(DATE_SUB(LOCALTIME,INTERVAL 1 DAY)) ORDER BY a_id
                                        ) t0
                                    WHERE t1.a_pkgname = t0.a_pkgname AND
                                          t1.a_source = "yyb" AND
                                          t1.a_getdate BETWEEN DATE(DATE_SUB(LOCALTIME,INTERVAL 10 DAY)) AND DATE(DATE_SUB(LOCALTIME,INTERVAL 1 DAY));"""
