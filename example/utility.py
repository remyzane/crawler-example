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
    return recognizer(gray, target_number)


def pattern_recognize_x_coordinate(recognizer, image_path):
    """ 识别图像中匹配区域的中心点的x轴坐标（一个）

    :param recognizer: 识别器
    :param image_path: 要识别的图片地址
    :return None|int: 匹配区域（矩形）的中心点的x轴坐标
    """
    result = pattern_recognize(recognizer, image_path, target_number=1)
    # 返回结果
    if result:
        target = result[0]          # type: rectangle
        center = target.center()    # type: point
        return center.x


def splash_get_lua_source(package, lua_file, js_file=None):
    """
    function main(splash, args)
  local aaa = [[
    function get_document_title(){
      return document.title;
    }
  ]]
  splash:autoload(aaa)

    :param package:
    :param lua_file:
    :param js_file:
    :return:
    """
    pass