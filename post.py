import requests
import json

token = None


# 登录获取token
def gettoken():
    url = 'http://10.250.100.17/account/uslogin_novalidate'
    data = {
        "userid": "00002003",
        "userpwd": "Nimda@123",
        "userstate": "0"
    }
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.post(url, data=json.dumps(data), headers=headers)

    # 将获取的token存在变量中
    response_data = response.json()
    token = response_data['data']['token']
    return token


# 获取教室列表
def get_classroom_list():
    classrooms = {}
    url = 'http://10.250.100.17/usiop/sysroom/usgetlist'
    headers = {
        'Content-Type': 'application/json',
    }

    for page in range(1, 19):
        params = {
            'token': token,
            'page': page,
        }
        response = requests.get(url, headers=headers, params=params)
        response_data = response.json()
        for classroom in response_data['data']:
            classrooms[classroom['roomid']] = classroom['roomname']
    return classrooms


# 发送开关灯指令
def post_light(roomid, roomname):
    url = 'http://10.250.100.17/usiop/sysroomctrl/usruncode'
    headers = {
        'Content-Type': 'application/json',
    }

    params = {
        'token': token
    }

    body = {
        'keyname': '关总灯光',
        'roomid': roomid,
        'roomname': roomname
    }

    response = requests.post(url, headers=headers, params=params, data=json.dumps(body))
    print(response.json())


if __name__ == '__main__':
    token = gettoken()
    clasrom = get_classroom_list()
    print(clasrom)
    # for roomid, roomname in clasrom.items():
    #     post_light(roomid, roomname)

