# -*- coding: utf-8 -*-
import os
import uuid
import dlib
import requests

from .utility import splash_get_lua_source

workspace = os.path.realpath(os.path.join(__file__, '..', '..'))

samples_xml = os.path.join(workspace, 'samples', 'samples.xml')     # 样本数据
samples_svm = os.path.join(workspace, 'samples', 'samples.svm')     # 训练结果

# 图形识别器
pattern_recognizer = dlib.simple_object_detector(samples_svm)
# 滑动块半径（用于获取中间点）
slide_block_radius = 42

# run command: python3 service.py
SERVICE_URL = 'http://172.20.10.6:5000/pattern/recognize_x_coordinate'
SPLASH_URL = 'http://172.20.10.8:8050/execute'
# TARGET_URL = 'http://172.20.10.6:7000/outmoded_browser'
TARGET_URL = 'https://passport.hupu.com/pc/login?project=www&from=pc'



def login():

    with open(os.path.realpath(os.path.join(__file__, '..', 'login.lua')), 'r') as lua_file:
        login_lua = lua_file.read()

    result = requests.post(SPLASH_URL, json={
        'lua_source': login_lua,
        # lua args ----
        'url': TARGET_URL,
        'api': SERVICE_URL,
        'load_time': 4,                 # 加载时间
        'boundary': uuid.uuid4().hex,   # post（multipart/form-data）的 boundary 值
    })

    print('aaaa', result.text)


# login()
