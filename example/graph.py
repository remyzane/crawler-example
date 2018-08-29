# -*- coding: utf-8 -*-
""" 验证图片（滑动块位置）识别 """
import os
import cv2
import dlib

# 样本
samples_path = os.path.realpath(os.path.join(__file__, '..', '..', 'samples'))
training_xml_path = os.path.join(samples_path, 'training.xml')  # 样本数据
detector_svm_path = os.path.join(samples_path, 'detector.svm')  # 训练结果
# 图片探测器
detector = None
# 滑动块半径（用于获取中间点）
slide_block_radius = 42


def training():
    """ 训练样本 """
    print('training samples ...')
    options = dlib.simple_object_detector_training_options()
    # 要识别的图形是否左右对称
    options.add_left_right_image_flips = True
    # C越大表示更好地去拟合训练集，当然也有可能造成过拟合。通过尝试不同C在测试集上的效果得到最佳值
    options.C = 5
    # 训练数据时开启的线程数
    options.num_threads = 2
    # 是否输出详细日志
    options.be_verbose = False

    dlib.train_simple_object_detector(training_xml_path, detector_svm_path, options)


def recognition(image_path):
    """ 辩识图片（滑动块位置）

    :param image_path: 要识别的图片地址
    :return: 滑动块中心点的X坐标
    """
    global detector
    # 创建图片探测器
    if detector is None:
        if not os.path.exists(detector_svm_path):
            raise Exception('training method not called.')
        detector = dlib.simple_object_detector(detector_svm_path)
    # 加载图片
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 识别图片
    result = detector(gray, 1)
    # 返回结果
    for k, d in enumerate(result):
        return d.left() + slide_block_radius
