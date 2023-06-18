import json
from urllib import parse
import requests
import sys
import re
import random
import time
import os

jobId = 'f867db47149de2901XNz29m9F1RR'

os.chdir(sys.path[0])
path = os.path.abspath('.')
lastPath = os.path.abspath('..')

# 获取求职牛人信息列表html
def getJobSeekersList( page, headers, proxies ):
    # 这里是你的求职推荐列表
    global url
    url = 'https://www.zhipin.com/wapi/zpjob/rec/geek/list?jobId=' + jobId + '&page=' + str(page)
    print(url)
    result = requests.get(url, headers=headers, proxies=proxies, timeout=1).json()
    jobSeekersList = result['zpData']['geekList']
    return jobSeekersList

# 读取本地cookie
fCookie = open(lastPath + '/config/cookie.txt','r')
cookie = fCookie.readline()
fCookie.close()


# 写死的header
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'cache-control': 'max-age=0',
    'cookie': cookie,
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
}

# 与牛人打招呼
def greetToJobSeeker( uid, jid, expectId, lid, headers, proxies ):
    params = {
        'gids': uid,
        'jids': jid,
        'expectIds': expectId,
        'lids': lid,
    }
    greetResult = requests.post('https://www.zhipin.com/chat/batchAddRelation.json', headers=headers, proxies=proxies, data=params)
    print(greetResult)

# 向牛人发送简历申请
def requestResumeToJobSeeker( uid, proxies ):
    requestResumeResult = requests.get('https://www.zhipin.com/chat/requestResume.json?to=' + str(uid) + '&_=' + str(int(round(time.time() * 1000))), headers=headers, proxies=proxies).json()
    print(requestResumeResult)

# 接受牛人简历
def acceptResumeOfJobSeeker( uid, proxies ):
    acceptResumeResuslt = requests.get('https://www.zhipin.com/chat/acceptResume.json?to=' + str(uid) + '&mid=' + str(38834193982) + '&aid=41&action=0&extend=&_=' + str(int(round(time.time() * 1000))), headers=headers, proxies=proxies).json()
    print(acceptResumeResuslt)

loop = True
page = 1
while loop:
    if page > 30 :
        loop = False
    proxies = None
    
    # 获取求职牛人信息列表html
    try :
        jobSeekersList = getJobSeekersList(page, headers, proxies)
        print(jobSeekersList)
    except Exception as e:
        if (str(e).find('www.zhipin.com') != -1) :
            continue
        print(str(e))
        # chrome=webbrowser.get('chrome')

        # chrome.open(url)
        print(url)
        break
    for jobSeeker in jobSeekersList :
        # 联系状态
        isFriend = jobSeeker['isFriend']
        if isFriend == 0 :
            contactStatus = "打招呼"
        else :
            contactStatus = "继续沟通"
        jobSeekerInfo = jobSeeker['geekCard']

        # 相关id
        encryptGeekId = jobSeeker['encryptGeekId']#gid
        geekId = jobSeekerInfo['geekId']#uid
        lid = jobSeekerInfo['lid']
        expectId = jobSeekerInfo['expectId']

        # 所在地 杭州
        location = jobSeekerInfo['expectLocationName']
        # 工作年限 5年
        workTime = jobSeekerInfo['geekWorkYear']
        # 学历 本科/硕士
        education = jobSeekerInfo['geekDegree']
        # 年龄 25岁
        age = jobSeekerInfo['ageDesc']
        # 工作状态 在职-考虑机会
        workStatus = jobSeekerInfo['applyStatusDesc']
        # 活跃状态 刚刚活跃
        activeStatus = jobSeeker['activeTimeDesc']
        # 期望薪资
        salary = jobSeekerInfo['salary']
        # 姓名
        name = jobSeekerInfo['geekName']
        # 毕业学校
        school = jobSeekerInfo['geekEdu']['school']
        if contactStatus == '打招呼':
            # 与牛人打招呼
            greetToJobSeeker( geekId, jobId, expectId, lid, headers, proxies)
        if contactStatus == '继续沟通':
            # 向牛人发送简历申请
            requestResumeToJobSeeker(geekId, proxies)
            # 接受牛人简历
            acceptResumeOfJobSeeker(geekId, proxies) 
