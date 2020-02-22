'''
    1.本脚本只供测试使用，不可以用于真正选课
    2.请测试完将文件删除
    3.所有解释权归脚本作者所有
    使用之前：安装对应版本的chromedriver以及相关库
'''
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image
import time
#from image import Login
class Login:
    def __init__(self, url_login, driver_path):
        self.url = url_login
        self.driver_path = driver_path

    def Open(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(executable_path=self.driver_path, chrome_options=chrome_options)
        driver.get(self.url)
        time.sleep(1.5)
        driver.maximize_window()
        return driver

    def Login(self):
        driver = self.Open()
        print("请输入学号：")
        username = input()
        driver.find_element_by_id("input_username").send_keys(username)
        print("请输入密码：")
        password = input()
        driver.find_element_by_id("input_password").send_keys(password)
        print("请输入验证码：")
        driver.save_screenshot("./test.png")
        ele = driver.find_element_by_id("captchaImg")
        loc = ele.location
        x = loc['x']
        y = loc['y']
        im = Image.open("./test.png")
        im = im.crop((x + 500, y + 450, x + 690, y + 520))
        im.show()
        checkcode = input()
        driver.find_element_by_id("input_checkcode").send_keys(checkcode)
        driver.find_element_by_xpath('//*[@id = "loginButton"]').click()
        print("登录完毕")
        return driver

    def Get_cookies(self):
        driver = self.Login()
        time.sleep(5)  # 等待页面登录完成
        global cookies
        cookies = driver.get_cookies()
        for i in cookies:
            # print(i)
            # print(i['value'])
            cookie = i['value']
        # print(cookie)
        driver.quit()
        return cookie


if __name__ == '__main__':
#def main():
    url = 'http://zhjw.scu.edu.cn/login/'
    driver_path = '/Users/apple/Downloads/chromedriver'    #你的驱动路径（绝对）
    Generator =  Login(url,driver_path)
    cookie = 'JSESSIONID=' + Generator.Get_cookies()
    print("cookie拼接完成:",cookie)

    ########################################################################################################################
    url = 'http://zhjw.scu.edu.cn/login/'
    url_SelectCourse = 'http://zhjw.scu.edu.cn/student/courseSelect/freeCourse/courseList'  #自由选课界面
    url_select = 'http://zhjw.scu.edu.cn/student/courseSelect/selectCourse/checkInputCodeAndSubmit' #向这个页面post，即选课
    url_token = 'http://zhjw.scu.edu.cn/student/courseSelect/courseSelect/index' #拿token的地方
    url_query = 'http://zhjw.scu.edu.cn/student/courseSelect/selectResult/query'

    headers_CourseSelect={
        'Host': 'zhjw.scu.edu.cn',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0',
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate',
        'Referer': 'http://zhjw.scu.edu.cn/student/courseSelect/freeCourse/index', #?fajhh=5519',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Length': '31',
        'Connection': 'keep-alive',
        'Cookie': cookie
    }

    headers_Login = {
        'Host': 'zhjw.scu.edu.cn',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate',
        'Referer': 'http://zhjw.scu.edu.cn/login',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': '91',
        'Connection': 'keep-alive',
        'Cookie': cookie,
        'Upgrade-Insecure-Requests': '1'
    }

    headers_QueryCourser={
        'Host': 'zhjw.scu.edu.cn',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Referer': 'http://zhjw.scu.edu.cn/student/courseSelect/selectCourses/waitingfor',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Length': '31',
        'Connection': 'close',
        'Cookie': cookie
    }
    token_headers = {
            'Referer':'http://202.115.47.141/login',
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0',
            'Host':'202.115.47.141',
            'Cookie': cookie
    }
    ########################################################################################################################
    print("请输入目标课程完整名称：")
    target_class = input()
    print("请输入目标课程课程号：")
    target_kechenghao = input()
    print("请输入目标课程课序号：")
    target_kexuhao = input()
    print("请输入目标课程完整课程号+课序号（用_连接）：")
    target_kechenghao_kexuhao = input()
    print("正在拼接课程信息...")
    kcIds = target_kechenghao_kexuhao + '_' + '2019-2020-1-1'
    kcms_ = target_class+'_'+target_kexuhao
    kcms = ''
    for chr in kcms_:
        kcms += (str(ord(chr)) + ',')
    print("课程信息拼接完成...")
    print("正在获取token......")
    r_token = requests.get(url_token,headers = token_headers)
    #print(token_headers)
    r_token = BeautifulSoup(r_token.text,"html.parser")
    #print(r_token)
    print(r_token.find("input" , attrs={'id':"tokenValue"}))
    token = r_token.find("input" , attrs={'id':"tokenValue"})['value'] #抓取tokenvalue
    print("token获取成功：",token)
    ########################################################################################################################
    param_Select={
                'dealType': '5',
                'kcIds':kcIds,
                'kcms':kcms,
                'fajhh':'5519',
                'sj':'0_0',
                'searchtj':kcIds,
                'kclbdm':'',
                'inputCode':'',
                'tokenValue':token
            }
    param_SelectCourse = {
        'searchtj': target_class,
        'xq': '0',
        'jc': '0',
        'kclbdm': ''
    }
    param_sever={
        'text': "选课成功",
        'desktop': '选课成功，请查看！'
    }
    url_sever = ""  #这是微信提醒发送功能，需自行注册server酱方可使用
    count=0
    while(1):
        r = requests.post(url_SelectCourse, headers=headers_CourseSelect, data=param_SelectCourse)
        r = r.json()
        r_json = r.get("rwRxkZlList")
        r_json = eval(r_json)
        length = len(r_json)
        for i in range(length):
            keyuliang = r_json[i]['bkskyl']
            #print("当前课程课余量：",keyuliang)
            kechenghao = r_json[i]['kch']
            kexuhao = r_json[i]['kxh']
            #print(kechenghao+","+kexuhao)
            if(keyuliang > 0 and kexuhao == target_kexuhao and kechenghao == target_kechenghao):
                for i in range(2):
                    r_final = requests.post(url_select, headers=token_headers, data=param_Select)
                #print("post done")
                #time.sleep(1)   #毛泽东思想和中国特色社会主义理论体系概论(107061050_65)
                # print(r_final.text)
                print("选课成功,等待脚本运行完毕请登录检查")
                # #requests.post(url=url_sever,data=param_sever)  #微信发送提醒
                time.sleep(10)
                param_query = {
                    'kcNum': '1',
                    'redisKey': '2018141501142' + '5'
                }
                header = {
                    'Referer': 'http://202.115.47.141/login',
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0',
                    'Host': '202.115.47.141',
                    'Cookie': cookie
                }
                print("正在查询选课结果...")
                queryCourse = requests.post(url=url_query, headers=headers_QueryCourser, data=param_query)  # 查询是否选课成功
                print(queryCourse.text)
                break
            elif(keyuliang <= 0 and kexuhao == target_kexuhao and kechenghao == target_kechenghao):
                print("done.")
                time.sleep(0.3)
                #count = count + 1

       # time.sleep(0.2)
#游戏艺术与技术(311161020_01)
#数论与代数基础(201110040_02)
#2019141410243
#092146
#数论与代数基础
#201110040_02
#
