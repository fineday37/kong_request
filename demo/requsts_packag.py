import datetime
import pprint

import requests
import json
from config import setting
# from operation_excel.read_excel import ReadExcel
from operation_excel.read_yaml import Read_Yaml, Write_Yaml


class PacKag:
    def __init__(self, api_data):
        self.api_data = api_data

    def packaging(self):
        if self.api_data["method"] == "get":
            res = requests.request(method=self.api_data["method"], url=self.api_data["url"],
                                   params=self.api_data["params"], headers=self.api_data["headers"])
        else:
            data = json.dumps(self.api_data["body"])
            res = requests.request(method=self.api_data["method"], url=self.api_data["url"],
                                   data=data, headers=self.api_data["headers"])
        return res.json()

    def authentication(self):
        token = Read_Yaml(setting.write_yaml).read_yam()
        news = self.api_data["headers"]
        news["Authorization"] = token["token"]["authentication"]
        if self.api_data["method"] == "get":
            res = requests.request(method=self.api_data["method"], url=self.api_data["url"],
                                   params=self.api_data["params"], headers=news)
        else:
            data = json.dumps(self.api_data["body"])
            res = requests.request(method=self.api_data["method"], url=self.api_data["url"],
                                   data=data, headers=news)
        return res.json()


if __name__ == '__main__':
    apidata = Read_Yaml(setting.yaml_data).read_yam()
    response = PacKag(apidata[0]).packaging()
    pprint.pprint(response)
    data = {"token": {"authentication": response["data"]["token"]}}
    Write_Yaml(data).write_yam()
    query_label = Read_Yaml(setting.authentication_yaml).read_yam()
    res = PacKag(query_label[0]).authentication()
    pprint.pprint(res)
    if res['data']['list'][0]['labelName'] == "iopk":
        print("测试通过")
    else:
        print('测试失败')
    # login = {
    #     "url": "http://10.168.20.188:9000/basic-api/auth/login/account",
    #     "headers": {"Content-Type": "application/json"},
    #     "body": {"account": "admin", "autoLogin": "false", "password": "sjkyadmin"},
    #     "method": "post"
    # }
    # tokens = PacKag(login).packaging()["data"]["token"]
    # write_token = {"token": {"authentication": tokens}}
    # Write_Yaml(write_token).write_yam()
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
