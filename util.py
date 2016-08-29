# _*_ coding: utf-8 _*_

import pymysql
import logging

# ----server----
SDB_HOST = "101.200.174.172"
SDB_DB = "data_apps"
SDB_USER = "dba_apps"
SDB_PWD = "mimadba_apps"
SDB_CHARSET = "utf8"


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


def condb():
    """
    connect to db
    :return:
    """
    conn = pymysql.connect(host=SDB_HOST, user=SDB_USER, password=SDB_PWD, db=SDB_DB, charset=SDB_CHARSET)
    cur = conn.cursor()
    return conn, cur

