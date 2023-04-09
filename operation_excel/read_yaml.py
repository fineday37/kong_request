import os

import yaml
from config import setting
import pprint
from logs.log import logger


class Read_Yaml:
    def __init__(self, filename):
        self.filename = filename

    def read_yam(self):
        with open(self.filename, "r", encoding="utf-8") as f:
            context = yaml.load(f, Loader=yaml.Loader)
        return context


class Write_Yaml:
    def __init__(self, response_data, addfile):
        self.addfile = addfile
        self.data = response_data

    def write_yam(self):
        try:
            with open(self.addfile, "w", encoding="utf-8") as f:
                yaml.dump(self.data, f, allow_unicode=True)
            logger.info("写入数据成功")
        except Exception as e:
            logger.error(e)


if __name__ == '__main__':
    data = Read_Yaml(setting.yaml_data).read_yam()
    pprint.pprint(data)
    # x = [{"token": ""}]
    # Write_Yaml(x).write_yam()
    # authentication = Read_Yaml(setting.write_yaml).read_yam()
    # pprint.pprint(authentication)
    # dragon = {"demo": "龙炎放歌"}
    # dragon["Authentication"] = authentication["token"]["authentication"]
    # print(dragon)
