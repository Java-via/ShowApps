# _*_ coding: utf-8 _*_
import pymysql
import util

conn, cur = util.condb()
cur.execute("SELECT DISTINCT a_pkgname FROM t_apps_basic_united")

pkgname_set = set(item[0] for item in cur.fetchall())
print(pkgname_set)

old_new_list = {}

f = open("G:/tmp/tmp.csv", "r", encoding="utf-8")
ff = open("G:/tmp/tmp1", "a", encoding="utf-8")
for line in f.readlines():
    item_old_new = []
    old = []
    new = []
    deviceid = ""
    if '"' in line:
        res = line.split('"')
        deviceid = res[0]
        print("DEV:" + deviceid)
        ff.write(deviceid + "\t")
        old = res[1]
        ff.write(res[1] + "\t")
        print("OLD" + res[1])
        pkgname = res[1].split(",")
        for pkg in pkgname:
            if pkg in pkgname_set:
                ff.write(pkg + ",")
                print("IN" + pkg)
        ff.write("\n")
    else:
        res = line.split(",")
        deviceid = res[0]
        ff.write(deviceid + "\t")
        if res[1] in pkgname_set:
            print("IN" + res[1])
            old = res[1]
            new = res[1]
            old = res[1]
            ff.write(new + "\t")
        else:
            ff.write(deviceid + "\n")

