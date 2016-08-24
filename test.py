# _*_ coding: utf-8 _*_
import sys
import pymysql

conn = pymysql.connect(host="127.0.0.1", user="root", passwd="123", db="my_db", charset="utf8")
curs = conn.cursor()


def delete_func(tablename, **kwargs):
    sql_str = "delete from %s " % tablename
    if "appid" in kwargs and "ds" in kwargs:
        sql_str += "where appid in ('%s') and ds='%s'" % (kwargs["appid"], kwargs["ds"])
        print(sql_str)
    elif "appid" in kwargs:
        sql_str += "where appid in ('%s')" % (kwargs["appid"])
        print(sql_str)
    elif "ds" in kwargs:
        sql_str += "where ds='%s'" % kwargs["ds"]
        print(sql_str)
    else:
        print(sql_str)
        pass
    return sql_str

if len(sys.argv) == 2:
    delete_func(sys.argv[1])
    print(1)
elif len(sys.argv) == 3:
    strin = sys.argv[2].split("=")
    if strin[0] == "appid":
        delete_func(sys.argv[1], appid=strin[1])
    elif strin[0] == "ds":
        delete_func(sys.argv[1], ds=strin[1])
    else:
        print("param error")
    print(2)
else:
    strin_appid = sys.argv[2].split("=")
    print(strin_appid)
    strin_ds = sys.argv[3].split("=")
    print(strin_ds)
    count = curs.execute(delete_func(sys.argv[1], appid=strin_appid[1], ds=strin_ds[1]))
conn.commit()
