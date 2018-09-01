# -*- coding: utf-8 -*-
import os
import requests

from example import RECOGNIZE_API, pattern_recognizer
from example.utility import pattern_recognize, pattern_recognize_x_coordinate
from tests import test_dir


def test_recognition():
    """ 图片（滑动块位置）辩识测试（允许左右各5px的偏差） """
    image = os.path.join(test_dir, 'pattern_test', '6.jpg')
    result = pattern_recognize(pattern_recognizer, image, target_number=1)
    assert result
    result = result[0].center().x
    centre_x = 465  # 滑块中心点基准值
    assert result >= centre_x - 5
    assert result <= centre_x + 5

    image = os.path.join(test_dir, 'pattern_test', '6.jpg')
    result = pattern_recognize_x_coordinate(pattern_recognizer, image)
    centre_x = 465  # 滑块中心点基准值
    assert result >= centre_x - 5
    assert result <= centre_x + 5

    image = os.path.join(test_dir, 'pattern_test', '6.jpg')  # 图片时间宽度为600，html中缩放后宽度为300
    result = pattern_recognize_x_coordinate(pattern_recognizer, image, scaled_width=300)
    centre_x = 232.5  # 滑块中心点基准值
    assert result >= centre_x - 5
    assert result <= centre_x + 5

    image = os.path.join(test_dir, 'pattern_test', '8.jpg')
    result = pattern_recognize_x_coordinate(pattern_recognizer, image)
    assert result is None


def test_recognition_web_service():
    """ 图片（滑动块位置）辩识测试（允许左右各5px的偏差） """
    files = {'file': open(os.path.join(test_dir, 'pattern_test', '7.jpg'), 'rb')}
    response = requests.post(RECOGNIZE_API, files=files)
    result = response.json()
    centre_x = 271  # 滑块中心点基准值
    assert result['code'] == 'ok'
    assert result['value'] >= centre_x - 5
    assert result['value'] <= centre_x + 5

    files = {'file': open(os.path.join(test_dir, 'pattern_test', '7.jpg'), 'rb')}
    response = requests.post(RECOGNIZE_API + '?scaled_width=300', files=files)
    result = response.json()
    centre_x = 135.5  # 滑块中心点基准值（图片时间宽度为600，html中缩放后宽度为300）
    assert result['code'] == 'ok'
    assert result['value'] >= centre_x - 5
    assert result['value'] <= centre_x + 5

    files = {'file': open(os.path.join(test_dir, 'pattern_test', '7.jpg.txt'), 'rb')}
    response = requests.post(RECOGNIZE_API + '?file_format=base64', files=files)
    result = response.json()
    centre_x = 271  # 滑块中心点基准值
    print(result.get('info'))
    assert result['code'] == 'ok'
    assert result['value'] >= centre_x - 5
    assert result['value'] <= centre_x + 5

    files = {'file': open(os.path.join(test_dir, 'pattern_test', '7.jpg.txt'), 'rb')}
    response = requests.post(RECOGNIZE_API + '?scaled_width=300&file_format=base64', files=files)
    result = response.json()
    centre_x = 135.5  # 滑块中心点基准值（图片时间宽度为600，html中缩放后宽度为300）
    print(result.get('info'))
    assert result['code'] == 'ok'
    assert result['value'] >= centre_x - 5
    assert result['value'] <= centre_x + 5
