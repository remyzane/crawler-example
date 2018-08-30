# -*- coding: utf-8 -*-
import os
import requests
from . import test_path
from example.graph import recognition
from example.splash import SERVICE_URL


def test_recognition():
    """ 图片（滑动块位置）辩识测试（允许左右各5px的偏差） """
    result = recognition(os.path.join(test_path, '6.jpg'))
    centre_x = 465  # 滑块中心点基准值
    assert result >= centre_x - 5
    assert result <= centre_x + 5


def test_recognition_web_service():
    """ 图片（滑动块位置）辩识测试（允许左右各5px的偏差） """
    files = {'file': open(os.path.join(test_path, '7.jpg'), 'rb')}
    response = requests.post(SERVICE_URL, files=files)
    result = response.json()
    centre_x = 271  # 滑块中心点基准值
    assert result['code'] == 'ok'
    assert result['value'] >= centre_x - 5
    assert result['value'] <= centre_x + 5

    files = {'file': open(os.path.join(test_path, '7.jpg.txt'), 'rb')}
    response = requests.post(SERVICE_URL + '?file_format=base64', files=files)
    result = response.json()
    centre_x = 271  # 滑块中心点基准值
    print(result.get('info'))
    assert result['code'] == 'ok'
    assert result['value'] >= centre_x - 5
    assert result['value'] <= centre_x + 5