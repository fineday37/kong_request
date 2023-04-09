import datetime

import xlwings as xw
from config import setting
import datetime


class WriteExcel:
    def __init__(self, filename):
        self.app = xw.App(visible=True, add_book=False)
        self.wb = self.app.books.open(filename)
        self.sht = self.wb.sheets["sheet1"]

    def update_excel(self, location, content):
        locations = self.sht.range(location)
        locations.columns.autofit()
        locations.rows.autofit()
        locations.api.HorizontalAlignment = -4108
        locations.color = (255, 0, 0)
        locations.value = content
        self.wb.save()
        # self.app.quit()


if __name__ == '__main__':
    WriteExcel(setting.test_data).update_excel("A11", [['蒙德', "璃月", "稻妻"], ["温迪", "钟离", "雷电影"]])
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    st = '2023-01-09 15:10'
    dt = datetime.datetime.strptime(st, '%Y-%m-%d %H:%M')
    print(dt.timestamp())
