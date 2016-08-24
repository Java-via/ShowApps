# _*_ coding: utf-8 _*_

import hashlib

# f = open("G:/imie.txt", "r")
# for line in f.readlines():
#     result = hashlib.md5(line.strip().upper().encode()).hexdigest()
#     print("'" + result + "'" + ",")


def make_con():
    old = open("G:/imie.txt", "r", encoding="utf-8")
    md5_old_dict = {}
    for line_o in old.readlines():
        md5_old_dict[hashlib.md5(line_o.strip().upper().encode()).hexdigest()] = line_o.strip()
    print(md5_old_dict)

    data = open("G:/out.txt", "r", encoding="utf-8")
    result_w = open("G:/result.txt", "a", encoding="utf-8")
    for line_d in data.readlines():
        result = line_d.split("\t")
        old_dev = result[0]
        result_w.write(md5_old_dict[old_dev] + "\t" + result[1] + "\n")


if __name__ == "__main__":
    make_con()
