import pprint

from config import setting
import xlrd


class ReadExcel:
    def __init__(self, filename, sheetName):
        self.data = xlrd.open_workbook(filename)
        self.table = self.data.sheet_by_name(sheetName)
        self.nrows = self.table.nrows
        self.ncols = self.table.ncols

    def read_data(self):
        if self.nrows > 1:
            keys = self.table.row_values(0)
            listApidata = []
            for col in range(1, self.nrows):
                values = self.table.row_values(col)
                api_dict = dict(zip(keys, values))
                listApidata.append(api_dict)
            return listApidata
        else:
            print("表格为空")


if __name__ == '__main__':
    pprint.pprint(ReadExcel(setting.test_data, "Sheet1").read_data())
