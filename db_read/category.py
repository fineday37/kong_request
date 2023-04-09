import pymysql
import configparser
from apimysql import DB
from config import setting

cf = configparser.ConfigParser()
cf.read(setting.test_config)


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


class Category:
    def __init__(self, sql_name):
        self.dm_rows = DB().Query_Fetchall(sql_name)

    # 访客
    def visitor(self, name):
        for dm_row in self.dm_rows:
            recept_num = dm_row[name]
            recept_num_ld = dm_row[name + '_ld']
            recept_num_lw = dm_row[name + '_lw']
            if recept_num_lw:
                daily = round((float(recept_num) - float(recept_num_ld)) / float(recept_num_ld) * 100, 2)
                weeks = round((float(recept_num) - float(recept_num_lw)) / float(recept_num_lw) * 100, 2)
                print("{} {} 查询值为{}, 日环比为：{}, 周同比为：{}".format(dm_row['store_name'],
                                                              dm_row['item_cate'], recept_num, daily, weeks))
            else:
                print("手动查看{}".format(dm_row['item_cate']))

    # 老买家占比
    def Regular(self, molecule, denominator):
        for dm_row in self.dm_rows:
            attnd_cnt = dm_row[molecule]
            attnd_cnt_ld = dm_row[molecule + '_ld']
            attnd_cnt_lw = dm_row[molecule + '_lw']
            cs_cnt = dm_row[denominator]
            cs_cnt_ld = dm_row[denominator + "_ld"]
            cs_cnt_lw = dm_row[denominator + '_lw']
            if attnd_cnt_lw and cs_cnt_lw and cs_cnt and attnd_cnt_ld and cs_cnt_ld:
                duty = round(float(attnd_cnt) / float(cs_cnt) * 100, 2)
                daily = round((float(float(attnd_cnt) / float(cs_cnt))
                               - float(float(attnd_cnt_ld) / float(cs_cnt_ld))) /
                              float(float(attnd_cnt_ld) / float(cs_cnt_ld)) * 100, 2)
                weeks = round((float(float(attnd_cnt) / float(cs_cnt))
                               - float(float(attnd_cnt_lw) / float(cs_cnt_lw))) /
                              float(float(attnd_cnt_lw) / float(cs_cnt_lw)) * 100, 2)
                print("{} {} 比率为{}, 日环比为：{} 周同比为：{}".format(dm_row['store_name'],
                                                            dm_row['item_cate'], duty, daily, weeks, ))
            else:
                print("手动查看{}".format(dm_row['item_cate']))


class Market:
    def __init__(self, sql_name):
        self.dm_rows = DB().Query_Fetchall(sql_name)

    def statistics(self, index):
        if self.dm_rows:
            for dm_row in self.dm_rows:
                recept_num = dm_row[index]
                recept_num_ld = dm_row[index + '_lm']

                if recept_num_ld:
                    daily = round((float(recept_num) - float(recept_num_ld)) / float(recept_num_ld) * 100, 2)
                    print("品类为：{}，店铺为{}， 查询值为{}, 环比为: {}".format(dm_row['category_name'],
                                                                 dm_row['store_name'], recept_num, daily))
                else:
                    print("手动查看店铺{} 品类{}, 查询值{}".format(dm_row['store_name'], dm_row['category_name'], recept_num))
        else:
            print("空值")

    def Conversion(self, index, denominator):
        if self.dm_rows:
            for dm_row in self.dm_rows:
                recept_num = dm_row[index]
                recept_num_ld = dm_row[index + '_lm']
                deno = dm_row[denominator]
                deno_ld = dm_row[denominator + '_lm']
                if recept_num_ld and deno_ld:
                    that_day = round(float(recept_num) / float(deno) * 100, 2)
                    daily = round((float(recept_num) / float(deno) - float(recept_num_ld) / float(deno_ld)) /
                                  float(recept_num_ld) / float(deno_ld) * 100, 2)
                    print("品类为：{}，店铺为{}， 查询值为{}, 环比为: {}".format(dm_row['category_name'],
                                                                 dm_row['store_name'], that_day, daily))
                else:
                    print("手动查看店铺{} 品类{} {}".format(dm_row['store_name'], dm_row['category_name'],
                                                    float(recept_num/deno)))
        else:
            print("空值")


