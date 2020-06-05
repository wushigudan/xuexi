from selenium import webdriver
from time import sleep
import os
import requests,xlwt,json
from aip import AipOcr
import re
import time
# import requests
import pytesseract
from PIL import Image,ImageEnhance
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
def start():
    driver = webdriver.Chrome()  #创建一个谷歌浏览器请求

    url_str = "http://120.79.178.24/gps-web-jt905/login.action"#定义网页地址
    driver.get(url_str)#打开网页
    sleep(3)#等待三秒
    #最大化窗口
    driver.maximize_window()
def logo():
    input_s = driver.find_elements_by_tag_name("input")
    # print(input_s)
    input_username = input_s[1]
    # print(input_username)
    input_password = input_s[4]
    # print(input_password)
    input_phrase = input_s[7]
    # print(input_phrase)
    input_username.clear()
    sleep(1)
    input_username.send_keys("huayutong")
    # input_password = driver.find_element_by_id("password")
    input_password.clear()
    sleep(1)
    input_password.send_keys("666666")
    sleep(1)
    # img_button = driver.find_element_by_id("pic_random_code")
    # img_button.click()
    sleep(0.5)
    driver.save_screenshot('1.png')
    #百度API orc识别
    imgelement = driver.find_element_by_id('pic_random_code')  # 定位验证码
    location = imgelement.location  # 获取验证码x,y轴坐标
    # print(location)
    size = imgelement.size  # 获取验证码的长宽
    # print(size)
    rangle = (int(location['x']), int(location['y']),
              int(location['x'] + size['width']),
              int(location['y'] + size['height']))  # 写成我们需要截取的位置坐标
    i = Image.open("1.png")  # 打开截图
    frame4 = i.crop(rangle)  # 使用Image的crop函数，从截图中再次截取我们需要的区域
    frame4=frame4.convert('RGB')
    frame4.save('save.jpg')
    APP_ID = '20141345'
    API_KEY = 'vArkbCaa8NjuVbYmR31SzF7g'
    SECRET_KEY = 'O3hUtjaxrO3caUgby4o2wsBUImPfAZtx'
    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    with open('save.jpg','rb') as f:
        image=f.read()
    text=client.basicAccurate(image)
    # print(text)
    code = text['words_result'][0]['words']
    # print(code)
    time.sleep(2)
    #输入验证码
    driver.find_element_by_xpath('//*[@id="loginForm"]/table/tbody/tr[4]/td[2]/span[1]/input[1]').send_keys(code)
    # #点击确定
    driver.find_element_by_xpath('//*[@id="loginForm"]/table/tbody/tr[5]/td/input').click()
    #选择所有车辆
    driver.find_element_by_xpath('/html/body/div[3]/div/div/div[2]/div[1]/div/ul/li/span[2]').click()
    time.sleep(20)
#发送post请求
def post():
    url='http://120.79.178.24/gps-web-jt905/realData/refresh.action'
    data={'update':'true'}
    html = requests.post(url,data).text

if __name__ == '__main__':
    start()
    logo()
    post()
