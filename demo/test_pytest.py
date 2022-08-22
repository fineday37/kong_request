import pytest


@pytest.fixture()
def name():
    print("开始执行")


name = "原神"


class Test_001:

    @pytest.mark.usefixtures('name')
    @pytest.mark.smoke
    def test_1(self, name):
        print(name)

    def test_2(self):
        print("test2")


if __name__ == '__main__':
    pytest.main("-m smoke")
