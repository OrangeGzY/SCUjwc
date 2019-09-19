# -*- coding: utf-8 -*-
import image
import requests
from bs4 import BeautifulSoup
import time


url = 'http://zhjw.scu.edu.cn/login/'
url_SelectCourse = 'http://zhjw.scu.edu.cn/student/courseSelect/freeCourse/courseList'  #自由选课界面
url_select = 'http://zhjw.scu.edu.cn/student/courseSelect/selectCourse/checkInputCodeAndSubmit' #向这个页面post，即选课
url_token = 'http://zhjw.scu.edu.cn/student/courseSelect/courseSelect/index' #拿token的地方
url_query = 'http://zhjw.scu.edu.cn/student/courseSelect/selectResult/query'
cookie = 'JSESSIONID='+image.cookie



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

print("cookie拼接完成:",cookie)
print("请输入目标课程完整名称：")
target_class = input()
print("请输入目标课程课程号：")
target_kechenghao = input()
print("请输入目标课程课序号：")
target_kexuhao = input()
print("请输入目标课程完整课程号+课序号（用_连接）：")
target_kechenghao_kexuhao = input()


token_headers = {
        'Referer':'http://202.115.47.141/login',
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0',
        'Host':'202.115.47.141',
        'Cookie': cookie
}

print("正在获取token......\n")
r_token = requests.get(url_token,headers = token_headers)
r_token = BeautifulSoup(r_token.text,"html.parser")
token = r_token.find("input" , attrs={'id':"tokenValue"})['value'] #抓取tokenvalue
print("token获取成功：",token)
kcIds = target_kechenghao_kexuhao + '_' + '2019-2020-1-1'
kcms_ = target_class+'_'+target_kexuhao
kcms = ''
for chr in kcms_:
    kcms += (str(ord(chr)) + ',') #形如：32593,32476,25915,38450,25216,26415,95,48,50,

param_Select={
            'dealType': '5',
            'kcIds':kcIds,      # 你的目标课程号_开课学期
            'kcms':kcms,
            'fajhh':'',
            'sj':'0_0',
            'searchtj':kcIds,      # 你在搜索框内搜索的东西（url编码后）
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
url_sever = "https://sc.ftqq.com/SCU61566T57ee337c6d60f1e1e6ca137ab29873825d8260c1ef41e.send"
username = '2018141501071' + '5'
count = 0
while(1):
    r = requests.post(url_SelectCourse, headers=headers_CourseSelect, data=param_SelectCourse)  # 向自由选课界面post以获取课余量
    print(r.status_code)
    # print(r.text)
    # 返回示例：{"rwRxkZlList":"[{\"bkskrl\":80,\"bkskyl\":-16,\"cxjc\":\"2\",\"id\":\"2714\",\"jasm\":\"二基楼B300\",\......
    r = r.json()
    r_json = r.get(
        "rwRxkZlList")  # json化： [{"bkskrl":21,"bkskyl":0,"cxjc":"3","id":"5025","jasm":"A111","jxlm":"一教A座","kch":"314009030","kclbdm":"","kclbmc":"","kcm":"网络渗透测试技术","kkxqh":"03","kkxqm":"江安","kkxsh":"314","kkxsjc":"网络空间安全学院","kslxdm....
    r_json = eval(r_json)
    length = len(r_json)
    for i in range(length):
        keyuliang = r_json[i]['bkskyl']
        #jiaoxuelou = r_json[i]['jxlm']
        # jiaoshi = r_json[i]['jasm']
        kechenghao = r_json[i]['kch']
        # kechengming = r_json[i]['kcm']
        kexuhao = r_json[i]['kxh']
        # print("课程名：", kechengming)
        # print("课程号：", kechenghao)
        # print("课序号：", kexuhao)
        # print("课余量", keyuliang)
        # print("\n")
        if(keyuliang > 0 and kexuhao == target_kexuhao and kechenghao == target_kechenghao):  #如果我们要选的有课余量
            r_final = requests.post(url_select, headers=token_headers, data=param_Select)
            print(r_final.text)
            print("选课成功")
            requests.post(url=url_sever,data=param_sever)  #微信发送提醒
            break
        elif(keyuliang <= 0 and kexuhao == target_kexuhao and kechenghao == target_kechenghao):
            print("第",count,"次选课,","目标课程无课余量。")
        count = count+1



    # s = time.localtime()[5]
    # if(s==0 or s==1 or s==2 or s==3):
    #     #print("test")
    #     r_final = requests.post(url_select, headers=token_headers, data=param_Select)
    #     print(r_final.text,"次数：",count)
    #     count = count+1
        #time.sleep(0.1)

#print("over")

# r_final = requests.post(url_select,headers = token_headers,data=param_Select)
#print(r_final.text)  #输出选课结果

# param_query = {
#     'kcNum': '1',
#     'redisKey': '20181415010715'
# }
# header = {
#         'Referer':'http://202.115.47.141/login',
#         'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0',
#         'Host':'202.115.47.141',
#         'Cookie': cookie
#         }
#

time.sleep(4)
queryCourse = requests.post(url=url_query,headers = headers_QueryCourser, data=param_query) #查询是否选课成功
print(queryCourse.status_code)
print(queryCourse.text)

# 网络渗透测试技术
# 314009030
# 314009030_01     http://202.115.47.141/student/courseSelect/selectResult/query      
#高级商务英语阅读与翻译 01 102342020_01

#一生受用的口腔卫生知识课    中华文化（历史篇）
#503185020_01           999005030_06
