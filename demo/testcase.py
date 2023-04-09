# import json
import os

import allure
import pytest
from pytest_assume.plugin import assume

from operation_excel.read_yaml import Read_Yaml, Write_Yaml
from config import setting
from demo.requsts_packag import PacKag
from logs.log import logger


@pytest.fixture(scope="function", params=[1, 2, 4])
def authorization(request) -> str:
    login = {
        "url": "http://10.168.20.48:9000/api/auth/login/account",
        "headers": {"Content-Type": "application/json"},
        "body": {"account": 210910622, "password": "sjky210910622"},
        "method": "post"
    }
    tokens = PacKag(login).packaging()["data"]["token"]
    write_token = {"token": {"authentication": tokens}}
    Write_Yaml(write_token, setting.write_yaml).write_yam()
    yield request.param
    print("测试完成")


@pytest.fixture(scope="function")
def test_date(request):
    yield request.param["status_code"]


@allure.feature('登录')
class Test_001:
    test_data = Read_Yaml(setting.yaml_data).read_yam()

    @allure.title("用户登录")
    @allure.story('不同的登录输入')
    @allure.severity('blocker')
    @pytest.mark.parametrize("arg", test_data)
    def test_case001(self, arg):
        try:
            res = PacKag(arg).packaging()
            assert res["errorMessage"] == arg["msg"]
            logger.info("测试通过，结果为{}".format(res["errorMessage"]))
            test_path = os.path.join(os.path.dirname(__file__), "秋水.jpg")
            allure.attach.file(source=test_path, name="李素裳", attachment_type=allure.attachment_type.JPG)
            # 上传附件
        except Exception as e:
            logger.error(e)


class Test_002:
    test_data = Read_Yaml(setting.authentication_yaml).read_yam()

    @allure.title("查询标签")
    @pytest.mark.smoke
    # @pytest.mark.usefixtures("authorization")
    @pytest.mark.parametrize("test_date", test_data, indirect=True)
    @pytest.mark.parametrize("arg", test_data)
    @pytest.mark.parametrize("args, tt", [(1, 2), (3, 4)], ids=["a:{}-b:{}".format(a, b) for a, b in [(1, 2), (3, 4)]])
    def test_case002(self, arg, authorization, test_date, args, tt):  # 需要参数时直接传进去，不需要走parametrize
        try:
            res = PacKag(arg).authentication()["data"]
            for i in range(3):
                pytest.assume(res[i]["moduleType"] == "拼多多")
                logger.info("数据为{}".format(res[i]["moduleType"]))
                print(authorization)
                print(test_date)  # fixture+mark实现数据驱动，mark获取数据传入test_date
                print(args, tt)
            pytest.assume(1 == 1)
            # logger.info("验证失败")
        except Exception as e:
            logger.error(e)
