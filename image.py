import execjs
import webbrowser
from PIL import ImageGrab
import time
from selenium import webdriver
import requests
import json

url = 'http://zhjw.scu.edu.cn/login/'
#webbrowser.get("Safari").open(url)
# driver = webdriver.Safari()
# driver.maximize_window()
# driver.get(url)
# time.sleep(3)
# box = (1890,1200,2020,1275)
# im = ImageGrab.grab(box)
# im.show()



def openSafari():
    driver = webdriver.Safari()
    #driver.maximize_window()

    #driver.get(url)
    return driver

def operationAuth(driver):
    url = 'http://zhjw.scu.edu.cn/'
    #url = 'http://baidu.com'
    time.sleep(1)
    driver.get(url)
    # 找到输入框输入并查询内容
    print("请输入学号：")
    username = input()
    driver.find_element_by_id("input_username").send_keys(username)
    print("请输入密码：")
    password = input()
    driver.find_element_by_id("input_password").send_keys(password)
    print("请输入验证码：")
    # box = (1890, 1200, 2020, 1275)
    # im = ImageGrab.grab(box)
    # im.show()
    checkcode = input()
    driver.find_element_by_id("input_checkcode").send_keys(checkcode)
    driver.find_element_by_xpath('//*[@id = "loginButton"]').click()
    print("登录完毕")
    time.sleep(5)  #等待页面登录完成
    cookies = driver.get_cookies()
    return cookies





#if __name__ == '__main__':
global cookie
driver = openSafari()
cookies = operationAuth(driver)
for i in cookies:
    print(i)
    print(i['value'])
    cookie = i['value']


# driver.execute_script( "window.location.href = \"http://zhjw.scu.edu.cn/student/courseSelect/freeCourse/index?fajhh=5519\"") #跳转到自由选课界面
# time.sleep(5)
# print("请输入课程名：")
# kcm = input()
# driver.find_element_by_id("searchtj").send_keys(kcm) #输入课程名
# driver.find_element_by_xpath('//*[@id = "queryButton"]').click()
# time.sleep(3)

#iframe内嵌table！！真阴
#只显示有课余量的课程

#driver.execute_script("var a = document.querySelector(\"iframe\");var b = a.contentWindow.document;var c = b.getElementById(\"kyl\");c['value']=1;") #只显示有课余量的

# driver.execute_script("""
#     var a = document.querySelector("iframe");
#     var b = a.contentWindow.document;
#     var c = b.getElementById("xirxkxkbody");
#     d = c.getElementsByTagName("tr");
#     for(var i = 0;i<d.length;i++){
#         if(d[i].getElementsByTagName("td")[2].innerHTML == ""){    查看课程名字是否为我们要的
#
#         }
#     }
# }
#                       """)


driver.quit()
