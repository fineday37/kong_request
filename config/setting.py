import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)

test_config = os.path.join(BASE_DIR, "database", "config.ini")
test_data = os.path.join(BASE_DIR, "operation_excel", "Excel", "testcase.xlsx")
yaml_data = os.path.join(BASE_DIR, "operation_excel", "Excel", "testdata.yaml")
write_yaml = os.path.join(BASE_DIR, "operation_excel", "Excel", "drive.yaml")
authentication_yaml = os.path.join(BASE_DIR, "operation_excel", "Excel", "authentication_test.yaml")