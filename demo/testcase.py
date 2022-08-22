import json

import allure
import pytest
from operation_excel.read_yaml import Read_Yaml, Write_Yaml
from config import setting
from demo.requsts_packag import PacKag
from logs.log import Format, logger


@pytest.fixture(scope="function")
def authorization():
    login = {
        "url": "http://10.168.20.188:9000/basic-api/auth/login/account",
        "headers": {"Content-Type": "application/json"},
        "body": {"account": "admin", "autoLogin": "false", "password": "sjkyadmin"},
        "method": "post"
    }
    tokens = PacKag(login).packaging()["data"]["token"]
    write_token = {"token": {"authentication": tokens}}
    Write_Yaml(write_token).write_yam()
    return "获取token成功"


class Test_001:
    test_data = Read_Yaml(setting.yaml_data).read_yam()

    @allure.title("用户登录")
    @pytest.mark.parametrize("arg", test_data)
    def test_case001(self, arg):
        try:
            res = PacKag(arg).packaging()
            assert res["errorMessage"] == arg["msg"]
            logger.info("测试通过，结果为{}".format(res["errorMessage"]))
        except Exception as e:
            Format().error(e)


class Test_002:
    test_data = Read_Yaml(setting.authentication_yaml).read_yam()

    @allure.title("查询标签")
    @pytest.mark.smoke
    @pytest.mark.usefixtures("authorization")
    @pytest.mark.parametrize("arg", test_data)
    def test_case002(self, arg):
        try:
            res = PacKag(arg).authentication()
            assert res["data"]["list"][0]["labelName"] == arg["body"]["labelName"]
            logger.info("查询标签成功，查询的标签名为{}".format(res["data"]["list"][0]["labelName"]))
        except Exception as e:
            logger.error(e)


if __name__ == '__main__':
    pytest.main("-v", "-m")
