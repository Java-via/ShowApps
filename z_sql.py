# _*_ coding: utf-8 _*_


# yesterday install top10 softgame
SQL_YS_INSTALL_TOP_SOFTGAME = """SELECT
                                    a_pkgname, a_name, a_picurl, a_tdinstall
                                  FROM
                                    t_apps_speed
                                  WHERE
                                    DATE(a_getdate) = DATE(DATE_SUB(LOCALTIME,INTERVAL 5 DAY)) AND a_isspeed = 0 AND
                                    a_classify = "综合" AND
                                    a_softgame = %s ORDER BY a_id;"""

# yesterday speed top10 softgame
SQL_YS_SPEED_TOP_SOGTGAME = """SELECT a_getdate, a_picurl, a_pkgname, a_name,
                                      ROUND(a_rateinstall*100,2), CONCAT(a_ysinstall," --> ",a_tdinstall) FROM t_apps_speed
                                WHERE DATE(a_getdate) = DATE(DATE_SUB(LOCALTIME,INTERVAL 5 DAY)) AND a_isspeed = 1 AND
                                      a_classify = "综合" AND
                                      a_softgame = %s ORDER BY a_id;"""

# current 10 day's speed of yesterday speed top10 softgame
SQL_CRNT_SPEED_TOP_SOFTGAME = """SELECT t1.a_pkgname, t1.a_name, t1.a_getdate, CAST((t1.a_install-t2.a_install)/t2.a_install AS CHAR) AS a_subinstall
                                  FROM
                                  t_apps_additional_new t2,
                                  t_apps_additional_new t1,
                                  (
                                    SELECT a_pkgname
                                    FROM t_apps_speed
                                    WHERE a_softgame = %s AND a_isspeed = 1 AND a_classify = "综合" AND
                                        DATE(a_getdate) = DATE(DATE_SUB(LOCALTIME,INTERVAL 5 DAY)) ORDER BY a_id
                                  ) t0
                                  WHERE
                                  t1.a_pkgname = t0.a_pkgname AND t2.a_pkgname = t0.a_pkgname AND
                                  t1.a_source = "yyb" AND t2.a_source = "yyb" AND
                                  t1.a_getdate BETWEEN DATE(DATE_SUB(LOCALTIME,INTERVAL 10 DAY)) AND
                                  DATE(DATE_SUB(LOCALTIME,INTERVAL 3 DAY)) AND
                                  t2.a_getdate = DATE_SUB(t1.a_getdate,INTERVAL 1 DAY);"""

# current 10 day's install of yesterday install top10 softgame
SQL_CRNT_INSTALL_TOP_SOFTGAME = """SELECT t1.a_pkgname, t1.a_name, t1.a_getdate, t1.a_install
                                    FROM
                                        t_apps_additional_new t1,
                                        (
                                          SELECT a_pkgname
                                          FROM
                                              t_apps_speed
                                          WHERE
                                              a_isspeed = 0 AND a_softgame = %s AND a_classify = "综合" AND
                                              DATE(a_getdate) = DATE(DATE_SUB(LOCALTIME,INTERVAL 5 DAY)) ORDER BY a_id
                                        ) t0
                                    WHERE t1.a_pkgname = t0.a_pkgname AND
                                          t1.a_source = "yyb" AND
                                          t1.a_getdate BETWEEN DATE(DATE_SUB(LOCALTIME,INTERVAL 10 DAY))
                                                        AND DATE(DATE_SUB(LOCALTIME,INTERVAL 3 DAY));"""

# yesterday install top10 classify
SQL_YS_INSTALL_TOP_CLASSIFY = """SELECT
                                      a_pkgname, a_name, a_picurl, a_tdinstall
                                  FROM
                                      t_apps_speed
                                  WHERE
                                  DATE(a_getdate) = DATE(DATE_SUB(LOCALTIME,INTERVAL 5 DAY)) AND a_isspeed = 0 AND
                                  a_classify = %s ORDER BY a_id;"""

# yesterday speed top10 classify
SQL_YS_SPEED_TOP_CLASSIFY = """SELECT a_getdate, a_picurl, a_pkgname, a_name,
                                      ROUND(a_rateinstall*100,2), CONCAT(a_ysinstall," --> ",a_tdinstall)
                                FROM t_apps_speed
                                WHERE DATE(a_getdate) = DATE(DATE_SUB(LOCALTIME,INTERVAL 5 DAY)) AND a_isspeed = 1 AND
                                      a_classify = %s ORDER BY a_id;"""

# search app by name
SQL_SEARCH_APP_BASIC_NAME = """SELECT
                              t0.a_pkgname, t0.a_publisher, t0.a_classify,
                              t1.a_version, t1.a_updatedate, t1.a_score, t1.a_install, t1.a_picurl
                          FROM t_apps_additional_new t1, t_apps_basic_new t0
                          WHERE t0.a_name = %s AND
                                t0.a_source = "yyb" AND t1.a_source = "yyb" AND
                                t1.a_name = %s AND DATE(t1.a_getdate) = DATE(DATE_SUB(LOCALTIME,INTERVAL 1 DAY));"""

# search app current install by name
SQL_SEARCH_APP_INSTALL_NAME = """SELECT a_getdate, a_install FROM t_apps_additional_new
                                  WHERE a_name = %s AND a_source = "yyb" AND
                                  DATE(a_getdate) BETWEEN DATE(DATE_SUB(LOCALTIME,INTERVAL 8 DAY)) AND
                                                          DATE(DATE_SUB(LOCALTIME,INTERVAL 1 DAY));"""

# search app current rate by name
SQL_SEARCH_APP_RATE_NAME = """SELECT t0.a_getdate, CAST(ROUND(1.0*(t0.a_install-t1.a_install)/t1.a_install*100,4) AS CHAR) AS rate
                              FROM t_apps_additional_new t1,
                                    (
                                        SELECT a_install, a_getdate, a_pkgname FROM t_apps_additional_new
                                        WHERE a_name = %s AND a_source = "yyb" AND
                                              DATE(a_getdate) BETWEEN DATE(DATE_SUB(LOCALTIME,INTERVAL 7 DAY)) AND
                                                                      DATE(DATE_SUB(LOCALTIME,INTERVAL 1 DAY))
                                    ) t0
                              WHERE t1.a_pkgname = t0.a_pkgname AND t1.a_source = "yyb" AND
                                    t1.a_getdate = DATE_SUB(t0.a_getdate,INTERVAL 1 DAY);"""

# search similarity app by name
SQL_SEARCH_SIMILARITY_APP_NAME = """SELECT a_name FROM t_apps_basic_new
                                    WHERE a_source = 'yyb' AND a_name LIKE '%s%%';"""
