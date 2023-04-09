import pymysql

import configparser

from config import setting

cf = configparser.ConfigParser()
cf.read(setting.test_config)

host = cf.get("BI-mysql-dayu-dm", "host")
port = cf.get("BI-mysql-dayu-dm", "port")
user = cf.get("BI-mysql-dayu-dm", "user")
password = cf.get("BI-mysql-dayu-dm", "password")
db_name = cf.get("BI-mysql-dayu-dm", "db_name")


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
            self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
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


# 当日销售实时数据
def One_day(shops):
    for shop in shops:
        if shop['store_name'] != "整体":
            dm_sql = 'select amt, amt_ld, amt_lw from dm_analyse_cs_store_realtime where store_name =' \
                     + '"' + shop['store_name'] + '" '
            dm_rows = DB().Query_Fetchone(dm_sql)
            amt = dm_rows["amt"]
            amt_ld = dm_rows["amt_ld"]
            amt_lw = dm_rows['amt_lw']
            if amt_ld and amt_lw:
                daily = round((float(amt) - float(amt_ld)) / float(amt_ld) * 100, 2)
                weeks = round((float(amt) - float(amt_lw)) / float(amt_lw) * 100, 2)
                total = round(float(dm_rows["amt"]) / 10000, 2)
                print("{} 总额为{}万，日环比为: {}, 周同比为：{}".format(shop['store_name'], total, daily, weeks))
            else:
                print('手动查看{}'.format(shop['store_name']))
        else:
            dm_sql = 'select amt, amt_ld, amt_lw from dm_analyse_cs_store_realtime where store_name = "整体"' \
                     + 'and dept_name =' + '"' + shop['dept_name'] + '" '
            dm_rows = DB().Query_Fetchone(dm_sql)
            daily = (round((float(dm_rows['amt']) - float(dm_rows["amt_ld"])) / float(dm_rows["amt_ld"]) * 100, 2))
            weeks = round((float(dm_rows['amt']) - float(dm_rows['amt_lw'])) / float(dm_rows['amt_lw']) * 100, 2)
            total = round(float(dm_rows["amt"]) / 10000, 2)
            print("{} 总额为{}万, 日环比为: {}， 周同比为：{}".format(shop['dept_name'], total, daily, weeks))


