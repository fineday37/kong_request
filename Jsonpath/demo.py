import os
from jsonpath import jsonpath
from operation_excel import read_yaml
from faker import Faker
fake = Faker(locale='zh-CN')
data = [{
    "store": {
        "book": [
            {
                "category": "reference",
                "author": fake.name(),
                "title": "Sayings of the Century",
                "price": 8.95
            },
            {
                "category": "fiction",
                "author": fake.name(),
                "title": "Sword of Honour",
                "price": 12.99
            },
            {
                "category": "fiction",
                "author": fake.name(),
                "title": "Moby Dick",
                "isbn": "0-553-21311-3",
                "price": 8.99
            },
            {
                "category": "fiction",
                "author": fake.name(),
                "title": "The Lord of the Rings",
                "isbn": "0-395-19395-8",
                "price": 22.99
            }
        ],
        "bicycle": {
            "color": "red",
            "price": 19.95
        }
    },
    "expensive": 10
}]
getAllBookAuthor = jsonpath(data[0], "$.store.book[*].author")
addfile = os.path.join(os.path.dirname(__file__), "json_test.yaml")
read_yaml.Write_Yaml(data, addfile).write_yam()
print(getAllBookAuthor)
