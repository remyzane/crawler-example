# -*- coding: utf-8 -*-
import os
import cv2

from dlib import point, rectangle, rectangles


def pattern_recognize(recognizer, image_path, target_number=0) -> rectangles:
    """ 图像识别

    :param recognizer: 识别器
    :param image_path: 要识别的图片地址
    :param target_number: 要识别的目标数量，为0时返回识别到的所有区域（矩形）
                          TODO 有时间搞清楚：返回结果是否按匹配度排序？参数为1时是否返回最匹配的区域？
    :return rectangles: 区域（矩形）列表
    """
    # 加载图片
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 识别图片
    return recognizer(image=gray, upsample_num_times=target_number)


def pattern_recognize_x_coordinate(recognizer, image_path, scaled_width=None):
    """ 识别图像中匹配区域的中心点的x轴坐标（一个）

    :param recognizer: 识别器
    :param image_path: 要识别的图片地址
    :param scaled_width: 图片缩放后的宽度（图片在html中会缩放，为了方便业务开发，返回值也同比缩放）
    :return None|int: 匹配区域（矩形）的中心点的x轴坐标（如果指定了缩放后的宽度，则返回值也同比缩放）
    """
    # 加载图片
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 识别图片
    result = recognizer(image=gray, upsample_num_times=1)
    # 返回结果
    if result:
        target = result[0]          # type: rectangle
        center = target.center()    # type: point
        if scaled_width:
            __, width, __ = image.shape  # height, width, channels
            return center.x * scaled_width / int(width)
        else:
            return center.x


def splash_get_lua_source(lua_file, js_file=None, folder=None):
    """ 拼装 splash 的 lua 和 js
    :param lua_file: lua 源文件
    :param js_file: js 源文件
    :param folder: 源文件所在目录
    :return: lua 文件内容， 或拼装后的lua代码（指定了 js_file 时）
    """
    if folder:
        lua_file = os.path.join(folder, lua_file)
        if js_file:
            js_file = os.path.join(folder, js_file)

    with open(lua_file, 'r') as lua_f:
        lua_src = lua_f.read()

    if js_file:
        with open(js_file, 'r') as js_f:
            js_source = js_f.read()
        lua_beg, lua_end = lua_src.split('function main(splash, args)')
        lua_src = lua_beg + 'function main(splash, args)'
        lua_src = lua_src + '\n\n    splash:autoload([['
        lua_src = lua_src + js_source + '\n    ]])' + lua_end
        return lua_src
    else:
        return lua_src