# 店铺模块
class Shop_day:
    def __init__(self, sql_name):
        self.sql_name = sql_name
        self.dm_rows = DB().Query_Fetchall(self.sql_name)

    # 销售额
    def sales(self):
        for dm_row in self.dm_rows:
            if dm_row["store_name"] != '整体':
                amt_shop = dm_row["amt_shop"]
                amt_shop_ld = dm_row["amt_shop_ld"]
                amt_shop_lw = dm_row['amt_shop_lw']
                target = dm_row["amt_shop_target"]
                if amt_shop_lw and target:
                    daily = round((float(amt_shop) - float(amt_shop_ld)) / float(amt_shop_ld) * 100, 2)
                    weeks = round((float(amt_shop) - float(amt_shop_lw)) / float(amt_shop_lw) * 100, 2)
                    total = round(float(amt_shop) / 10000, 2)
                    complete = round(float(amt_shop) / float(target), 2)
                    print("{} 总额为{}万，日环比为 {}，周同比为：{}, 目标为{}，完成值{}".format(dm_row['store_name'], total,
                                                                          daily, weeks, target, complete))
            else:
                daily = (
                    round(
                        (float(dm_row['amt_shop']) - float(dm_row["amt_shop_ld"])) / float(dm_row["amt_shop_ld"]) * 100,
                        2))
                target = dm_row["amt_shop_target"]
                if dm_row['amt_shop_lw'] and target:
                    complete = round(float(dm_row["amt_shop"]) / float(target), 2)
                    weeks = round(
                        (float(dm_row['amt_shop']) - float(dm_row['amt_shop_lw'])) / float(dm_row['amt_shop_lw']) * 100,
                        2)
                    total = round(float(dm_row["amt_shop"]) / 10000, 2)
                    print("{} 总额为{}万，日环比为 {}, 周同比为：{}, 目标为{}，完成值{}".format(dm_row['store_name'], total,
                                                                           daily, weeks, target, complete))

    # 客服
    def Customer(self):
        for dm_row in self.dm_rows:
            amt_shop = dm_row["cs_cnt"]
            # amt_shop_ld = dm_row["cs_cnt_ld"]
            amt_shop_lw = dm_row['cs_cnt_ly']
            if dm_row["store_name"] != '整体':
                if amt_shop_lw != 0:
                    # daily = round((float(amt_shop) - float(amt_shop_ld)) / float(amt_shop_ld) * 100, 2)
                    weeks = round((float(amt_shop) - float(amt_shop_lw)) / float(amt_shop_lw) * 100, 2)
                    print("{} 客服人数为{}, 周同比为：{}".format(dm_row['store_name'], amt_shop, weeks))
                else:
                    print("{} 客服人数为{}, 日环比为: 0， 周同比为：0".format(dm_row['store_name'], amt_shop))
            else:
                if amt_shop_lw:
                    # daily = (
                    #     round(
                    #         (float(amt_shop) - float(amt_shop_ld)) / float(amt_shop_ld) * 100, 2))
                    weeks = round(
                        (float(amt_shop) - float(amt_shop_lw)) / float(amt_shop_lw) * 100, 2)
                    print("{} 客服人数为{}, 周同比为：{}".format(dm_row['dept_name'], amt_shop, weeks))
                else:
                    print("{} 客服人数为{}, 日环比为: 0， 周同比为：0".format(dm_row['store_name'], amt_shop))

    # 出勤率
    def Duty(self):
        for dm_row in self.dm_rows:
            attnd_cnt = dm_row['attnd_cnt']
            attnd_cnt_ld = dm_row['attnd_cnt_ld']
            attnd_cnt_lw = dm_row['attnd_cnt_lw']
            cs_cnt = dm_row["cs_cnt"]
            cs_cnt_ld = dm_row["cs_cnt_ld"]
            cs_cnt_lw = dm_row['cs_cnt_lw']
            if cs_cnt:
                duty = round(int(attnd_cnt) / int(cs_cnt) * 100, 2)
                if dm_row["store_name"] != '整体':
                    if cs_cnt_lw != 0:
                        daily = round((float(int(attnd_cnt) / int(cs_cnt))
                                       - float(int(attnd_cnt_ld) / int(cs_cnt_ld))) /
                                      float(int(attnd_cnt_ld) / int(cs_cnt_ld)) * 100, 2)
                        weeks = round((float(int(attnd_cnt) / int(cs_cnt))
                                       - float(int(attnd_cnt_lw) / int(cs_cnt_lw))) /
                                      float(int(attnd_cnt_lw) / int(cs_cnt_lw)) * 100, 2)
                        print("{} 出勤率为{}, 日环比为：{}周同比为：{}".format(dm_row['store_name'], duty, daily, weeks, ))
                    else:
                        print("{} 出勤率为{}, 日环比为: 0， 周同比为：0".format(dm_row['store_name'], duty))
                else:
                    daily = round((float(int(attnd_cnt) / int(cs_cnt))
                                   - float(int(attnd_cnt_ld) / int(cs_cnt_ld))) /
                                  float(int(attnd_cnt_ld) / int(cs_cnt_ld)) * 100, 2)
                    weeks = round((float(int(attnd_cnt) / int(cs_cnt))
                                   - float(int(attnd_cnt_lw) / int(cs_cnt_lw))) /
                                  float(int(attnd_cnt_lw) / int(cs_cnt_lw)) * 100, 2)
                    print("{} 出勤率为{}, 日环比为：{} 周同比为：{}".format(dm_row['dept_name'], duty, daily, weeks, ))

    # 接待人数
    def visitors(self):
        for dm_row in self.dm_rows:
            recept_num = dm_row["recept_num"]
            # recept_num_ld = dm_row["recept_num_ld"]
            recept_num_lw = dm_row['recept_num_ly']
            if dm_row["store_name"] != '整体':
                # daily = round((float(recept_num) - float(recept_num_ld)) / float(recept_num_ld) * 100, 2)
                weeks = round((float(recept_num) - float(recept_num_lw)) / float(recept_num_lw) * 100, 2)
                print("{} 接待人数为{}, 周同比为：{}".format(dm_row['store_name'], recept_num, weeks))
            else:
                # daily = (
                #     round(
                #         (float(recept_num) - float(recept_num_ld)) / float(recept_num_ld) * 100, 2))
                weeks = round(
                    (float(recept_num) - float(recept_num_lw)) / float(recept_num_lw) * 100, 2)
                print("{} 接待人数为{}, 周同比为：{}".format(dm_row['dept_name'], recept_num, weeks))

    # 转化率
    def Rotation(self):
        for dm_row in self.dm_rows:
            trans_rate_mol = dm_row['trans_rate_mol']
            trans_rate_mol_ld = dm_row['trans_rate_mol_ld']
            trans_rate_mol_lw = dm_row['trans_rate_mol_lw']
            trans_rate_deno = dm_row["trans_rate_deno"]
            trans_rate_deno_ld = dm_row["trans_rate_deno_ld"]
            trans_rate_deno_lw = dm_row['trans_rate_deno_lw']
            duty = round(float(trans_rate_mol) / float(trans_rate_deno) * 100, 2)
            if dm_row["store_name"] != '整体':
                if trans_rate_deno != 0 and trans_rate_deno != 0:
                    daily = round((float(float(trans_rate_mol) / float(trans_rate_deno))
                                   - float(float(trans_rate_mol_ld) / float(trans_rate_deno_ld))) /
                                  float(float(trans_rate_mol_ld) / float(trans_rate_deno_ld)) * 100, 2)
                    weeks = round((float(float(trans_rate_mol) / float(trans_rate_deno))
                                   - float(float(trans_rate_mol_lw) / float(trans_rate_deno_lw))) /
                                  float(float(trans_rate_mol_lw) / float(trans_rate_deno_lw)) * 100, 2)
                    print("{} 转化率为{}, 日环比{} 周同比为：{}".format(dm_row['store_name'], duty, daily, weeks, ))
                else:
                    print("{} 转化率为0, 日环比为: 0， 周同比为：0".format(dm_row['store_name']))
            else:
                daily = round((float(float(trans_rate_mol) / float(trans_rate_deno))
                               - float(float(trans_rate_mol_ld) / float(trans_rate_deno_ld))) /
                              float(float(trans_rate_mol_ld) / float(trans_rate_deno_ld)) * 100, 2)
                weeks = round((float(float(trans_rate_mol) / float(trans_rate_deno))
                               - float(float(trans_rate_mol_lw) / float(trans_rate_deno_lw))) /
                              float(float(trans_rate_mol_lw) / float(trans_rate_deno_lw)) * 100, 2)
                print("{} 转化率为{}, 日环比{}, 周同比为：{}".format(dm_row['dept_name'], duty, daily, weeks, ))

    # 客单价
    def unit_price(self):
        for dm_row in self.dm_rows:
            amt_shop = dm_row['amt_shop']
            # amt_shop_ld = dm_row['amt_shop_ld']
            amt_shop_lw = dm_row['amt_shop_ly']
            amtnum_shop = dm_row["amtnum_shop"]
            # amtnum_shop_ld = dm_row["amtnum_shop_ld"]
            amtnum_shop_lw = dm_row['amtnum_shop_ly']
            duty = round(float(amt_shop) / float(amtnum_shop), 2)
            if dm_row["store_name"] != '整体':
                if amtnum_shop_lw != 0:
                    # daily = round((float(float(amt_shop) / float(amtnum_shop))
                    #                - float(float(amt_shop_ld) / float(amtnum_shop_ld))) /
                    #               float(float(amt_shop_ld) / float(amtnum_shop_ld)) * 100, 2)
                    weeks = round((float(float(amt_shop) / float(amtnum_shop))
                                   - float(float(amt_shop_lw) / float(amtnum_shop_lw))) /
                                  float(float(amt_shop_lw) / float(amtnum_shop_lw)) * 100, 2)
                    print("{} 客单价为{}, 周同比为：{}".format(dm_row['store_name'], duty, weeks, ))
                else:
                    print("{} 客单价为0, 日环比为: 0， 周同比为：0".format(dm_row['store_name']))
            else:
                # daily = round((float(float(amt_shop) / float(amtnum_shop))
                #                - float(float(amt_shop_ld) / float(amtnum_shop_ld))) /
                #               float(float(amt_shop_ld) / float(amtnum_shop_ld)) * 100, 2)
                weeks = round((float(float(amt_shop) / float(amtnum_shop))
                               - float(float(amt_shop_lw) / float(amtnum_shop_lw))) /
                              float(float(amt_shop_lw) / float(amtnum_shop_lw)) * 100, 2)
                print("{} 客单价为{}, 周同比为：{}".format(dm_row['dept_name'], duty, weeks, ))

    # 响应时间
    def Response(self):
        for dm_row in self.dm_rows:
            amt_shop = dm_row['rtt_mol']
            # amt_shop_ld = dm_row['rtt_mol_ld']
            amt_shop_lw = dm_row['rtt_mol_ly']
            amtnum_shop = dm_row["recept_num"]
            # amtnum_shop_ld = dm_row["recept_num_ld"]
            amtnum_shop_lw = dm_row['recept_num_ly']
            duty = round(float(amt_shop) / float(amtnum_shop), 2)
            if dm_row["store_name"] != '整体':
                if amtnum_shop_lw != 0:
                    # daily = round((float(float(amt_shop) / float(amtnum_shop))
                    #                - float(float(amt_shop_ld) / float(amtnum_shop_ld))) /
                    #               float(float(amt_shop_ld) / float(amtnum_shop_ld)) * 100, 2)
                    weeks = round((float(float(amt_shop) / float(amtnum_shop))
                                   - float(float(amt_shop_lw) / float(amtnum_shop_lw))) /
                                  float(float(amt_shop_lw) / float(amtnum_shop_lw)) * 100, 2)
                    print("{} 响应时间为{}, 周同比为：{}".format(dm_row['store_name'], duty, weeks, ))
                else:
                    print("{} 客单价为0, 日环比为: 0， 周同比为：0".format(dm_row['store_name']))
            else:
                # daily = round((float(float(amt_shop) / float(amtnum_shop))
                #                - float(float(amt_shop_ld) / float(amtnum_shop_ld))) /
                #               float(float(amt_shop_ld) / float(amtnum_shop_ld)) * 100, 2)
                weeks = round((float(float(amt_shop) / float(amtnum_shop))
                               - float(float(amt_shop_lw) / float(amtnum_shop_lw))) /
                              float(float(amt_shop_lw) / float(amtnum_shop_lw)) * 100, 2)
                print("{} 响应时间为{}, 周同比为：{}".format(dm_row['dept_name'], duty, weeks, ))

    # 退款率
    def Refund(self):
        for dm_row in self.dm_rows:
            trans_rate_mol = dm_row['amt_refund']
            # trans_rate_mol_ld = dm_row['amt_refund_ld']
            trans_rate_mol_lw = dm_row['amt_refund_ly']
            trans_rate_deno = dm_row["amt_shop"]
            # trans_rate_deno_ld = dm_row["amt_shop_ld"]
            trans_rate_deno_lw = dm_row['amt_shop_ly']
            duty = round(float(trans_rate_mol) / float(trans_rate_deno) * 100, 2)
            if dm_row["store_name"] != '整体':
                if trans_rate_deno != 0 and trans_rate_deno != 0:
                    # daily = round((float(float(trans_rate_mol) / float(trans_rate_deno))
                    #                - float(float(trans_rate_mol_ld) / float(trans_rate_deno_ld))) /
                    #               float(float(trans_rate_mol_ld) / float(trans_rate_deno_ld)) * 100, 2)
                    weeks = round((float(float(trans_rate_mol) / float(trans_rate_deno))
                                   - float(float(trans_rate_mol_lw) / float(trans_rate_deno_lw))) /
                                  float(float(trans_rate_mol_lw) / float(trans_rate_deno_lw)) * 100, 2)
                    print("{} 退款率为{}, 周同比为：{}".format(dm_row['store_name'], duty, weeks, ))
                else:
                    print("{} 退款率为0, 日环比为: 0， 周同比为：0".format(dm_row['store_name']))
            else:
                # daily = round((float(float(trans_rate_mol) / float(trans_rate_deno))
                #                - float(float(trans_rate_mol_ld) / float(trans_rate_deno_ld))) /
                #               float(float(trans_rate_mol_ld) / float(trans_rate_deno_ld)) * 100, 2)
                weeks = round((float(float(trans_rate_mol) / float(trans_rate_deno))
                               - float(float(trans_rate_mol_lw) / float(trans_rate_deno_lw))) /
                              float(float(trans_rate_mol_lw) / float(trans_rate_deno_lw)) * 100, 2)
                print("{} 退款率为{}, 周同比为：{}".format(dm_row['dept_name'], duty, weeks, ))

    # 剩余金额
    def surplus(self):
        for dm_row in self.dm_rows:
            trans_rate_mol = dm_row['amt_shop']
            trans_rate_mol_ld = dm_row['amt_shop_ld']
            trans_rate_mol_lw = dm_row['amt_shop_lw']
            trans_rate_deno = dm_row["amt_refund"]
            trans_rate_deno_ld = dm_row["amt_refund_ld"]
            trans_rate_deno_lw = dm_row['amt_refund_lw']
            duty = round(float(trans_rate_mol) - float(trans_rate_deno), 2)
            if dm_row["store_name"] != '整体':
                if trans_rate_deno != 0 and trans_rate_deno != 0:
                    daily = round((float(float(trans_rate_mol) - float(trans_rate_deno))
                                   - float(float(trans_rate_mol_ld) - float(trans_rate_deno_ld))) /
                                  float(float(trans_rate_mol_ld) - float(trans_rate_deno_ld)) * 100, 2)
                    weeks = round((float(float(trans_rate_mol) - float(trans_rate_deno))
                                   - float(float(trans_rate_mol_lw) - float(trans_rate_deno_lw))) /
                                  float(float(trans_rate_mol_lw) - float(trans_rate_deno_lw)) * 100, 2)
                    print("{} 退款后金额为{}, 日环比：{}周同比为：{}".format(dm_row['store_name'], duty, daily, weeks, ))
                else:
                    print("{} 退款后金额为0, 日环比为: 0， 周同比为：0".format(dm_row['store_name']))
            else:
                daily = round((float(float(trans_rate_mol) - float(trans_rate_deno))
                               - float(float(trans_rate_mol_ld) - float(trans_rate_deno_ld))) /
                              float(float(trans_rate_mol_ld) - float(trans_rate_deno_ld)) * 100, 2)
                weeks = round((float(float(trans_rate_mol) - float(trans_rate_deno))
                               - float(float(trans_rate_mol_lw) - float(trans_rate_deno_lw))) /
                              float(float(trans_rate_mol_lw) - float(trans_rate_deno_lw)) * 100, 2)
                print("{} 退款后金额为{}, 日环比：{},周同比为：{}".format(dm_row['dept_name'], duty, daily, weeks, ))

    # 接待人数
    def payer(self):
        for dm_row in self.dm_rows:
            recept_num = dm_row["amtnum_shop"]
            # recept_num_ld = dm_row["amtnum_shop_ld"]
            recept_num_lw = dm_row['amtnum_shop_ly']
            if dm_row["store_name"] != '整体':
                # daily = round((float(recept_num) - float(recept_num_ld)) / float(recept_num_ld) * 100, 2)
                weeks = round((float(recept_num) - float(recept_num_lw)) / float(recept_num_lw) * 100, 2)
                print("{} 支付人数为{}, 周同比为：{}".format(dm_row['store_name'], recept_num, weeks))
            else:
                # daily = (
                #     round(
                #         (float(recept_num) - float(recept_num_ld)) / float(recept_num_ld) * 100, 2))
                weeks = round(
                    (float(recept_num) - float(recept_num_lw)) / float(recept_num_lw) * 100, 2)
                print("{} 支付人数为{}, 周同比为：{}".format(dm_row['dept_name'], recept_num, weeks))

    # 询单人数
    def inquiries(self):
        for dm_row in self.dm_rows:
            recept_num = dm_row["inquiry_num"]
            # recept_num_ld = dm_row["inquiry_num_ld"]
            recept_num_lw = dm_row['inquiry_num_ly']
            if dm_row["store_name"] != '整体':
                # daily = round((float(recept_num) - float(recept_num_ld)) / float(recept_num_ld) * 100, 2)
                weeks = round((float(recept_num) - float(recept_num_lw)) / float(recept_num_lw) * 100, 2)
                print("{} 询单人数为{}, 周同比为：{}".format(dm_row['store_name'], recept_num, weeks))
            else:
                # daily = (
                #     round(
                #         (float(recept_num) - float(recept_num_ld)) / float(recept_num_ld) * 100, 2))
                weeks = round(
                    (float(recept_num) - float(recept_num_lw)) / float(recept_num_lw) * 100, 2)
                print("{} 询单人数为{}, 周同比为：{}".format(dm_row['dept_name'], recept_num, weeks))


