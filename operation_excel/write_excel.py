import xlwings as xw
from config import setting


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
        self.app.quit()


if __name__ == '__main__':
    WriteExcel(setting.test_data).update_excel("A5:A10", "原神")
