# coding = utf-8

import csv
import codecs
from selenium import webdriver
from time import sleep
import os
from aip import AipOcr
import re
import time
# import requests
import pytesseract
from PIL import Image, ImageEnhance
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()


# 打开网页
def start():
    url_str = "http://120.79.178.24/gps-web-jt905/main.action#"
    driver.get(url_str)
    sleep(3)
    # 最大化窗口
    driver.maximize_window()


def logn():
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
    input_username.send_keys("sa")
    # input_password = driver.find_element_by_id("password")
    input_password.clear()
    sleep(1)
    input_password.send_keys("cr8888")
    sleep(1)
    # img_button = driver.find_element_by_id("pic_random_code")
    # img_button.click()
    sleep(0.5)
    driver.save_screenshot('1.png')
    # 百度API orc识别
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
    frame4 = frame4.convert('RGB')
    frame4.save('save.jpg')
    APP_ID = '20141345'
    API_KEY = 'vArkbCaa8NjuVbYmR31SzF7g'
    SECRET_KEY = 'O3hUtjaxrO3caUgby4o2wsBUImPfAZtx'
    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    with open('save.jpg', 'rb') as f:
        image = f.read()
    text = client.basicAccurate(image)
    # print(text)
    code = text['words_result'][0]['words']
    # print(code)
    time.sleep(2)
    # 输入验证码
    driver.find_element_by_xpath('//*[@id="loginForm"]/table/tbody/tr[4]/td[2]/span[1]/input[1]').send_keys(code)
    # #点击确定
    driver.find_element_by_xpath('//*[@id="loginForm"]/table/tbody/tr[5]/td/input').click()
    sleep(5)
    # 点击深圳中心
    driver.find_element_by_xpath('//*[@id="vehicleTree_95_switch"]').click()
    # 获取数据
    nub = driver.find_element_by_xpath('//*[@id="vehicleTree_1972_span"]').text
    nubs = nub[7:9]
    driver.find_element_by_xpath('//*[@id="vehicleTree_1972_check"]').click()

    i = 0
    nubs = int(nubs)
    print(nubs, type(nubs))
    #
    # print (nub)
    while i < nubs:
        mx1 = driver.find_element_by_xpath('//*[@id="rd_{}"]'.format(i)).text
        i = i + 1
        mx1 = str(mx1)
        wss_list.append(mx1)


def text_save(filename, wss_list):  # filename为写入CSV文件的路径，data为要写入数据列表.
    file = open(filename, 'a')
    for a in range(len(wss_list)):
        s = str(wss_list[a]).replace('[', '').replace(']', '')  # 去除[],这两行按数据不同，可以选择
        s = s.replace("'", '').replace(',', '') + '\n'  # 去除单引号，逗号，每行末尾追加换行符
        file.write(s)
    file.close()
    print("保存文件成功")


if __name__ == '__main__':
    wss_list = []
    start()
    logn()
    print(wss_list)
    text_save("name.txt", wss_list)

# input_phrase = driver.find_element_by_id("randomCode")
#
# cookies = driver.get_cookies()
# while True :
#     inputString = input_phrase.get_attribute("value")
#     if len(inputString)==4 :
#         sleep(1)
#         if len(inputString)==4:
#             print(inputString)
#             input_phrase.send_keys(Keys.ENTER)
#             break
# sleep(3)
# #
# for cook in cookies:
#     print("%s--->%s"%(cook["name"],cook["value"]))
# xtsz = driver.find_element_by_xpath("//div[@id='rightBar']/div/div[5]")
# ActionChains(driver).move_to_element(xtsz).perform()
# sleep(1)
# driver.find_element_by_xpath("//div[@id='rightBar']/div/div[5]/ul/li[4]").click()
# def vedioPlay():
#     B8753 = driver.find_element_by_id("vehicleTree_49_span")
#     # #   B03479 = driver.find_element_by_id("vehicleTree_2_span")
#     #     B03479 = driver.find_element_by_id("vehicleTree_10_span")
#     ActionChains(driver).context_click(B8753).perform()
#     driver.find_element_by_xpath('//*[@id="rightMenu"]/div[8]/div[1]').click()
#     sleep(1)
#     iframe = driver.find_element_by_id("commandIframe")
#     driver.switch_to_frame(iframe)
#     # 点击播放按钮
#     driver.find_element_by_xpath("//form[@id='entityForm']/div/div/div[2]/a[1]").click()
#     sleep(5)
#     driver.find_element_by_xpath("//form[@id='entityForm']/div/div/div[2]/a[1]").click()
#     sleep(15)
#     #关闭直播
#     driver.find_element_by_xpath("//form[@id='entityForm']/div/div/div[2]/a[2]").click()
#     sleep(1)
#     # 点击切换到车内
#     driver.find_element_by_xpath("//form[@id='entityForm']/div/div/div[3]/span[1]/input[2]").click()
#     sleep(1)
#     driver.find_element_by_xpath("//form[@id='entityForm']/div/div/div[2]/a[1]").click()
#     sleep(5)
#     driver.find_element_by_xpath("//form[@id='entityForm']/div/div/div[2]/a[1]").click()
#     sleep(15)
#     driver.find_element_by_xpath("//form[@id='entityForm']/div/div/div[2]/a[2]").click()
#     sleep(1)
#     #切换主码流
#     driver.find_element_by_xpath("//form[@id='entityForm']/div/div/div[3]/span[2]/input[2]").click()
#     sleep(1)
#     driver.find_element_by_xpath("//form[@id='entityForm']/div/div/div[2]/a[1]").click()
#     sleep(5)
#     driver.find_element_by_xpath("//form[@id='entityForm']/div/div/div[2]/a[1]").click()
#     sleep(15)
#     driver.find_element_by_xpath("//form[@id='entityForm']/div/div/div[2]/a[2]").click()
#     sleep(1)
#     #切换到车外
#     driver.find_element_by_xpath("//form[@id='entityForm']/div/div/div[3]/span[1]/input[1]").click()
#     sleep(1)
#     driver.find_element_by_xpath("//form[@id='entityForm']/div/div/div[2]/a[1]").click()
#     sleep(5)
#     driver.find_element_by_xpath("//form[@id='entityForm']/div/div/div[2]/a[1]").click()
#     sleep(15)
#     driver.find_element_by_xpath("//form[@id='entityForm']/div/div/div[2]/a[2]").click()
#     sleep(1)
#     # 关闭视频播放框
#     driver.find_element_by_xpath("//form[@id='entityForm']/div/div/div[2]/a[3]").click()
#     driver.switch_to_default_content()
#
# for i in range(50):
#     vedioPlay()
#     print(i+1)
#     sleep(160)
# sleep(1)
# # driver.close()
# # # driver.quit()