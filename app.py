import json

import cv2
import requests
from flask import Flask, request, jsonify
from ultralytics import YOLO

app = Flask(__name__)

token = None
model = YOLO('G:/project/Video/pythonProject/model/best.pt')


# 接口接收传入的视频流地址，返回调用模型检测之后的人数
def detect_people_in_stream(rtsp_url):
    cap = cv2.VideoCapture(rtsp_url)
    if not cap.isOpened():
        return -1  # 返回 -1 表示无法打开视频流

    people_count = 0
    ret, frame = cap.read()
    if ret:
        # 使用模型检测帧中的人数
        results = model(frame)
        if results and hasattr(results[0], 'boxes'):
            boxes = results[0].boxes
            people_count = sum(1 for box in boxes if box.cls == 0)  # 假设类别 0 是“人”

    cap.release()
    return people_count


@app.route('/api/detect', methods=['POST'])
def detect():
    data = request.get_json()
    rtsp_url = data.get('rtsp_url')  # 从请求体中获取 rtsp_url 参数

    if not rtsp_url:
        return jsonify({"error": "缺少 rtsp_url 参数"}), 400

    people_count = detect_people_in_stream(rtsp_url)

    if people_count == -1:
        return jsonify({"error": "无法打开视频流"}), 500

    return jsonify({"number": people_count})


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


# 发送开关灯指令
def post_light(roomid, roomname, keyname):
    url = 'http://10.250.100.17/usiop/sysroomctrl/usruncode'
    headers = {
        'Content-Type': 'application/json',
    }

    params = {
        'token': token
    }

    body ={
        'keyname': keyname,
        'roomid': roomid,
        'roomname': roomname
    }

    response = requests.post(url, headers=headers, params=params, data=json.dumps(body))
    return response.json()


@app.route('/api/light', methods=['POST'])
def api_light():
    data = request.json
    roomid = data.get('roomid')
    roomname = data.get('roomname')
    keyname = data.get('keyname')
    result = post_light(roomid, roomname, keyname)
    return jsonify(result)


if __name__ == '__main__':
    token = gettoken()
    app.run(host='0.0.0.0', port=5011)