def Get_category():
    category_sql = "SELECT it.item_value dept_id, it.item_text dept_name, it.sort_order  FROM `dim_dict` t INNER JOIN " \
                   "dim_dict_item it ON it.dict_id = t.id AND it.`status` = 1 and it.pid is null WHERE t.dict_code = " \
                   "'cs_market_cat' and t.del_flag = 0 order by it.sort_order "
    dept_id = [dept["dept_id"] for dept in Dim(category_sql)]
    return dept_id


if __name__ == '__main__':
    dept_ids = Get_category()
    for dept_pk in dept_ids:
        dept_sql = "SELECT  distinct it.item_value, itt.item_value store_code, itt.item_text store_name  FROM " \
                   "`dim_dict` t INNER " \
                   "JOIN dim_dict_item it ON it.dict_id = t.id  AND it.`status` = 1 and it.pid is null INNER JOIN " \
                   "dim_dict_item_cs_market itt ON itt.dict_id = it.dict_id and itt.pid = it.id      AND itt.`status` " \
                   "= 1 and itt.refer_value = 'SELF' WHERE t.dict_code = 'cs_market_cat'  and  t.del_flag = 0  and " \
                   "it.item_value = " + "'" + dept_pk + "'" + "order by itt.sort_order "
        competing_sql = "select distinct itt.item_value store_code, itt.item_text  store_name FROM  `dim_dict` t " \
                        "INNER JOIN dim_dict_item it ON it.dict_id = t.id AND it.`status` = 1 and it.pid is null     " \
                        "INNER JOIN dim_dict_item_cs_market itt ON itt.dict_id = it.dict_id and itt.pid = it.id      " \
                        "AND itt.`status` = 1 and itt.refer_value = 'COMPARE' WHERE t.dict_code = 'cs_market_cat' and " \
                        "t.del_flag = 0 and it.item_value = " + "'" + dept_pk + "'" + "order by itt.sort_order "
        for i in Dim(dept_sql):
            analyse_sql = 'select * from dm_analyse_cs_category_m where category_code =' + "'" + i["item_value"] + "'" + \
                          'and store_name =' + "'" + i["store_name"] + "'" + 'and static_date = ' \
                                                                             '"2023-02"; '
            Market(analyse_sql).Conversion("buyer_pay", 'uv')
        for j in Dim(competing_sql):
            com_sql = 'select * from dm_analyse_cs_category_m where store_name =' + "'" + j["store_name"] + "'" + \
                      ' and static_date = "2023-02"; '
            Market(com_sql).Conversion("buyer_pay", 'uv')
    # store = input("店铺：")
    # types = input("类型：")
    # 自定义日期
    # sql = 'select store_name, item_cate, sum(amt_pay) amt_pay, sum(amt_pay_ld) amt_pay_ld, sum(amt_pay_lw) amt_pay_lw,' \
    #       'sum(old_payer_amt_ld), sum(old_payer_amt_lw),sum(uv) uv, sum(uv_ld) uv_ld, sum(uv_lw) uv_lw, ' \
    #       'sum(old_payer_amt) old_payer_amt, sum(old_payer_amt_ld) old_payer_amt_ld, sum(old_payer_amt_lw) ' \
    #       'old_payer_amt_lw, sum(payer_search) payer_search, sum(payer_search_ld) payer_search_ld, ' \
    #       'sum(payer_search_lw) payer_search_lw,sum(uv_search) uv_search, sum(uv_search_ld) uv_search_ld, ' \
    #       'sum(uv_search_lw) uv_search_lw ' \
    #       'from dm_analyse_cs_item_cate_d where static_date BETWEEN "2022-12-15" and "2023-02-28" and store_name = ' \
    #           '"' + store + '" and cate_type = ' '"' + types + '"' + 'group by item_cate;'' \
    # sql = 'select * from dm_analyse_cs_item_cate_d where static_date = "2023-02-28" and ' \
    #       'store_name = ' '"' + store + '" and cate_type = ' '"' + types + '"' + 'group by item_cate;'
    # judgment = input("是否需要计算字段(YES/NO): ")
    # if judgment == "NO":
    #     name = input("无需计算字段：")
    #     Category(sql).visitor(name)
    # else:
    #     molecule_input = input("分子字段：")
    #     denominator_input = input("分母字段")
    #     Category(sql).Regular(molecule_input, denominator_input)
