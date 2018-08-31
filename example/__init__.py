# -*- coding: utf-8 -*-
import os
import dlib

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
# LOGIN_URL = 'http://172.20.10.6:7000/outmoded_browser'
LOGIN_URL = 'https://passport.hupu.com/pc/login?project=www&from=pc'
