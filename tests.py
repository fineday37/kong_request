import os

import apscheduler.schedulers
import requests

import smtplib
from email.mime.text import MIMEText
import traceback
# 阻塞进程
from apscheduler.schedulers.blocking import BlockingScheduler
# 不阻塞进程
from apscheduler.schedulers.background import BackgroundScheduler
import datetime

data = {
    "username": "object",
    "password": "tests"
}
headers = {"Content-Type": "multipart/form-data"}
data = {
    "title": "上传文件",
    "timestamp": "2022-11-22 16:44:12"
}
files = [('file', ('log.txt', open(os.path.join(os.path.dirname(__file__), "logs", "log.txt"), 'rb'), 'text/plain'))]
r = requests.post(url="http://127.0.0.1:8000/api/file/", files=files, data=data)

print(r.text)


def send_excel():
    try:
        session = smtplib.SMTP_SSL('smtp.qq.com', 465, 30)
        message = MIMEText(r.text, 'plain', 'utf-8')
        message['subject'] = '响应内容'  # 标题
        message['from'] = '1250953976@qq.com'  # 发送人
        message['to'] = 'zhenguo_kong@126.com'  # 接收人
        session.login('1250953976@qq.com', 'gdvurwhwmxvmgdha')
        # 发送
        session.sendmail('1250953976@qq.com', 'zhenguo_kong@126.com', str(message))
        print('发送成功')
    except Exception as e:
        print(traceback.print_exc(), e)  # 打印错误信息


if __name__ == '__main__':
    scheduler = BlockingScheduler(timezone="Asia/Shanghai")
    scheduler.add_job(send_excel, 'date', run_date=datetime.datetime(2023, 1, 5, 14, 45, 5))
    scheduler.add_job(send_excel, 'date', run_date=datetime.datetime(2023, 1, 5, 14, 40, 5))
    scheduler.add_job(send_excel, 'date', run_date=datetime.datetime(2023, 1, 5, 14, 47, 5))
    scheduler.start()

#
#
# def twoSum(nums, target):
#     num = []
#     for i in range(len(nums) - 1):
#         for j in range(i + 1, len(nums)):
#             if nums[i] + nums[j] == target:
#                 num.append(i)
#                 num.append(j)
#                 return num
#
#
# nums = [2, 7, 11, 15]
# target = 22
# print(twoSum(nums, target))
#
# test1 = [2, 4, 3]
# l1 = int(''.join([str(a) for a in test1][::-1]))
# test2 = [5, 6, 4]
# l2 = int(''.join([str(a) for a in test2][::-1]))
# value = l1 + l2
# value_list = list(map(int, str(value)))[::-1]
# print(value_list)
#
#
# class Solution:
#     def lengthOfLongestSubstring(self, s: str) -> int:
#
#         length = 0
#
#         queue = []
#         for i in s:
#             if i in queue:
#                 length = max(length, len(queue))
#                 while i in queue:
#                     queue.pop(0)
#
#             queue.append(i)
#
#         return max(length, len(queue))
#
#
# print(Solution().lengthOfLongestSubstring("abbsbbbbb"))
