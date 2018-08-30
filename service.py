#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" 滑动块位置识别 WEB 接口服务 """
import os
import uuid
import base64
import logging
from flask import Flask, jsonify, request

from example.graph import recognition

TMP_FOLDER = '/tmp/crawler-example/'
if not os.path.exists(TMP_FOLDER):
    os.mkdir(TMP_FOLDER)

app = Flask(__name__)
log = logging.getLogger(__name__)


def request_args(arg, default_value=None):
    """ 获取request参数

    GET 和 POST 都有 request.args （url地址上的参数）；
    如果是 POST 还有 request.form 或 request.json（根据 Content-Type）

    :param arg: 请求参数
    :param default_value: 如果没有时使用的默认值
    :return: 请求参数值
    """
    if request.method == 'GET':
        return request.args.get(arg, default_value)
    else:   # POST
        # 先从url地址上获取
        value = request.args.get(arg)
        if value:
            return value
        else:
            if request.json is None:
                # Content-Type: application/x-www-form-urlencoded
                return request.form.get(arg, default_value)
            else:
                # Content-Type: application/json
                return request.json.get(arg, default_value)


@app.route('/graph/recognition', methods=['POST'])
def graph_recognition():
    """ 辩识图片（滑动块位置）

    :post file: 要识别的图片
    :post arg file_format: 上传的文件格式 [ raw 原始格式 | base64 ascii 编码 ]
        该参数可为调用方提供方便，如 splash:http_post 的 body 不支持 raw（会报python <-> lua 转换错误）
    """
    if 'file' not in request.files:
        log.error('No file part')
        return jsonify({'code': 'no_file_part', 'info': 'No file part'})
    try:
        file = request.files['file']
        file_path = os.path.join(TMP_FOLDER, uuid.uuid4().hex)
        file_format = request_args('file_format', 'raw')    # base64 or raw
        if file_format == 'raw':
            file.save(file_path)
        elif file_format == 'base64':
            content = base64.b64decode(file.stream.read())
            with open(file_path, 'wb') as raw_file:
                raw_file.write(content)
        else:
            log.error('Unknown file format: %s' % file_format)
            return jsonify({'code': 'unknown_file_format',
                            'info': 'Unknown file format: %s' % file_format})
        return jsonify({'code': 'ok', 'value': recognition(file_path)})

    except Exception as e:
        log.exception('Unknown Error')
        return jsonify({'code': 'unknown_error', 'info': str(e)})


# 运行服务
app.debug = True
app.run(host='0.0.0.0', use_reloader=True)