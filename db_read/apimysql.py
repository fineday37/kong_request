import pymysql

import configparser

from config import setting

cf = configparser.ConfigParser()
cf.read(setting.test_config)

host = cf.get("mysql_conf", "host")
port = cf.get("mysql_conf", "port")
user = cf.get("mysql_conf", "user")
password = cf.get("mysql_conf", "password")
db_name = cf.get("mysql_conf", "db_name")


class DB:
    def __init__(self):
        try:
            self.conn = pymysql.connect(
                port=int(port),
                host=host,
                user=user,
                password=password,
                db=db_name,
                charset='utf8mb4'
            )
            self.cursor = self.conn.cursor()
        except pymysql.OperationalError as e:
            print("mysql error %d: %s" % (e.args[0], e.args[1]))

    def Query_Fetchone(self, sql_name):
        sql_tag = self.cursor.execute(sql_name)
        if sql_tag:
            result = self.cursor.fetchone()
            return result

    def Query_Fetchmany(self, sql_name, number):
        sql_tag = self.cursor.execute(sql_name)
        if sql_tag:
            result = self.cursor.fetchmany(number)
            return result

    def Query_Fetchall(self, sql_name):
        sql_tag = self.cursor.execute(sql_name)
        if sql_tag:
            results = self.cursor.fetchall()
            return results

    def insert(self, table_name, table_data):
        for key in table_data:
            table_data[key] = "'" + str(table_data[key] + "'")
        key = ",".join(table_data.keys())
        value = ",".join(table_data.values())
        real_sql = "insert into" + table_name + "(" + key + ") values + (" + value + ")"
        self.cursor.execute(real_sql)
        self.conn.commit()

    def clear(self, table_name):
        real_sql = "delete from" + table_name + ";"
        self.cursor.execute(real_sql)
        self.conn.commit()

    def init_data(self, data):
        for table_name, table_data in data.items():
            self.clear(table_name)
            for d in table_data:
                self.insert(table_name, d)


if __name__ == '__main__':
    sql = "select * from mbr_member"
    row = DB().Query_Fetchone(sql)
    rows = DB().Query_Fetchmany(sql, 10)
    for i in rows:
        print(i[3])
    print(row)