def Dim(sql_name):
    dim_host = cf.get("BI-mysql-dayu-dim", "host")
    dim_port = cf.get("BI-mysql-dayu-dim", "port")
    dim_user = cf.get("BI-mysql-dayu-dim", "user")
    dim_password = cf.get("BI-mysql-dayu-dim", "password")
    dim_db_name = cf.get("BI-mysql-dayu-dim", "db_name")
    conn = pymysql.connect(
        port=int(dim_port),
        host=dim_host,
        user=dim_user,
        password=dim_password,
        db=dim_db_name,
        charset='utf8mb4'
    )
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql_tag = cursor.execute(sql_name)
    if sql_tag:
        results = cursor.fetchall()
        return results


if __name__ == '__main__':
    res = Dim("select b.item_text store_name from `dim_dict` t inner join "
              "dim_dict_item a on a.dict_id = t.id and a.`status` =1 and a.pid is null and t.del_flag = 0 inner join "
              "dim_dict_item b on a.dict_id = b.dict_id and b.pid = a.id where t.dict_code = 'cs_dept' order by "
              "b.sort_order;")
    shop_sql = "select * from dm_analyse_cs_store_d " \
               "" \
               "where static_date = '2023-02-28' group by dept_name, store_name; "
    ONe_sql = 'select * from dm_analyse_cs_store_realtime'
    shop_name = []
    for shop in DB().Query_Fetchall(ONe_sql):
        shop_name.append(shop)
    One_day(shop_name)
    Shop_day(shop_sql).Rotation()
    # name = input("选项：")
    # shop = {"销售额": Shop_day(shop_sql).sales(), "客服": Shop_day(shop_sql).Customer()}
